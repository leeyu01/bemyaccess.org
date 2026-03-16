# Accessible News Website — Second Meeting Guide
### System Requirements & Technical Specification

> **Meeting Goal:** Produce a detailed specification document that each developer can hand directly to Claude Code to build their assigned component independently.

---

## 📋 Meeting Agenda Overview

| # | Topic | Duration |
|---|---|---|
| 1 | Review First Meeting Output & Resolve Conflicts | 15 min |
| 2 | Database Design (Supabase/PostgreSQL) | 20 min |
| 3 | API Design (Next.js API Routes) | 15 min |
| 4 | Crawler & AI Pipeline Design | 15 min |
| 5 | Component Breakdown & Assignment | 20 min |
| 6 | UI/UX Specification | 10 min |
| 7 | Claude Code Strategy | 15 min |
| 8 | Document Assignments | 10 min |
| 9 | Definition of Done | 5 min |
| **Total** | | **~125 min** |

FYI, MVP - Minimum Viable Product. (최소기능)

---

## 1. 📄 Review First Meeting Output & Resolve Conflicts (15 min)

Start by aligning everyone on what was agreed in Meeting 1 and resolving conflicts in this template.

- [x] Review the summary document from Meeting 1
- [ ] Confirm the agreed MVP feature list:
  - **3 Categories**: Local News, News for the Disabled, Weather
  - **Keyword search** (MVP), semantic search (later)
  - **No-login policy** — lowest barrier to entry
  - **Bookmarks via cookies** — no user accounts
  - **TTS via Web Speech API** — browser-native, no paid services
- [ ] Confirm the agreed tech stack:
  - **Frontend**: Next.js (TypeScript) on **Vercel**
  - **Database**: **Supabase** (PostgreSQL)
  - **Crawlers**: **Claude cowork** with Python script
  - **AI/LM**: Filter, summarize, and de-duplicate articles
  - **TTS**: Web Speech API (browser-native) - for searching? go to menu? - NEED
- [ ] Confirm accessibility target: **WCAG 2.2 AAA**
- [ ] Confirm **90-day content retention** policy - confirmed. Just disable news, not hard delete, days should be configurable. 
- [ ] **Freeze the scope** — no new features after this meeting - confirmed

---

## 2. 🗄️ Database Design — Supabase/PostgreSQL (20 min)

> This is the most critical discussion — everything depends on it.
> **Decided in Meeting 1:** We are using **Supabase (PostgreSQL)**, not SQLite.

### Proposed Schema (PostgreSQL via Supabase)

```sql
-- Core Tables
CREATE TABLE categories (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(100) NOT NULL UNIQUE,
  description TEXT
);
-- Seed with: 'Local News', 'News for the Disabled', 'Weather'

CREATE TABLE articles (
  id            SERIAL PRIMARY KEY,
  title         VARCHAR(300) NOT NULL,
  content       TEXT NOT NULL,
  summary       TEXT,                    -- AI-generated summary for TTS
  source_url    VARCHAR(500),            -- Original RSS source link
  category_id   INTEGER REFERENCES categories(id),
  source_name   VARCHAR(200),            -- e.g., 'Newsday', 'Patch Suffolk'
  published_at  TIMESTAMPTZ NOT NULL,
  crawled_at    TIMESTAMPTZ DEFAULT NOW(),
  dedup_hash    VARCHAR(64),             -- SHA-256 hash for de-duplication
  is_active     BOOLEAN DEFAULT TRUE
);

CREATE TABLE tags (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE article_tags (
  article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
  tag_id     INTEGER REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (article_id, tag_id)
);

-- No users/bookmarks tables — bookmarks handled client-side via cookies (no-login policy)
```

** Maybe tags are not needed - since we use cookie. - need to confirm. 

### Decisions Already Made (Meeting 1)

- [x] **No user accounts** for MVP — no-login policy confirmed
- [x] **TTS generated on-the-fly** via Web Speech API (no stored audio)
- [x] **RSS feed import** via Python crawlers + AI summarization pipeline
- [x] No `author` field — replaced with `source_name` (crawled source)

### Questions to Decide

- [ ] 90-day retention cleanup: **Supabase scheduled function** vs **Python cron script**?
=> no deletion, just piles up, later cron script will delete them if needed. 
- [ ] Store AI summaries in `articles.summary` column or a separate `summaries` table?
=> articles.summary
- [ ] Index strategy for keyword search — PostgreSQL full-text search (`tsvector`) or Supabase search?
=> PostgreSQL full-text search
- [ ] Do we need Supabase Row-Level Security (RLS) for admin endpoints?
=> admin endpoints
---

## 3. 🔌 API Design — Next.js API Routes (15 min)

> A well-defined API allows frontend and backend developers to work in parallel.
> These will be **Next.js API routes** deployed on **Vercel**, connecting to **Supabase**.

