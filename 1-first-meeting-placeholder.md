# Accessible News Website — First Meeting Guide
### Project Kickoff Meeting

> **Meeting Goal:** Align the team on the project purpose, target users, core features, tech stack, and roles — producing a shared document to guide the next phase.

---

## 📋 Meeting Agenda Overview

| # | Topic | Duration |
|---|---|---|
| 1 | Define the Purpose | 10 min |
| 2 | User Stories & Use Cases | 15 min |
| 3 | Core Features Discussion | 15 min |
| 4 | Website Look & Feel | 10 min |
| 5 | Technical Decisions | 15 min |
| 6 | Roles & Responsibilities | 10 min |
| 7 | Roadmap & Timeline | 10 min |
| 8 | Open Discussion | 10 min |
| **Total** | | **~95 min** |

---

## 1. 🎯 Define the Purpose (10 min)

> Start with the **"Why"** before the "How".

### Questions to Answer

- Who exactly is our target user?
  - Fully blind users?
  - Low vision users?
  - Both?
- What problem are we solving for them?
- What is the exact scope of this app? Any limitations? 
- What makes us different from existing news sites?

---

## 2. 👤 User Stories & Use Cases (15 min)

> Get everyone thinking from the **user's perspective**.

### Example User Stories to Discuss

- *"As a blind user, I want to hear news articles read aloud so I can consume content without sight."*
- *"As a low-vision user, I want to increase font size easily so I can read comfortably."*
- *"As a user, I want to navigate the site using only my keyboard so I don't need a mouse."*
- *"As a user, I want to filter news by category so I can find topics I care about."*
- *"As a user, I want to bookmark articles for later so I can come back to them."*

### Action Item
> ✏️ **Ask everyone to write 2–3 user stories before the meeting.**

---

## 3. 🌐 Core Features Discussion (15 min)

> Decide what is **must-have vs nice-to-have** (MVP scope).

### Must-Have (MVP — Build First)

- [ ] Article listing and reading
- [ ] Text-to-Speech (TTS) playback
- [ ] High contrast mode and dark/light theme toggle
- [ ] Font size adjustment controls
- [ ] Full keyboard navigation support
- [ ] Category filtering

### Nice-to-Have (Build Later)

- [ ] User accounts and login
- [ ] Bookmarks / saved articles
- [ ] Newsletter / email digest
- [ ] Multi-language support
- [ ] Mobile app

> **MVP = Minimum Viable Product** — the simplest version that still delivers real value to users. Build, test, and validate before adding more.

---

## 4. 🎨 Website Look & Feel (10 min)

> Even for vision-impaired users, design and structure matter.

### Design Priorities to Discuss

- Color contrast strategy — dark mode and light mode
- Font choices — large, clean, and highly readable
- Layout simplicity — minimal clutter, clear hierarchy
- Consistent and predictable navigation structure

### Reference Sites to Review Before the Meeting

- [BBC Accessibility](https://www.bbc.co.uk/accessibility/) — strong accessible design example
- [AP News](https://apnews.com) — clean, minimal news layout
- [Gov.uk](https://www.gov.uk) — excellent accessibility standards

---

## 5. 🔧 Technical Decisions (15 min)

> Discuss and **vote** on the tech stack. Keep it simple to start.

| Decision | Options to Vote On |
|---|---|
| **Frontend** | Flask/Jinja2 (server-rendered) vs Next.js vs React |
| **Backend** | Python Flask / Django vs Node.js vs .NET Core |
| **Database** | SQLite (recommended — simple to start) |
| **Hosting** | Azure App Service vs Render vs Railway |
| **TTS Engine** | Web Speech API (free, browser-native) vs Amazon Polly |

### Recommended Starting Stack

```
Frontend  →  Flask + Jinja2 templates  (or Next.js if team prefers React)
Backend   →  Python Flask or Django
Database  →  SQLite
Hosting   →  Azure App Service or Render
TTS       →  Web Speech API (start free, upgrade later)
```

> 💡 **Tip:** Don't over-engineer at this stage. Start simple — complexity can be added later.

---

## 6. 👥 Roles & Responsibilities (10 min)

> Assign who does what so everyone leaves with clear ownership.

| Role | Responsibility | Assigned To |
|---|---|---|
| **Project Lead** | Overall coordination, deadlines, meeting facilitation | |
| **Frontend Developer** | UI, accessibility, templates, theme toggle | |
| **Backend Developer** | API, database, content management | |
| **Content Manager** | News sourcing, article posting, editorial | |
| **Accessibility Tester** | Screen reader testing, WCAG compliance checks | |

---

## 7. 📅 Roadmap & Timeline (10 min)

> Set realistic milestones everyone agrees on.

```
Week 1–2   →  Finalize requirements & design mockup
Week 3–4   →  Project setup, DB schema, basic pages
Week 5–6   →  Core features (TTS, navigation, articles)
Week 7–8   →  Accessibility testing & bug fixes
Week 9     →  Beta launch & user feedback
Week 10    →  Public launch
```

### Collaboration Tools to Agree On

- [ ] Version control: **GitHub**
- [ ] Communication: **Slack / Discord**
- [ ] Task tracking: **Notion / Trello / GitHub Issues**
- [ ] Meeting frequency going forward?

---

## 8. ❓ Open Discussion (10 min)

- Any concerns or blockers?
- Skills gaps — does anyone need support in a particular area?
- Any questions about accessibility requirements?
- Next meeting date and agenda?

---

## 📝 Before the Meeting — Ask Everyone To

1. Think of **2–3 user stories** from a visually impaired person's perspective
2. Browse **1–2 accessible websites** for design inspiration
3. Note their **preferred tech stack** choice and reason why

---

## 📄 Expected Output of This Meeting

By the end of Meeting 1, the team should produce a document covering:

- [ ] Confirmed target user group
- [ ] Agreed user stories list
- [ ] MVP feature list (must-have vs nice-to-have)
- [ ] Agreed tech stack
- [ ] Assigned roles and responsibilities
- [ ] Project timeline with milestones
- [ ] Collaboration tools selected

> This document becomes the **input for Meeting 2** — System Requirements & Technical Specification.

---

## 💬 Leader's Closing Message
열심히 합시다!
---

*Document prepared for Meeting 1 — Accessible News Website Project*
*Last updated: March 2026*