"""
BeMyAccess crawler.

Reads the news sources listed in sources.json, merges what it finds into
articles.json inside your website repo, then commits and pushes that one file
to GitHub (GitHub Pages republishes the site a minute or two later).

Usage (from the crawler folder):
    python crawl.py --dry-run     crawl and print what it would publish; writes and pushes nothing
    python crawl.py --no-push     crawl and update articles.json locally; no git
    python crawl.py               full run: pull, crawl, update articles.json, commit, push
"""
import argparse
import hashlib
import html
import json
import logging
import os
import re
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
CONFIG_PATH = Path(os.environ.get("BMA_CONFIG", BASE / "sources.json"))
UA = "BeMyAccessCrawler/1.0 (+https://bemyaccess.org)"
CATEGORIES = {"Local News", "News for the Disabled", "Weather"}
RETRIES = 3
RETRY_SLEEP = int(os.environ.get("BMA_RETRY_SLEEP", "60"))   # seconds between retries
DELAY = float(os.environ.get("BMA_DELAY", "1.5"))            # seconds between requests
COMMON_FEEDS = ["/feed/", "/feed", "/rss", "/rss.xml", "/feed.xml", "/atom.xml"]
BAD_TITLES = re.compile(r"(page not found|404|access denied|just a moment|forbidden|not found|"
                        r"attention required|are you a human)", re.I)
SKIP_PATH = re.compile(r"/(tag|tags|category|categories|author|page|feed|wp-content|wp-admin|wp-json|"
                       r"login|cart|search|contact|donate|privacy|terms)(/|$)", re.I)
SKIP_EXT = re.compile(r"\.(pdf|jpe?g|png|gif|zip|docx?|xlsx?|mp3|mp4)$", re.I)
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