### Agreed Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/articles/all` | List all articles (paginated), including active and inactive articles|
| GET | `/api/articles` | List all articles (paginated) only active articles|
| GET | `/api/articles/disabled` | List all articles (paginated), only inactive articles|
| GET | `/api/articles/[id]` | Single article detail |
| GET | `/api/categories` | List all categories |
| GET | `/api/articles?category={id}` | Filter by category |
| GET | `/api/articles?search={query}` | Keyword search articles |
| POST | `/api/articles` | Create article (admin only) |
| PUT | `/api/articles/[id]` | Update article (admin only) |
| DELETE | `/api/articles/[id]` | Delete article (admin only) |

### Questions to Decide

- [ ] Weather data: **separate API endpoint** (`/api/weather`) calling a weather API, or crawled into articles?
=>weather API
- [ ] Admin auth: **API key in header** vs **Supabase RLS** vs **simple password**?
=> API key in header (fixed)
- [ ] Pagination: **cursor-based** (better performance) or **offset-based** (simpler)?
=> offset-based

### Response Format (agree on standard shape)

```json
{
  "status": "success",
  "data": { },
  "pagination": { "page": 1, "totalPages": 10, "totalItems": 95 },
  "message": ""
}
```

---

## 4. 🐍 Crawler & AI Pipeline Design (15 min)

> **New section** — this was decided in Meeting 1 but not yet specified.
1. Python scripts crawls to get news from given source news websites
2. AI calls api to whether they are already in the DB
  1. if not, publish news through api


### Python Crawler Architecture

| Decision | Details |
|---|---|
| **Language** | Python |
| **RSS Sources** | Newsday, Patch Suffolk, local government feeds (list TBD) |
| **Frequency** | Daily cron job |
| **Hosting** | Team's internal VMs (zero cost) |
| **Output** | Insert cleaned articles into Supabase |

#### source websites
this websites should be configurable. 
- https://www.helenkeller.org/hksb⁠
- https://www.siloinc.org⁠
- http://www.vips-li.org⁠
- https://visionsvcb.org⁠
- https://www.suffolkcountyny.gov/Departments/Disability-Services⁠
- https://www.esboces.org⁠
- https://www.stonybrook.edu/events⁠
- https://calendar.stonybrook.edu⁠
- https://healthprofessions.stonybrookmedicine.edu/calendars⁠
- https://www.suffolknet.org/events⁠


### AI/LM Pipeline (runs after each crawl)

```
RSS Feed → Python Crawler → Raw Articles
                                  │
                                  ▼
                         AI/LM Processing:
                         1. Filter relevance (Suffolk County)
                         2. Summarize for TTS-friendly reading
                         3. De-duplicate (SHA-256 hash + semantic similarity)
                         4. Categorize into: Local News / Disabled / Weather
                                  │
                                  ▼
                         Insert into Supabase
```

### Questions to Decide

- [ ] Which LM to use? **Local Ollama** (see `ollama_settings` in repo) vs **cloud API** (OpenAI, etc.)?
=> Claude cowork
- [ ] De-duplication: **hash-only** (exact match) or **hash + semantic similarity** (fuzzy match)?
=> semantic search (summary)
- [ ] How many RSS sources to support in MVP? Start with 3–5?
=> described in previous section
- [ ] Error handling: what happens when a source is unreachable?
=> Retry 3 times (sleep time 1 min) then still not reachable just skip

---

## 5. 🧩 Component Breakdown & Assignment (20 min)

> Each component maps to one Claude Code session.
> **Tech stack:** Next.js (TypeScript) + Supabase + Web Speech API

| Component | Description | Assigned To | Status |
|---|---|---|---|
| **Navigation** | Skip links, keyboard nav, ARIA landmarks (reference existing `index.html`) | | ⬜ Unassigned |
| **Article List Page** | Article cards, category filter (3 categories), search bar | | ⬜ Unassigned |
| **Article Detail Page** | Full content, font size controls, TTS trigger button | | ⬜ Unassigned |
| **TTS Player** | Web Speech API: play/pause/speed control, read aloud | | ⬜ Unassigned |
| **Theme Toggle** | Light / dark / high-contrast mode switcher | | ⬜ Unassigned |
| **Search Component** | Keyword search with accessible results display | | ⬜ Unassigned |
| **Weather Widget** | Suffolk County weather display | | ⬜ Unassigned |
| **Admin Panel** | CRUD for articles (can defer to phase 2) | | ⬜ Unassigned |
| **Supabase Layer** | PostgreSQL schema, Supabase client, query functions | | ⬜ Unassigned |
| **Python Crawler** | RSS aggregation + AI summarization pipeline | | ⬜ Unassigned |
| **Accessibility Audit** | WCAG AAA checks, screen reader testing | | ⬜ All Members |

All jobs will be assigned to Claude code
Todo: In order to assign each job, what prompts/docs are needed?

---

## 6. 🎨 UI/UX Specification (10 min)

> Design rules must be agreed here so all components look and feel consistent.

Each member should provide example pages. 

### Typography

| Property | Value |
|---|---|
| Base font size | Minimum `18px` |
| Font family | `Inter`, `Open Sans`, or system-ui |
| Line height | Minimum `1.6` |
| Font weight (body) | `400` |
| Font weight (headings) | `700` |

### Color Palette

