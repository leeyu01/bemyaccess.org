Accessible News Website: Project Definition of Done (DoD) Standards Report

1. Project Mission and Global Quality Mandate

The mission of the Accessible News Website is to provide a specialized, localized news portal specifically designed for the visually impaired community in Suffolk County, NY. This project addresses the isolation often faced by blind and low-vision individuals by delivering highly relevant local news and community events—specifically concerts and community gatherings—to support mental health and foster community engagement.

High-Level Success Criteria

* Accessibility First: Guaranteed compatibility for fully blind and low-vision users via strict WCAG 2.2 AAA standards.
* Zero-Login Policy: To remove all barriers to entry, the system shall require no accounts, passwords, or logins.
* Social Responsibility: Content curation is mandates to focus on community activity and events to combat social isolation.
* Frozen Scope: The MVP is strictly limited to three categories: Local News, News for the Disabled, and Weather.
* Economic Sustainability: Execution of a zero-cost infrastructure model utilizing the free tiers of Vercel and Supabase.

2. Universal Definition of Done (Project-Wide Standards)

A task is only considered "Done" when the code has been peer-reviewed and successfully deployed to the Vercel staging environment for verification.

* [ ] Scope Adherence: Implementation strictly follows the "Frozen Scope" policy; no unauthorized features or localization efforts.
* [ ] Language Policy: The portal is strictly English only.
* [ ] Keyboard Navigability: 100% of functionality must be accessible via keyboard-only tabbing (no mouse required).
* [ ] Mobile Responsiveness: Functional testing passed at 375px, 768px, and 1280px viewports.
* [ ] Code Quality: Review completed by at least one other team member; all linting passes (ESLint/Flake8).
* [ ] Data Integrity: Adherence to the configurable content retention policy (records are marked as is_active = false, never hard-deleted).

3. Role-Specific Standards: Project Lead

The Project Lead serves as the final authority on scope and coordination.

Required Deliverables

* Master System Requirements Document (SRD): Finalized and grounded in Meeting 2 outputs; serves as the absolute truth for development.
* Task Tracking: 100% of development tasks must be logged, assigned, and status-tracked via GitHub Issues.

Validation Steps

* Facilitation of weekly Wednesday team meetings.
* Mandatory sign-off on scope freezes to prevent feature creep.
* Verification that all role-specific documentation is sufficient for autonomous development via Claude Code.

4. Role-Specific Standards: Frontend Developer

The Frontend Developer is responsible for the UI/UX, accessibility templates, and browser-native interactive features.

Technical Deliverables

* Grid-style UI: Predictable, high-contrast layout for article listing and detail views.
* TTS Player: Browser-native Text-to-Speech (Web Speech API) with play/pause and speed controls.
* Theme Toggle: High-contrast, light, and dark mode switchers.
* Cookie-Based Bookmarks: Implementation of "Saved Articles" functionality utilizing browser cookies (no database-side user accounts).

Technical UI/UX Specification Table

Category	Requirement
Typography	Minimum 18px font size; minimum 1.6 line height.
Contrast	Minimum 7:1 ratio for all text and interactive elements (WCAG AAA).
Focus Indicators	Visible focus rings must meet the 7:1 contrast ratio against the background.
Layout	Maximum 800px content width; zero horizontal scrolling on all viewports.
Interactions	44x44px minimum clickable/tappable target size.

Validation Steps

* Weather Widget: Validate successful data fetching from the /api/weather (Open-meteo) endpoint using specific Suffolk County coordinates.
* Category Enforcement: Verify the UI only displays the three approved categories: Local News, News for the Disabled, and Weather.

5. Role-Specific Standards: Backend/DB Developer

The Backend/DB Developer is responsible for the Supabase (PostgreSQL) architecture and Next.js API Routes.

API Endpoint Readiness Checklist

* [ ] Standardized REST: Full implementation of GET/POST/PUT/DELETE for /api/articles.
* [ ] Admin Control: Implementation of PATCH /api/articles/[id]/toggle-active and POST /api/admin/crawl/trigger.
* [ ] Security: Protection of admin endpoints using a fixed API key in the request headers.
* [ ] Configurable Retention: The 90-day retention threshold must be controlled via a configurable environment variable (not hard-coded).
* [ ] Search: Successful handling of offset-based pagination and PostgreSQL full-text search (tsvector).

Validation Steps

* Confirm the is_active flag correctly handles content visibility for the frontend.
* Verify Supabase connectivity and successful execution of the 90-day retention logic (disabling rather than deleting).

6. Role-Specific Standards: Crawler & AI Developer

The Crawler & AI Developer is responsible for the Python-based data pipeline and content summarization.

Mandatory Source Coverage

The crawler must successfully aggregate data from the following 12 sources:

1. Newsday & Patch Suffolk
2. Helen Keller Services (HKSB)
3. SILO (Suffolk Independent Living Organization)
4. VIPS (Visually Impaired Persons of Long Island)
5. VISIONS (Services for the Blind and Visually Impaired)
6. Suffolk County Dept. of Disability Services
7. Eastern Suffolk BOCES
8. Stony Brook University (General Events, Medicine, and Health Professions calendars)
9. SuffolkNet (Suffolk Cooperative Library System)

AI Pipeline Requirements

* Semantic De-duplication: Mandatory check to prevent repeat stories from different sources based on content similarity, not just URL.
* Summarization: Generate concise article summaries stored in the articles.summary column.
* Retry Logic: Hard requirement of 3 attempts with 1-minute sleep intervals for unreachable sources.

Validation Steps

* Verify daily execution via Claude Co-worker or internal VM cron jobs.
* Validate the insertion of "cleaned" data (no HTML tags) into the Supabase articles table.

7. Role-Specific Standards: Accessibility Lead

As the final "Gatekeeper," the Accessibility Lead has the authority to reject any code that fails compliance.

WCAG 2.2 AAA Compliance Checklist

* [ ] Landmark Validation: Mandatory rejection of any component using div for structural regions where header, nav, main, or footer are appropriate.
* [ ] ARIA Integrity: Descriptive ARIA labels on all interactive elements; no exceptions.
* [ ] Heading Hierarchy: Strict no-skip hierarchy (H1 → H2 → H3).
* [ ] Focus Contrast: Focus indicators must be tested against the 7:1 contrast standard.

Mandatory Testing Procedures

* Manual Audits: Successful navigation and content consumption using screen readers (NVDA, VoiceOver, and TalkBack).
* Automated Scans: Zero "Critical" or "Serious" violations in axe DevTools or Lighthouse audits.

8. Merge and Deployment Readiness Protocol

Every component must pass this final check before being merged into the main branch.

Final Merge Checklist

Criteria	Requirement
Connectivity	Confirmed connection to Supabase and Open-meteo APIs.
Contrast	7:1 ratio verified for text and focus rings.
Navigation	100% keyboard operable with manual screen reader audit passed.
Scope	Strictly Local News, News for the Disabled, and Weather categories only.
Bookmarks	Cookie-based bookmarks verified as functional without login.
Deployment	Code successfully deployed to Vercel staging.


--------------------------------------------------------------------------------


Closing Mandate

*"After today, every member should be able to sit down with Claude Code and build their piece without needing to ask anyone else a question. Our documents need to be that clear and that detailed. If you can't write a clear prompt from your spec, the spec isn't done yet. 열심히 합시다! (Let's work hard!)"*​
