# BeMyAccess news crawler

Collects local news from the sources listed in `sources.json`, saves it to `articles.json` in the root of this repo, then commits and pushes that one file to GitHub. GitHub Pages republishes bemyaccess.org a minute or two later. The website (`index.html`) loads `articles.json`; if that file is missing it shows a few built-in sample articles.

```
News sources  ->  crawl.py (runs on a Windows PC)  ->  articles.json  ->  git push  ->  bemyaccess.org
```

## Files in this folder

| File | Purpose |
|---|---|
| `crawl.py` | The crawler |
| `sources.json` | Which sources to read, and settings |
| `run.bat` | Launcher used by Windows Task Scheduler |
| `.gitignore` | Keeps the Python environment and logs out of GitHub |

Created on your PC and never uploaded: `venv/` (Python environment), `crawl.log`, `run_output.log`.

## How it works

For each enabled source in `sources.json` the crawler:

1. Tries an RSS/Atom feed: the `feed` address if one is given, then common addresses (`/feed/`, `/feed`, `/rss`, `/rss.xml`, `/feed.xml`, `/atom.xml`).
2. If there is no feed, opens the source's `pages` in a real (headless) browser, collects links that look like articles, opens each one, and reads its title, date and text. **Pages without a publication date are skipped**, which filters out menus and service pages.
3. Skips a story it has already seen under another address (same title from the same source).
4. Keeps only a short excerpt (summary plus up to about 1,200 characters of text) with a link to the original. It does not copy full articles.
5. Merges the results into `articles.json`, newest first, and drops anything older than `retention_days`.
6. Commits and pushes `articles.json` only. It never commits any other file.

Good-citizen behavior: it follows each site's `robots.txt`, waits about 1.5 seconds between requests, identifies itself as `BeMyAccessCrawler`, and retries an unreachable source 3 times, 1 minute apart. If a source fails, the others still run. If every source fails, `articles.json` is left untouched. A watchdog stops the run after 20 minutes.

Crawled text is treated as untrusted: the website escapes all of it, so a headline containing HTML shows as plain text.

## One-time setup (Windows 11)

1. **Install Python** from python.org. Tick "Add python.exe to PATH".
2. **Install Git for Windows** from git-scm.com.
3. **Clone the repo to a local drive**, not a network drive (Git and Python environments misbehave on network shares):
   ```
   mkdir C:\projects
   cd C:\projects
   git clone https://github.com/leeyu01/bemyaccess.org.git
   ```
4. **Create the Python environment inside the crawler folder:**
   ```
   cd C:\projects\bemyaccess.org\crawler
   python -m venv venv
   venv\Scripts\python.exe -m pip install --upgrade pip
   venv\Scripts\python.exe -m pip install playwright
   venv\Scripts\python.exe -m playwright install chromium
   ```
5. **Sign in to GitHub once.** Make any push by hand (for example `git push` from the repo folder). A sign-in window opens and Windows remembers the login, which lets the scheduled job push without a password.
6. Check `repo_path` in `sources.json` matches where you cloned the repo.

## Running it

Run these from `C:\projects\bemyaccess.org\crawler`:

```
venv\Scripts\python.exe crawl.py --dry-run     # crawl and print results; writes and pushes nothing
venv\Scripts\python.exe crawl.py --no-push     # update articles.json locally; no Git
.\run.bat                                      # full run: pull, crawl, update, commit, push
```

**Always do a dry run after changing `sources.json`.** It lists every article found, with its date, before anything is published.

## Scheduling (Monday to Friday, 1:00 PM)

Run once in PowerShell:

```powershell
$dir = "C:\projects\bemyaccess.org\crawler"
$action   = New-ScheduledTaskAction -Execute "$dir\run.bat" -WorkingDirectory $dir
$trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 1:00PM
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Minutes 15)
Register-ScheduledTask -TaskName "BeMyAccessCrawler" -Action $action -Trigger $trigger -Settings $settings
```

The PC must be on and signed in at that time (a missed run happens as soon as the PC is back). Test it with `Start-ScheduledTask -TaskName "BeMyAccessCrawler"`, then read `run_output.log`. To remove it: `Unregister-ScheduledTask -TaskName "BeMyAccessCrawler"`.

## Settings in `sources.json`

Top level:

| Key | Meaning |
|---|---|
| `repo_path` | Where the website repo is cloned (use `\\` in paths) |
| `branch` | Branch to publish to (`main`) |
| `retention_days` | Articles older than this are removed from the site (currently 365) |

Each entry in `sources`:

| Key | Meaning |
|---|---|
| `name` | Shown on the site as the source |
| `category` | Must be exactly `Local News`, `News for the Disabled` or `Weather` |
| `pages` | One or more page addresses; the first is also used to find the site's feeds |
| `feed` | Optional RSS/Atom address, tried first |
| `max_articles` | Most articles to take from this source per run |
| `enabled` | `false` to switch a source off without deleting it |
| `link_include` / `link_exclude` | Optional regular expressions to narrow which links are treated as articles (page scraping only) |
| `link_selector` | Optional CSS selector for where article links live on the page |
| `require_date` | Default `true`; set `false` only if a site shows no dates (riskier) |

### Adding a source

1. Find the site's RSS feed if it has one (a feed gives the cleanest results). Otherwise find the page that lists its news.
2. Add an entry to `sources.json`.
3. Run `crawl.py --dry-run` and read the list. Publish only if the titles and dates are real news.
4. Commit and push `sources.json` (`git add crawler`, `git commit`, `git push`).

Currently enabled: Suffolk County Government (RSS feed), VISIONS Services for the Blind (page scraping), SILO (no news page found yet). Other disability organizations are listed but switched off until they are checked.

## What gets published

`articles.json` is a list of articles with these fields: `id`, `category`, `source`, `published` (display date), `date` (YYYY-MM-DD), `title`, `summary`, `body` (escaped paragraphs), `url` (original article) and `first_seen`.

Nothing reviews articles before they go live. Check `articles.json` or the site now and then, and consider asking source organizations for permission to republish excerpts.

## Troubleshooting

| What you see | What it means |
|---|---|
| `not a usable feed ... not well-formed` | The site answered with a web page instead of a feed. Normal; the crawler moves on |
| `no feed at ... (HTTP 404)` | The site has no feed at that address. Normal |
| `skipped (blocked by robots.txt)` | The site asks crawlers not to read that address. The crawler respects this; ask the site for permission or use a different source |
| `no article-like links found` | The page has no links the crawler recognizes. Point `pages` at the page that lists the news, or add `link_include` |
| `Ignored N articles older than ... days` | Those articles are past `retention_days`. Expected for old posts |
| `dubious ownership` from Git | The repo is on a network drive. Clone it to `C:\` instead |
| `Could not update the repo` | `git pull` failed; fix the repo state by hand, then rerun |
| `Push failed` | `articles.json` is saved locally; the next run retries. Check the GitHub sign-in |
| `No articles from any source` | Every source failed or was empty; `articles.json` was left unchanged |

Exit codes of `crawl.py`: `0` success, `2` configuration or repo problem, `3` repo could not be updated, `4` no articles found, `5` push failed, `9` stopped by the 20-minute watchdog.

## Not included

- **Weather.** Plan: a separate weather API, not crawling.
- **Event calendars** (Stony Brook, Suffolk Net): these are calendars, not news, and need different handling.
- **Summaries written by AI.** The summary is the source's own description.