| Token | Light Mode | Dark Mode |
|---|---|---|
| Background | `#FFFFFF` | `#121212` |
| Surface | `#F5F5F5` | `#1E1E1E` |
| Primary Text | `#1A1A1A` | `#F5F5F5` |
| Secondary Text | `#4A4A4A` | `#AAAAAA` |
| Accent / Link | `#0057B8` | `#4FA3FF` |
| Focus Ring | `#FF6B00` | `#FF6B00` |

> **Contrast requirement:** Minimum **7:1** ratio (WCAG AAA) — upgraded from AA per Meeting 1 decision

### Layout Rules

- Max content width: `800px` (readable line length)
- No horizontal scrolling on any viewport
- Minimum clickable/tappable target size: `44 x 44px`
- Consistent heading hierarchy: `h1 → h2 → h3` (never skip levels)
- All interactive elements must have a **visible focus indicator**
- Keyboard shortcuts: reference `brainstorming/functioning_shortcuts.md` for agreed scheme

---

## 7. 🤖 Claude Code Strategy (15 min)

> How our team will use Claude Code effectively to build each component.
TODO: probably need to rebuild below structures. 

### Folder Structure (agree before coding)

```
/project
  /src
    /app                    # Next.js App Router
      layout.tsx
      page.tsx
      /articles
        page.tsx
        /[id]
          page.tsx
      /api
        /articles
          route.ts
          /[id]
            route.ts
        /categories
          route.ts
    /components
      Navbar.tsx
      ArticleCard.tsx
      ArticleList.tsx
      ArticleDetail.tsx
      TTSPlayer.tsx
      ThemeToggle.tsx
      SearchBar.tsx
      WeatherWidget.tsx
    /lib
      supabase.ts           # Supabase client config
      types.ts              # Shared TypeScript interfaces
    /styles
      globals.css
  /crawler                  # Python crawler (independent)
    crawler.py
    ai_pipeline.py
    requirements.txt
    config.yaml
  /database
    schema.sql
    seed_data.sql
  /tests
    accessibility_checklist.md
  /public
    favicon.ico
```

### Coding Standards

- **Frontend**: Next.js (TypeScript) with App Router
- **Backend API**: Next.js API Routes (TypeScript)
- **Database**: Supabase (PostgreSQL) via `@supabase/supabase-js`
- **Crawler**: Python 3.x with `feedparser`, `requests`, `psycopg2` (or Supabase Python client)
- **Linting**: `ESLint` (TypeScript), `flake8` (Python)
- **Styling**: Tailwind CSS utilities only — no inline styles) and ShadCn
- **Hosting**: Vercel (frontend + API) / Internal VMs (crawler)

### Writing Effective Claude Code Prompts

Each member's prompt to Claude Code should include:

```
1. Component name and its purpose
2. Tech stack: Next.js + TypeScript + Supabase (or Python for crawler)
3. Input/output (props, API endpoints it calls)
4. Agreed database schema (paste the PostgreSQL schema)
5. Accessibility requirements (ARIA roles, keyboard nav, WCAG AAA)
6. UI spec (colors, font sizes, layout rules from this doc)
7. Reference files: sample_usecases.md, functioning_shortcuts.md
8. Definition of Done checklist
```

---

## 8. 📝 Document Assignments (10 min)

Each member leaves with a writing task to complete **before coding begins**.

| Member | Document to Produce |
|---|---|
| Project Lead | Master system requirements document |
| Frontend Developers | UI component spec per assigned component (Next.js/TypeScript) |
| Backend / DB Developer | API routes spec + Supabase schema doc |
| Crawler Developer | Python crawler spec + AI pipeline design doc |
| Accessibility Lead | WCAG AAA checklist per component |

> These completed documents become the **Claude Code prompts** in the next phase.

---

## 9. ✅ Definition of Done (5 min)

Agree on what "finished" means for every component before it is merged.

- [ ] Passes **WCAG 2.2 AAA** audit (axe DevTools or Lighthouse)
- [ ] Fully navigable using **keyboard only**
- [ ] Tested with a screen reader (NVDA / VoiceOver / TalkBack)
- [ ] Mobile responsive (tested at 375px, 768px, 1280px)
- [ ] All images have descriptive `alt` text
- [ ] No missing ARIA labels on interactive elements
- [ ] Minimum **7:1** contrast ratio for all text
- [ ] Code reviewed by at least **one other team member**
- [ ] Successfully connects to Supabase via agreed API routes
- [ ] Validated against relevant use cases in `sample_usecases.md`

---

## 📅 What Comes After Meeting 2

```
Meeting 2 Output (this document, filled in)
        │
        ▼
Each member writes their detailed component spec
        │
        ▼
Feed spec into Claude Code → build component
        │
        ▼
Meeting 3 → Integration, testing & review session
```

---

## 💬 Leader's Closing Message

> *"After today, every member should be able to sit down with Claude Code and build their piece without needing to ask anyone else a question. Our documents need to be that clear and that detailed. If you can't write a clear prompt from your spec, the spec isn't done yet."*

---

*Document prepared for Meeting 2 — Accessible News Website Project*
*Last updated: March 2026*