# ───────────────────────── small helpers ─────────────────────────
def clean(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


def strip_tags(s):
    return clean(re.sub(r"<[^>]+>", " ", s or ""))


def truncate(s, n):
    s = clean(s)
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(",;:-– ")
    return cut + "…"


def normalize_url(u):
    p = urlparse(u)
    q = [(k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith(("utm_", "fbclid", "gclid"))]
    return urlunparse((p.scheme, p.netloc.lower(), p.path, "", urlencode(q), ""))


def host_key(u):
    h = urlparse(u).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def parse_date(s):
    s = clean(s)
    if not s:
        return None
    try:
        return parsedate_to_datetime(s).date()
    except Exception:
        pass
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
    except Exception:
        pass
    m = re.search(rf"({MONTHS})\s+(\d{{1,2}}),?\s+(\d{{4}})", s)
    if m:
        try:
            return datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%B %d %Y").date()
        except Exception:
            pass
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except Exception:
            pass
    return None


def fmt_date(d):
    return f"{d:%B} {d.day}, {d.year}"


def with_retries(fn, what, retries=RETRIES, sleep=RETRY_SLEEP):
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as e:
            logging.warning(f"{what}: attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(sleep)
    logging.error(f"{what}: giving up after {retries} attempts")
    return None


# ───────────────────────── fetching ─────────────────────────
class Fetcher:
    def __init__(self, ctx):
        self.ctx = ctx
        self.robots = {}
        self.last = 0.0

    def _pause(self):
        wait = DELAY - (time.time() - self.last)
        if wait > 0:
            time.sleep(wait)
        self.last = time.time()

    def allowed(self, url):
        p = urlparse(url)
        root = f"{p.scheme}://{p.netloc}"
        rp = self.robots.get(root)
        if rp is None:
            rp = RobotFileParser()
            try:
                r = self.ctx.request.get(root + "/robots.txt", timeout=20000, headers={"User-Agent": UA})
                if r.status == 200:
                    rp.parse(r.text().splitlines())
                elif r.status >= 500:
                    rp.disallow_all = True
                else:
                    rp.allow_all = True
            except Exception as e:
                logging.warning(f"robots.txt not readable for {root}: {e} (treating as allowed)")
                rp.allow_all = True
            self.robots[root] = rp
        return rp.can_fetch(UA, url)

    def get_text(self, url):
        """Plain HTTP GET (used for feeds). Returns text or None."""
        if not self.allowed(url):
            logging.info(f"  skipped (blocked by robots.txt): {url}")
            return None
        self._pause()
        r = self.ctx.request.get(url, timeout=30000, headers={"User-Agent": UA})
        if r.status != 200:
            logging.info(f"  no feed at {url} (HTTP {r.status})")
            return None
        return r.text()

    def open_page(self, page, url):
        """Load a page in the browser (runs JavaScript). Raises on failure."""
        if not self.allowed(url):
            raise PermissionError(f"blocked by robots.txt: {url}")
        self._pause()
        resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
        if resp is not None and resp.status >= 400:
            raise RuntimeError(f"HTTP {resp.status}")
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass


# ───────────────────────── feeds ─────────────────────────
def local(tag):
    return tag.split("}")[-1].lower()


def child_text(el, *names):
    for c in el:
        if local(c.tag) in names and (c.text or "").strip():
            return c.text
    return ""


def parse_feed(text):
    """Return a list of dicts: title, url, date, summary, paras. Raises if not a feed."""
    if re.search(r"<!ENTITY", text, re.I):
        raise ValueError("feed uses XML entities; refusing to parse")
    root = ET.fromstring(text.strip())
    items = []
    for el in root.iter():
        if local(el.tag) not in ("item", "entry"):
            continue
        link = child_text(el, "link")
        if not link:
            for c in el:
                if local(c.tag) == "link" and c.get("href") and c.get("rel", "alternate") == "alternate":
                    link = c.get("href")
                    break
        body_html = child_text(el, "encoded", "content") or child_text(el, "description", "summary")
        paras = [strip_tags(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", body_html, re.S | re.I)]
        paras = [p for p in paras if len(p) >= 40]
        plain = strip_tags(body_html)
        items.append({
            "title": clean(child_text(el, "title")),
            "url": clean(link),
            "date": parse_date(child_text(el, "pubdate", "published", "updated", "date")),
            "summary": plain,
            "paras": paras or ([plain] if plain else []),
        })
    if not items:
        raise ValueError("no items in feed")
    return items


def try_feed(fetcher, url):
    try:
        text = fetcher.get_text(url)
        if not text:
            return None
        return parse_feed(text)
    except Exception as e:
        logging.info(f"  not a usable feed: {url} ({e})")
        return None


# ───────────────────────── scraping ─────────────────────────
PAGE_JS = """() => {
  const meta = (sel, attr) => { const e = document.querySelector(sel); return e ? (e.getAttribute(attr) || '').trim() : ''; };
  const root = document.querySelector('article') || document.querySelector('main') || document.body;
  const paras = [...root.querySelectorAll('p')].map(p => p.innerText.trim()).filter(t => t.length >= 40);
  const t = document.querySelector('time');
  return {
    ogTitle: meta('meta[property="og:title"]', 'content'),
    h1: (document.querySelector('h1') || {}).innerText || '',
    docTitle: document.title || '',
    desc: meta('meta[property="og:description"]', 'content') || meta('meta[name="description"]', 'content'),
    published: meta('meta[property="article:published_time"]', 'content') || meta('meta[name="date"]', 'content')
               || meta('time[datetime]', 'datetime') || (t ? t.innerText : ''),
    ld: [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent).join('\\n'),
    siteName: meta('meta[property="og:site_name"]', 'content'),
    feedLink: meta('link[rel="alternate"][type="application/rss+xml"]', 'href')
              || meta('link[rel="alternate"][type="application/atom+xml"]', 'href'),
    paras: paras.slice(0, 8),
  };
}"""

LINKS_JS = """(sel) => {
  let els = [...document.querySelectorAll(sel)];
  if (!els.length) els = [...document.querySelectorAll('a[href]')];
  return els.map(e => ({text: (e.innerText || '').trim(), href: e.href}));
}"""


def candidate_links(links, listing_url, src):
    inc = re.compile(src["link_include"]) if src.get("link_include") else None
    exc = re.compile(src["link_exclude"]) if src.get("link_exclude") else None
    seen, out = set(), []
    for l in links:
        href, text = l.get("href") or "", clean(l.get("text"))
        if not href.startswith(("http://", "https://")):
            continue
        u = normalize_url(href)
        p = urlparse(u)
        if host_key(u) != host_key(listing_url) or u == normalize_url(listing_url) or p.path in ("", "/"):
            continue
        if SKIP_PATH.search(p.path) or SKIP_EXT.search(p.path):
            continue
        if len(text) < 25 or len(text.split()) < 4:
            continue
        if inc and not inc.search(u):
            continue
        if exc and exc.search(u):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def scrape_article(fetcher, page, url, site_name):
    try:
        fetcher.open_page(page, url)
        d = page.evaluate(PAGE_JS)
    except Exception as e:
        logging.warning(f"  skip {url}: {e}")
        return None
    title = clean(d["ogTitle"] or d["h1"] or d["docTitle"])
    for name in {d.get("siteName") or "", site_name}:
        if name:
            title = re.sub(rf"\s*[|\-–—:]\s*{re.escape(name)}\s*$", "", title, flags=re.I)
    when = parse_date(d["published"])
    if not when:
        m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', d.get("ld") or "")
        when = parse_date(m.group(1)) if m else None
    return {"title": title, "url": url, "date": when, "summary": clean(d["desc"]), "paras": d["paras"]}


def crawl_source(fetcher, page, src):
    """Return (items, ok). items are dicts with title, url, date, summary, paras."""
    name = src["name"]
    limit = int(src.get("max_articles", 10))
    pages = src["pages"]
    root = f"{urlparse(pages[0]).scheme}://{urlparse(pages[0]).netloc}"

    # 1) RSS/Atom feed, if the source has one
    feeds = ([src["feed"]] if src.get("feed") else []) + [root + p for p in COMMON_FEEDS]
    for f in feeds:
        items = try_feed(fetcher, f)
        if items:
            logging.info(f"  using feed {f} ({len(items)} items)")
            return items[:limit], True

    # 2) otherwise read the listing page(s) with a real browser
    links, feed_link, opened = [], "", 0
    for lp in pages:
        if not with_retries(lambda: fetcher.open_page(page, lp) or True, f"{name}: open {lp}"):
            continue
        opened += 1
        feed_link = feed_link or page.evaluate(PAGE_JS)["feedLink"]
        sel = src.get("link_selector") or "main a[href], article a[href], #content a[href], .content a[href]"
        links += candidate_links(page.evaluate(LINKS_JS, sel), lp, src)
    if not opened:
        return [], False                      # site unreachable
    if feed_link:
        items = try_feed(fetcher, urljoin(root, feed_link))
        if items:
            logging.info(f"  using feed {feed_link} ({len(items)} items)")
            return items[:limit], True
    if not links:
        logging.warning(f"  {name}: no article-like links found")
        return [], True
    items = []
    for u in list(dict.fromkeys(links))[: limit * 2]:
        it = scrape_article(fetcher, page, u, name)
        if it and (it["date"] or not src.get("require_date", True)):
            items.append(it)
        if len(items) >= limit:
            break
    logging.info(f"  scraped {len(items)} dated articles from {len(links)} candidate links")
    return items, True


# ───────────────────────── records ─────────────────────────
def make_record(src, it, today):
    title = clean(it["title"])
    if len(title) < 10 or BAD_TITLES.search(title) and len(title) < 40:
        return None
    url = normalize_url(it["url"])
    if not url.startswith(("http://", "https://")):
        return None
    paras, total = [], 0
    for p in it.get("paras") or []:
        if total + len(p) > 1200 and paras:
            break
        paras.append(truncate(p, 1200))
        total += len(p)
    summary = truncate(it.get("summary") or (paras[0] if paras else ""), 300)
    if not summary:
        return None
    if not paras:
        paras = [summary]
    return {
        "id": int(hashlib.sha256(url.encode()).hexdigest()[:8], 16),
        "category": src["category"],
        "source": src["name"],
        "published": fmt_date(it["date"] or today),
        "date": (it["date"] or today).isoformat(),
        "_dated": bool(it["date"]),
        "title": title,
        "summary": summary,
        "body": "".join(f"<p>{html.escape(p)}</p>" for p in paras),
        "url": url,
        "first_seen": today.isoformat(),
    }


def merge(existing, fresh, today, retention_days):
    by_url = {a["url"]: a for a in existing}
    new = changed = 0
    cutoff = (today - timedelta(days=retention_days)).isoformat()
    too_old = [r for r in fresh if r["date"] < cutoff]    # ignore stories already past retention
    fresh = [r for r in fresh if r["date"] >= cutoff]
    if too_old:
        logging.info(f"Ignored {len(too_old)} articles older than {retention_days} days (before {cutoff})")
    title_key = lambda a: (a["source"], clean(a["title"]).casefold())
    seen_titles = {title_key(a): a["url"] for a in existing}
    for rec in fresh:
        # the same story can appear under two addresses; keep only the first one
        if seen_titles.setdefault(title_key(rec), rec["url"]) != rec["url"]:
            logging.info(f"Skipping duplicate title: {rec['title'][:70]} ({rec['url']})")
            continue
        old = by_url.get(rec["url"])
        dated = rec.pop("_dated")
        if old:
            rec["first_seen"] = old.get("first_seen", rec["first_seen"])
            if not dated:
                rec["date"], rec["published"] = old.get("date", rec["date"]), old.get("published", rec["published"])
            keys = ("title", "summary", "body", "category", "source", "date")
            if any(old.get(k) != rec[k] for k in keys):
                changed += 1
            else:
                rec = old
        else:
            new += 1
        by_url[rec["url"]] = rec
    kept = [a for a in by_url.values() if a.get("date", "9999") >= cutoff]
    dropped = len(by_url) - len(kept)
    kept.sort(key=lambda a: (a.get("date", ""), a.get("first_seen", ""), a["id"]), reverse=True)
    return kept, new, changed, dropped


# ───────────────────────── git ─────────────────────────
def git(repo, *args, check=True):
    cmd = ["git", "-C", str(repo)]
    for key, default in (("user.name", "BeMyAccess Crawler"), ("user.email", "crawler@users.noreply.github.com")):
        have = subprocess.run(["git", "-C", str(repo), "config", key], capture_output=True, text=True).stdout.strip()
        if not have:
            cmd += ["-c", f"{key}={default}"]
    cmd += list(args)
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=180)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {(r.stderr or r.stdout).strip()}")
    return r


def pull(repo, branch):
    r = git(repo, "pull", "--rebase", "--autostash", "origin", branch, check=False)
    if r.returncode != 0:
        git(repo, "rebase", "--abort", check=False)
        raise RuntimeError(f"git pull failed: {(r.stderr or r.stdout).strip()}")


def publish(repo, branch, message):
    """Commit articles.json (only that file) and push. Returns True if something was pushed."""
    git(repo, "add", "--", "articles.json")
    staged = git(repo, "diff", "--cached", "--quiet", "--", "articles.json", check=False)
    if staged.returncode != 0:
        git(repo, "commit", "-m", message, "--", "articles.json")
    ahead = git(repo, "log", f"origin/{branch}..HEAD", "--format=%s", check=False).stdout.split("\n")
    ahead = [s for s in ahead if s.strip()]
    if not ahead:
        return False
    if not all(s.startswith("Update articles") for s in ahead):
        logging.warning("Your repo has other unpushed commits; not pushing them. Push them yourself when ready.")
        return False
    r = git(repo, "push", "origin", f"HEAD:{branch}", check=False)
    if r.returncode != 0:
        pull(repo, branch)
        git(repo, "push", "origin", f"HEAD:{branch}")
    return True


# ───────────────────────── main ─────────────────────────
def load_config():
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))   # tolerates a BOM from Windows editors
    for s in cfg["sources"]:
        if s.get("enabled", True):
            assert s["category"] in CATEGORIES, f"{s['name']}: category must be one of {sorted(CATEGORIES)}"
            assert s.get("pages"), f"{s['name']}: needs at least one page URL"
    return cfg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="crawl and print results; write and push nothing")
    ap.add_argument("--no-push", action="store_true", help="update articles.json locally but do not use git")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        handlers=[logging.FileHandler(BASE / "crawl.log", encoding="utf-8"),
                                  logging.StreamHandler(sys.stdout)])
    def _watchdog():
        logging.error("Crawler ran longer than 20 minutes; stopping it.")
        os._exit(9)
    t = threading.Timer(20 * 60, _watchdog)
    t.daemon = True
    t.start()

    cfg = load_config()
    repo = Path(cfg["repo_path"])
    branch = cfg.get("branch", "main")
    out_file = repo / "articles.json"
    if not (repo / "index.html").exists():
        logging.error(f"repo_path does not look like the website repo: {repo}")
        return 2
    use_git = not (args.dry_run or args.no_push)
    today = date.today()

    if use_git:
        try:
            if git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() != branch:
                raise RuntimeError(f"repo is not on branch '{branch}'")
            pull(repo, branch)
        except Exception as e:
            logging.error(f"Could not update the repo, stopping: {e}")
            return 3

    existing = []
    if out_file.exists():
        try:
            existing = json.loads(out_file.read_text(encoding="utf-8"))
        except Exception as e:
            logging.error(f"articles.json is not valid JSON, stopping so it is not overwritten: {e}")
            return 2

    fresh, failed = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--blink-settings=imagesEnabled=false"])   # no images: faster, lighter
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        fetcher = Fetcher(ctx)
        for src in cfg["sources"]:
            if not src.get("enabled", True):
                continue
            logging.info(f"Source: {src['name']}")
            try:
                items, ok = crawl_source(fetcher, page, src)
            except Exception as e:
                logging.error(f"  {src['name']} failed: {e}")
                items, ok = [], False
            recs = [r for r in (make_record(src, it, today) for it in items) if r]
            logging.info(f"  {len(recs)} usable articles")
            for r in recs:
                logging.info(f"    {r['date']}  {r['title'][:80]}")
            if not ok:
                failed.append(src["name"])
            fresh += recs
        browser.close()

    if not fresh:
        logging.error("No articles from any source; leaving articles.json untouched.")
        return 4

    merged, new, changed, dropped = merge(existing, fresh, today, int(cfg.get("retention_days", 90)))
    logging.info(f"Retention setting in use: {cfg.get('retention_days', 90)} days")
    logging.info(f"Result: {len(merged)} articles ({new} new, {changed} updated, {dropped} past retention)"
                 + (f"; sources that failed: {', '.join(failed)}" if failed else ""))

    if args.dry_run:
        for a in merged[:15]:
            print(f"  [{a['category']}] {a['date']}  {a['title']}\n      {a['url']}")
        return 0

    text = json.dumps(merged, indent=2, ensure_ascii=False) + "\n"
    old_text = out_file.read_text(encoding="utf-8") if out_file.exists() else ""
    if text != old_text:
        out_file.write_text(text, encoding="utf-8", newline="\n")
        logging.info("articles.json updated")
    else:
        logging.info("articles.json unchanged")

    if use_git:
        try:
            if publish(repo, branch, f"Update articles: {new} new, {changed} updated ({today.isoformat()})"):
                logging.info("Pushed to GitHub")
            else:
                logging.info("Nothing to push")
        except Exception as e:
            logging.error(f"Push failed (articles.json is saved locally; the next run will retry): {e}")
            return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
