# Career Compass — Data Logbook

This logbook records key decisions, data sources, and progress made throughout the
development of Career Compass, for the Researchathon (Aug 28-29, 2026) submission.

---

## Entry 1 — July 26, 2026

**Project structure set up.**

Decided on stack: HTML/CSS/JS frontend + Python (Flask) backend, instead of Streamlit
or React. Reasoning: Streamlit's UI ceiling was too low for the polish we wanted;
React added unnecessary setup overhead given the 5-week deadline. Flask + custom
frontend gives full design control while staying simple enough to build and explain
quickly.

**Data source decisions:**
- O*NET Web Services (US Dept of Labor) — approved for use, will be credited per
  their terms. Used for occupation/skills taxonomy (universal, not country-specific).
- World Bank Open Data API — free, real API, used for Pakistan macro labor trends.
- Pakistan Bureau of Statistics (PBS) labour force survey reports — no public API,
  so key figures will be manually extracted and cited, not pulled live.
- Decision: NOT using the Kaggle "Pakistan Job Market Intelligence Dataset" as a
  primary source since it is explicitly synthetic/simulated data. May use it only
  for internal pipeline testing, clearly disclosed as such if referenced anywhere.

**Known limitation (to state in the paper):** granular, real-time Pakistani job
market data is not available via public API. This is a real constraint of building
for the Pakistani market and will be documented transparently in the Discussion/
Limitations section rather than glossed over.

**Brand identity finalized:** navy + brass "naval crest" visual direction — chosen
over a softer vintage-cartography look for a stronger, more authoritative feel.
Logo has a full crest version (display board / hero use) and a circular badge
version (web header use).

**Landing page + questionnaire flow built.** Landing page introduces the product
and links to a step-by-step questionnaire (one question per screen, progress bar).

**Questionnaire designed with 15 questions**, grouped into: Interests, Background,
Work Style, Strengths, Priorities, Constraints, Preferences. Includes both hard
filters (budget, location, years willing to study) and soft matching signals
(interests, strengths, work style, ranked priorities) — the hard filters will be
used to narrow candidates before AI/O*NET matching runs, the soft signals will
feed the similarity scoring.

All routes tested and confirmed working (Flask test client, all 200 responses).
Answer submission currently stubbed (logs to console) — next step is connecting
this to the O*NET matching + AI personalization backend.

## Entry 2 — July 26, 2026 (continued)

**Full UI redesign using Google Stitch.** User felt the initial hand-built CSS was
too plain, so we used Stitch (Google's AI UI design tool) to generate a "navy +
gold executive" design system (Tailwind CSS based), then integrated it into the
existing Flask app — kept all working functionality (15-question dynamic engine,
progress tracking, answer state) and rebuilt the visual layer around it.

Decisions made during integration:
- Replaced Stitch's temporary Google-hosted logo image URLs with our own logo asset,
  since temporary URLs would break in the final deployed app.
- Deliberately removed a Stitch-generated "stats" section (e.g. "10,000+ Future
  Leaders", "98% Accuracy Rate") from the landing page — these were placeholder
  marketing numbers with no real backing data. Keeping them would have directly
  contradicted this project's core principle of not presenting invented statistics
  as real, so they were cut rather than kept for visual effect.
- Rebuilt Stitch's static single-example question into a fully dynamic renderer
  driven by our real 15-question dataset (questions.js), supporting all question
  types (multi-select, single-select, text, dropdown, drag-to-rank).

## Entry 3 — July 26, 2026 (continued)

**Visual polish pass.** User felt the first integrated version still looked flat.
Added: a global subtle grid-pattern + soft glow background (applied site-wide via
base.html), a two-column hero with a sample preview card (clearly labeled
"Illustrative preview" to avoid implying it's real user data), and color variety
across the three "How It Works" cards (gold/blue/green gradient icons instead of
uniform brass) to break visual monotony while staying within the established
navy/gold identity.

## Entry 4 — July 26, 2026 (continued)

**Animated background system.** User wanted a richer, more "AI product" feel
(referencing polished AI-builder aesthetics) rather than a static flat background.
Added: slowly drifting animated gradient-mesh orbs (gold/blue/green, blurred,
looping float animation), a large faint slow-rotating compass motif tying back to
the brand identity, a radially-masked grid (fades at edges instead of hard-cutting),
and a subtle grain/noise texture overlay for a less "flat vector" feel. All effects
implemented in pure CSS/SVG (no extra libraries) to keep the app lightweight and
avoid new dependencies this close to the deadline.


## Entry 5 — July 27, 2026

**Data source revision — Glassdoor rejected.** User suggested using Glassdoor for
salary estimation. Investigated and found Glassdoor's public developer API was shut
down in 2022 (enterprise-only now); the only available workarounds are web scraping,
which violates Glassdoor's Terms of Service. Decision: do NOT use Glassdoor, since
scraping against ToS is a real credibility/legal risk for a research submission.

**Replacement: ILOSTAT** (International Labour Organization statistics database) —
publishes a legitimate, citable Pakistan labour market profile (wages, employment,
working conditions) based on Pakistan's own Labour Force Survey, with structured
data tools for programmatic access. This replaces Glassdoor in the data stack.

Updated data stack: O*NET (occupation/skills taxonomy) + World Bank API (macro
trends) + ILOSTAT (Pakistan-specific wages) + PBS reports (manually cited).

**Navigation expanded.** Added four new nav items: University Comparisons, About
Our Data (transparency page), Saved Career Options, and AI Advisor. University
Comparisons, Saved Options, and AI Advisor are currently "coming soon" stubs since
they depend on the O*NET/AI matching backend not yet built. AI Advisor is planned
to answer using matched real data rather than freeform AI advice, to stay consistent
with the project's no-fabrication principle.

**Navbar visual pass** — added icons per nav item, animated gradient underline on
hover, backdrop blur, and a persistent "Start Now" CTA button for more visual energy.

## Entry 6 — July 27, 2026 (continued)

**Logo redesigned (3rd iteration).** User didn't like the naval-crest version.
New design: a glowing gold ring with tick marks, a blue glowing compass needle
(instead of all-gold), cleaner and more icon-like — works better at small sizes
(nav bar, favicon) than the crest did.

**Background animation made clearly visible.** Previous version was too subtle
(opacity 0.05). Increased compass motif opacity to 0.22, added a second smaller
counter-rotating blue-dominant compass in the opposite corner, and strengthened
the gold/blue gradient orb glows. Background now visibly reflects the brand
(gold + blue compass) rather than being an almost-invisible texture.

**Sample Roadmap page built.** Since the real AI/O*NET matching backend isn't
built yet, created a "/sample-roadmap" page so the full results experience can
be previewed end-to-end. Includes an animated SVG growth-outlook chart (line +
area chart, 2026-2036). Clearly labeled "Sample Analysis" and "illustrative"
throughout — this is a placeholder shape, not real data, and will be rebuilt
using live O*NET Bright Outlook / ILOSTAT projections once that pipeline exists.
Added a "View Sample Roadmap" secondary button on the landing page hero.

## Entry 7 — July 27, 2026 (continued)

**Loading screen added.** After finishing the questionnaire, a full-screen loading
overlay now appears — spinning glowing compass logo, pulsing glow behind it, an
animated progress bar, and cycling status messages ("Analyzing your responses...",
"Matching real occupational data...", etc.) before redirecting to the roadmap.

Currently implemented as a fixed 4.2-second timer (simulated) since the real
backend isn't built yet. Marked clearly in code comments: once /generate-report
(O*NET + AI + PDF pipeline) exists, this will become a real fetch() call, and the
redirect will happen when the actual response returns instead of on a timer.

## Entry 8 — July 28, 2026

**Real backend pipeline built.** Implemented the actual O*NET + Gemini pipeline:

- `backend/onet_client.py` — handles all O*NET Web Services calls (HTTP Basic
  Auth per O*NET's API docs). Functions: search_occupations(), get_occupation_
  overview(), get_occupation_skills(), get_occupation_knowledge(), get_job_
  outlook(), and get_full_occupation_profile() which bundles all of the above
  for one occupation.
- `backend/ai_engine.py` — sends the student's answers PLUS the real O*NET data
  to Gemini (gemini-2.0-flash via direct REST call, no extra SDK dependency),
  with an explicit prompt instruction: base the response only on the provided
  real data, do not invent statistics. Requests JSON-only output and validates
  it parses correctly before returning it, raising a clear error instead of
  passing broken data downstream if the model doesn't comply.
- New Flask route `/generate-report` (POST) ties it together: picks a search
  keyword from the student's answers (dream field first, else first selected
  interest — a simple heuristic for now; real similarity-scoring matching
  across all answers is a planned upgrade once this pipeline is confirmed
  stable), searches O*NET, pulls the full occupation profile, sends it to
  Gemini, returns structured JSON.
- Frontend (`main.js`) updated: submitAnswers() now makes a real fetch() call
  to /generate-report instead of a simulated timer. On success, stores the
  report in sessionStorage for the results page to render. On failure (e.g.
  missing API keys, network error), shows a clear message and falls back to
  the sample roadmap page rather than leaving the student stuck.

**Security decision:** API keys are never hardcoded or shared in chat/logs —
loaded via a local .env file (see .env.example) using python-dotenv, which is
standard practice and keeps credentials private per-developer.

**Tested:** confirmed the app still runs correctly end-to-end, and that
/generate-report fails gracefully with a clear error message when API keys
aren't configured yet (rather than crashing), so the rest of the app remains
usable even before real keys are added.

## Entry 9 — July 28, 2026 (continued)

**Fixed the missing pieces user found while testing.** The questionnaire and
/generate-report backend worked, but nothing downstream was actually connected —
the results page still showed hardcoded sample content, and PDF generation
hadn't been built at all. Fixed both:

- `backend/pdf_generator.py` — new module, builds the actual PDF using reportlab
  (report layout) + matplotlib (outlook chart, rendered to an in-memory image,
  no temp files on disk). Includes required O*NET attribution in the footer.
- New route `/download-report` (POST) — accepts report JSON, returns a
  downloadable PDF via Flask's send_file.
- `sample_roadmap.html` made dynamic — on page load, checks sessionStorage for
  a real generated report (set by main.js after /generate-report succeeds). If
  found: swaps the "Sample Analysis" badge for "Your Personalized Report",
  fills in the real recommended path / explanation / skills, and reveals a
  working "Download PDF Report" button. If not found (e.g. visited directly),
  falls back to showing the original illustrative sample content — so the page
  never breaks either way.

Tested end-to-end with a mock report (since real O*NET/Gemini keys require the
user's local .env): confirmed PDF generation produces a valid, correctly
formatted PDF.

## Entry 10 — July 28, 2026 (continued)

**Adapted React component code to our stack.** User found two React components
(ShimmerText using Framer Motion, and a background gradient/grid snippet) from
a shadcn/Next.js component library site. Since our project is Flask + plain
HTML/CSS/JS (not React/Next/shadcn/TypeScript), direct copy-paste wasn't
possible — instead, rebuilt both effects in plain CSS with equivalent visual
results, so no new frameworks or build tooling needed:

- Shimmer text: pure CSS `background-clip: text` + keyframe animation,
  applied to the hero's key phrase ("actually fits you").
- Background spotlight: a radial-gradient glow layered behind the existing
  grid pattern, adapted from their `radial-gradient(circle...)` technique.

Noted for future reference: any further template/component code the user
brings should be checked for framework compatibility before integration —
React/Next-based snippets need adaptation, plain HTML/CSS/JS or Tailwind-based
ones integrate directly.

## Entry 11 — July 28, 2026 (continued)

**Hero/logo overhaul from a detailed design brief.** User provided a full
design brief (navy #0B132B / gold #D4AF37 theme, floating 3D compass graphic,
typewriter headline effect, sharp geometric logo avoiding generic "AI slop"
icons, glow-on-hover polish). Implemented with adaptations to keep content
real to Career Compass rather than the brief's generic placeholder text/nav:

- New logo: hexagonal faceted frame (not a plain circle), angular diamond-
  point compass star instead of a soft needle — sharper, more geometric,
  matches the "sophisticated emblem, not cliché icon" instruction.
- Hero: added a larger floating compass graphic with a CSS-only pseudo-3D
  effect (translateY + rotateX/rotateY oscillation via keyframes — no
  WebGL/Three.js dependency needed for this).
- Typewriter effect: cycles through real Career Compass value props
  ("Discover your ideal career path.", "Match your interests to real data.",
  etc.) — substituted for the brief's generic demo text, which didn't apply
  to this product.
- Nav links kept as our real pages (Assessment, University Comparisons, Our
  Data, Saved Options, AI Advisor) rather than the brief's generic Home/
  Features/Showcase/Contact, since those don't correspond to anything in
  this app.
- Added stronger gold glow-on-hover to CTA buttons per the brief's request.

Note: brief also requested this be built as a standalone single-file HTML
page. Kept it integrated into the existing Flask/Jinja template structure
instead, since a standalone file would abandon all working functionality
(real routes, backend integration, shared base template) built so far.

## Entry 12 — July 28, 2026 (continued)

**Removed sample preview card, background rebuilt to match sent snippet exactly.**

1. Deleted the "Sample Preview" mock analysis card from the hero (fake "Top
   Match: Software Engineering", progress bars, stats) — user felt it was
   unnecessary clutter and wanted the compass graphic to be the visual focus
   instead. Compass is now larger, centered, and stands alone in the hero.

2. Rebuilt the global background to precisely match the CSS technique from
   the background-gradient snippet the user originally provided — plain CSS
   `linear-gradient` grid lines (not an SVG pattern) masked with a
   `radial-gradient`, plus a `radial-gradient` spotlight glow — rather than
   our earlier looser SVG-pattern + multiple-blurred-orbs interpretation.
   Colors adapted to gold (#D4AF37) instead of the snippet's original sky-blue
   to stay on-brand. Compass motifs kept but reduced to subtle secondary
   accents rather than the dominant background element.

## Entry 13 — July 29, 2026

**Removed background compass motifs.** Removed the two faint rotating compass
SVGs from the global background (base.html) — background now shows only the
grid pattern, radial spotlight glow, and grain texture. The large floating
compass in the hero section remains as the single compass visual on the site,
avoiding visual clutter/competition between multiple compass graphics.

## Entry 14 — July 29, 2026 (continued)

**Found and fixed the real cause of the O*NET 401 error.** User confirmed their
credentials were correct, which ruled out a typo. Investigated further and found
O*NET migrated to API v2 since our original integration was built — v2 uses a
completely different authentication method (a single API key via an X-API-Key
header, hosted at api-v2.onetcenter.org) instead of the old v1.9 system (HTTP
Basic Auth with username/password, hosted at services.onetcenter.org/v1.9).
Since the user's account was approved recently (after this migration), it was
only provisioned for v2 — meaning correct v1.9-style credentials wouldn't have
existed at all, explaining the 401 regardless of what was entered.

Rewrote `backend/onet_client.py` to use v2 (new base URL, X-API-Key header).
Updated `.env.example` to require a single `ONET_API_KEY` instead of
`ONET_USERNAME`/`ONET_PASSWORD`. This is a good example of why checking official
docs before debugging paid off — the issue looked like a credentials problem but
was actually an API version mismatch.

## Entry 15 — July 29, 2026 (continued)

**Fixed a real O*NET search bug + built the internships/courses/companies feature.**

Bug fix: search_occupations() was reading the wrong JSON key. O*NET's search
response uses "career" as the results array key, but the code checked for
"occupation" — meaning every single search silently returned zero results,
regardless of the keyword. This fully explains the "No O*NET matches found"
error the user hit, and was unrelated to the earlier auth issue.

New feature — real companies + real courses, requested by user:
- `backend/pakistan_resources.py` — new curated reference file. Contains
  real, well-known Pakistani companies grouped by broad career field
  (Software/Technology, Business/Finance, Engineering, Healthcare/Biology,
  Arts/Design/Media), and a skill -> real course mapping (Coursera, edX,
  freeCodeCamp, Skillshare — mixing free and paid, all real providers).
  Explicitly documented WHY this is curated rather than API-sourced: no
  live "who's hiring interns" API exists, and letting the AI freely name
  companies risks hallucinating fake-but-plausible names, which would be a
  serious credibility problem for a research submission.
- Added guess_field() — simple keyword matching to map an O*NET occupation
  title to one of our curated buckets.
- ai_engine.py updated: prompt now includes the curated companies/courses
  as real data, with explicit instruction to use ONLY the provided names,
  never invent additional ones. Report schema expanded with
  recommended_companies and recommended_courses fields.
- pdf_generator.py updated to render both new sections, with a note in the
  companies section clarifying it's a reference list, not live job openings.

Maintenance note logged in the file itself: this curated list needs periodic
human review since companies close/merge/stop offering internships — this
limitation should be disclosed in the paper's Methods/Limitations section.

Tested end-to-end with mock data: field-guessing, company matching, course
matching, and PDF generation with the new sections all confirmed working.

## Entry 16 — July 29, 2026 (continued)

**Found and fixed the real crash cause.** User kept getting "Couldn't reach the
server" — a network-level failure, meaning the Flask process itself was dying,
not just returning an error response. Root cause: the /generate-report route
only caught `RuntimeError`, but errors from O*NET (`requests.exceptions.
HTTPError`) or other failure types were NOT RuntimeError instances, so they
went uncaught. Combined with Flask's debug auto-reloader (which restarts the
whole server if it detects file changes, including new __pycache__ files
created on first import of new modules), an uncaught exception during a
slow request could coincide with an unexpected restart, killing the
in-flight request and producing exactly this symptom in the browser.

Fixes applied:
- Broadened exception handling in both /generate-report and /download-report
  to catch ALL exception types, not just RuntimeError — the server can no
  longer crash from an unexpected error type; it always returns a clean
  JSON error instead.
- Added traceback logging — every error now prints its full traceback to
  the terminal running the server, so the real cause is always visible
  going forward instead of a vague "no result."
- Disabled the auto-reloader (use_reloader=False) — removes the mid-request
  restart risk entirely. Documented that code changes now require manually
  restarting the server (Ctrl+C, then "python app.py" again).

Tested: confirmed the server survives an error condition (missing API keys)
without crashing, returns a clean structured error, and remains responsive
to subsequent requests.

## Entry 17 — July 29, 2026 (continued)

**Fixed the "'list' object has no attribute 'get'" crash — real progress marker:
this error occurred AFTER O*NET auth and search both succeeded, meaning those
earlier fixes are confirmed working.**

Root cause: two compounding bugs in how skills/knowledge responses were parsed.
1. Wrong nesting assumed — O*NET's actual response shape nests elements inside
   a "group" array (`{"group": [{"element": [...]}]}`), but the code was
   checking for "element" at the top level directly, which doesn't exist there.
2. No defensive handling — for occupations with no collected skills/knowledge
   data, O*NET can return an empty list `[]` instead of a dict, and calling
   .get() on that list crashes.

Fix: added _extract_elements() helper in onet_client.py that correctly walks
the real group -> element nesting AND checks isinstance(data, dict) first,
safely returning an empty list for the no-data case instead of crashing.
Applied to both get_occupation_skills() and get_occupation_knowledge().

Tested against three cases: normal nested data, the empty-list no-data case,
and a dict missing the group key entirely — all now return correctly instead
of crashing.

## Entry 18 — July 29, 2026 (continued)

**403 error resolved by user generating a fresh O*NET API key** — confirms
account/key permission was the actual cause, not our code.

**Improved O*NET keyword matching with fallback candidates.** The "no matches
for businessmen" case revealed a real limitation: O*NET's search matches
structured occupation titles, not everyday/colloquial phrasing. Replaced the
single-keyword pick_onet_keyword() with pick_onet_keyword_candidates(), which
builds an ordered list of fallback terms: the raw answer, common suffix-
stripped versions ("businessmen" -> "business"), each individual word in a
multi-word answer, the student's selected interests, then a general fallback.
search_with_fallback() tries each in order until one returns results. Tested
against the exact failing case — "business" now appears as a working fallback
candidate.

**Questionnaire wording fix (user-approved "option 2" from the education-level
loophole discussion).** Reworded dream_field and dream_university questions
to work naturally whether the student is pre-university or already graduated
— e.g. "A university you're aiming for — or one you've already attended?"
instead of assuming only a future goal. Full conditional/branching logic
(skipping irrelevant questions entirely based on education level) noted as a
future improvement if time allows, deprioritized in favor of backend stability
given the deadline.

## Entry 19 — July 29, 2026 (continued)

**Major milestone: O*NET pipeline fully confirmed working end-to-end.** The
429 error from Gemini happened AFTER O*NET search, skills, knowledge, and
outlook data all succeeded — meaning the entire O*NET integration is now
confirmed functional in a real run, not just isolated tests.

**Security incident + fix:** user's Gemini API key was visible in a screenshot
(Gemini's own error message included it in a URL). Advised immediate key
rotation (delete old key, generate new one in Google AI Studio) — user
confirmed this was done. Also fixed the code so this can't happen again:
the API key is now passed via `params=` instead of being embedded directly
in the URL string, and any HTTPError message has the key stripped out
(replaced with "***") before being shown to the user or logged.

**Added retry-with-backoff for Gemini rate limits.** 429 errors are expected
and normal on the free tier, especially during rapid testing (which is
exactly what's been happening during debugging today). generate_report_content()
now retries up to 3 times with a 15-second delay between attempts before
giving up, instead of failing immediately on the first rate limit hit.
Updated the loading screen's message list to include a reassuring "still
working, can take up to a minute" message so a retry-triggered wait doesn't
look like the app is frozen or broken.

## Entry 20 — July 29, 2026 (continued)

**Added Gemini model fallback chain.** Since retries alone weren't enough when
the free-tier quota was genuinely exhausted (not just a transient per-minute
limit), added a second layer: MODEL_CHAIN = ["gemini-2.0-flash",
"gemini-2.0-flash-lite"]. Each model gets its own retry attempts (2 tries,
15s apart); if a model is still rate-limited after that, the code
automatically falls back to the next model in the chain, since Flash and
Flash-Lite have separate free-tier quotas — a genuine fallback, not just
repeating the same limited request.

Tested with a mock that simulates the first model always returning 429 and
the second succeeding — confirmed the chain correctly retries model 1,
then switches to model 2 and returns a valid result, rather than failing
outright.

## Entry 21 — July 29, 2026 (continued)

**Added a non-AI template report generator, decoupling testing from Gemini's
rate limits.** User's idea: build/test the rest of the pipeline now, add
Gemini's polish back once quota is available. Implemented:

- `ai_engine.generate_template_report()` — builds the exact same JSON schema
  as the Gemini version, but using plain string templates instead of an AI
  call. Every value still comes from real data (O*NET occupation title/skills/
  outlook, curated companies/courses) — no invented content, same principle
  as the AI path, just without AI-generated prose.
- New `.env` toggle: `USE_GEMINI=true/false`. When false, skips Gemini
  entirely. When true (default) but Gemini fails at runtime (rate limit,
  etc.), automatically falls back to the template report instead of failing
  the whole request — the "sample roadmap fallback" behavior is now only a
  last resort, not the first response to any Gemini hiccup.

Tested full pipeline end-to-end with mocked O*NET responses and USE_GEMINI=
false: search -> occupation profile -> companies/courses matching -> template
report -> PDF generation, all confirmed working without any Gemini API call.
This means the rest of the app (results page, University Comparisons,
further features) can now be built and tested independent of Gemini's
free-tier availability.

## Entry 22 — July 29, 2026 (continued)

**Fixed the missing companies/courses display gap the user found.** Confirmed
there is only ONE pipeline (not separate ones) — companies/courses were
already flowing through /generate-report correctly, but the web results page
was never updated to display them, still showing old static placeholder
content ("NUST · FAST-NUCES · GIKI", generic internship text).

Fixed:
- sample_roadmap.html: replaced the static "Matched Universities" and
  "Internship Outlook" cards with dynamic "Recommended Courses" and
  "Companies in This Field" cards, wired to read recommended_courses and
  recommended_companies from the real report response.
- pdf_generator.py: gave courses/companies sections highlighted box styling
  (brass-bordered, cream background table) instead of plain bullet lists, so
  they visually stand out as requested. Fixed a bug introduced during this
  change — Table/TableStyle weren't imported, caught immediately by the
  hardened error handling (clean 500 + traceback, no crash) and fixed.

Tested: PDF generates correctly with highlighted sections (confirmed 25KB+
valid PDF output).

## Entry 23 — July 29, 2026 (continued)

**Fixed the root cause of sparse PDF content.** User correctly identified the
PDF looked incomplete. Root cause: COURSE_DIRECTORY was keyed against
tech-specific terms ("Python", "Data Analysis") that barely overlap with
O*NET's ACTUAL skill vocabulary, which only returns broad Work Skills
categories ("Critical Thinking", "Complex Problem Solving", "Programming",
"Judgment and Decision Making", etc.) — meaning most skill-to-course matches
were silently returning empty.

Fixes:
- Rebuilt COURSE_DIRECTORY keyed against O*NET's real skill vocabulary
  (19 skill categories now covered, up from 9 mismatched ones), each with
  2-3 real courses including verified real URLs (Coursera, edX, Khan
  Academy) and real YouTube channel links (freeCodeCamp, CrashCourse,
  3Blue1Brown, DesignCourse) — channels used instead of individual video
  URLs since channels are stable long-term references.
- Added FIELD_FALLBACK_COURSES — tops up results to a minimum of 4 courses
  per report using field-level fallback courses if skill-matching alone
  returns too few, so the report is never sparse.
- Expanded COMPANY_DIRECTORY significantly — roughly 3x more real companies
  per field (e.g. Software/Technology went from 8 to 12 companies).
- Added clickable course links in both the PDF (reportlab <link> tags) and
  the web results page (real <a href> tags, opening in new tab).
- Increased required_skills shown from 5 to 10 in the template report.
- Updated Gemini prompt schema to include and preserve the "url" field on
  courses, with explicit instruction to copy URLs exactly rather than
  inventing new ones.

Tested against realistic O*NET-style skill names (Critical Thinking, Complex
Problem Solving, Programming, etc.) — now returns 9 real courses with working
URLs and 12 real companies, versus the previous near-empty results.

## Entry 24 — July 29, 2026 (continued)

**Built the University Comparisons page (previously a stub).**

- `backend/university_data.py` — curated reference table of 12 real, well-
  known Pakistani universities (NUST, LUMS, IBA, FAST, GIKI, Punjab
  University, Quaid-i-Azam, Aga Khan, King Edward Medical, NCA, Indus
  Valley, UET Lahore), each with category, HEC rank (explicitly dated to
  the 2023 cycle, since HEC hasn't published an update since), an
  approximate annual fee range in PKR (labeled as approximate, not exact),
  and notable programs. Documented in the file itself: this is manually
  curated, not a live feed — no public API exists for this data.
- `templates/universities.html` — real page: category filter pills (All,
  Engineering, Business, Medical, General, Arts/Design), a grid of
  university cards, and a side-by-side comparison feature (select up to 3
  via checkbox, view a comparison table in a modal).
- Route /universities now serves this real page instead of the
  "coming soon" stub.

Tested: all routes still load correctly, confirmed real university names
(NUST, LUMS) render in the page output, confirmed 12 university cards
present with correct data attributes for the JS filtering/comparison logic.

## Entry 25 — July 29, 2026 (continued)

**Expanded university comparison criteria + built Programs Directory page.**

1. Added two new fields to university_data.py: "admission_competitiveness"
   (qualitative: Highly Competitive/Competitive/Moderate) and expanded
   notable_programs lists (from ~3 to 4-6 real, well-known programs per
   university). Explicitly documented that admission_competitiveness is a
   reputation-based estimate, NOT an official acceptance-rate statistic
   (Pakistani universities don't consistently publish these) — flagged for
   disclosure in the paper, same honesty pattern as other curated data.

2. Updated universities.html comparison table to include Category and
   Admission Competitiveness alongside the existing City/HEC Rank/Fee/
   Programs fields — now 6 comparison criteria total.

3. Built a new page: Programs Directory (/programs) — addresses "which
   university is best for X degree" directly. Search-by-degree interface:
   type or click a program tag (e.g. "Computer Science"), see all
   universities offering it, automatically sorted with higher-competitiveness/
   higher-tier institutions first. This "ranking" is derived from our real
   curated admission_competitiveness data, not an invented separate score.
   Linked bidirectionally with the University Comparisons page.

Tested: all 5 routes load correctly, confirmed program tags and university
data render properly in the page output.

## Entry 26 — July 29, 2026 (continued)

**Expanded universities from 12 to 25, added more comparison detail, added
a site-wide page loader.**

1. Added 13 more real Pakistani universities: NED, Mehran, COMSATS, Air
   University, Institute of Space Technology, UMT, SZABIST, Iqra, UCP, Dow
   University of Health Sciences, Ziauddin, Beaconhouse National University,
   Forman Christian College, University of Karachi — broader coverage across
   all existing categories and more cities (Jamshoro, multi-campus entries).

2. Added two new factual fields per university: "sector" (Public/Private —
   verifiable historical fact, not estimated) and "established" (founding
   year). Comparison table now covers 8 criteria total: City, Category,
   Sector, Established, HEC Rank, Admission Competitiveness, Approx. Fee,
   Notable Programs.

3. Added a site-wide page loader (base.html) — a full-screen splash with the
   spinning logo, shown while the page's assets (Tailwind CDN script, web
   fonts) load, masking the flash-of-unstyled-content the user noticed (nav
   headings appearing before Tailwind's styling applied). Built with plain
   inline CSS (not Tailwind classes), since Tailwind itself is what's still
   loading — using Tailwind classes for the loader would defeat the purpose.
   Includes a 3-second safety fallback so it can never get stuck open if the
   window "load" event doesn't fire as expected.

Tested: all routes still load correctly, confirmed 25 universities render
with real data (spot-checked COMSATS and Dow University present).

## Entry 27 — July 29, 2026 (continued)

**Added real Pakistan macro labor market data via World Bank API.**

- `backend/worldbank_client.py` — new module, calls the real, free, no-key-
  needed World Bank API (api.worldbank.org) for Pakistan-specific macro
  indicators: total unemployment rate, youth unemployment rate, labor force
  participation rate, GDP growth. Correctly handles World Bank's response
  format (skips null values, uses most recent available year). Results
  cached in-memory for 24 hours since this data doesn't change frequently
  — avoids hitting the API on every single report generation.
- Investigated ILOSTAT as a second Pakistan-specific source, but unlike
  World Bank, it has no simple REST/JSON API — only bulk downloads/SDMX
  tools, which don't fit our live pipeline. Documented this clearly in the
  module docstring rather than fabricating ILOSTAT figures we can't verify
  programmatically. This limitation is flagged for the paper's Methods/
  Limitations section.
- Wired into the pipeline: /generate-report now fetches this macro snapshot
  and passes it to both the Gemini prompt (with explicit instruction to
  treat it as national-level context, not occupation-specific, and not
  conflate the two) and the template report generator. Wrapped in its own
  try/except so a World Bank outage doesn't fail the whole report — falls
  back gracefully to O*NET + curated data alone.
- Added a new "macro_context_note" field to the report schema, displayed
  on both the PDF (italicized note under Job Market Outlook) and the web
  results page (small italic text under "why it fits").

Tested end-to-end with mocked O*NET and World Bank responses: confirmed real
macro data (e.g., "Pakistan's national unemployment rate was 6.3% as of 2023")
flows correctly through the full pipeline into the final report.

## Entry 28 — August 8, 2026

**Major fixes based on user feedback: restored missing university feature,
switched to strict navy/cream/gold theme, moved navigation to a sidebar.**

**1. Restored the "best university for this field" feature** — this was in
the original project registration but had been dropped from the live
pipeline during earlier UI-focused work sessions. Added:
- `university_data.get_top_universities_for_occupation()` — tries a direct
  program-name match against the matched O*NET occupation first, falling
  back to the broader academic category (mapped from pakistan_resources'
  career-field buckets) if no direct match exists. Always returns real,
  curated data, ranked by admission competitiveness.
- Wired into /generate-report: top 3 matched universities now flow through
  to both the Gemini prompt and the template fallback report.
- Restructured "next steps" from a flat list into a genuine ORDERED
  "career_path_steps" schema (step_number, title, description), each step
  grounded in real data (apply to X university, learn Y skill, take Z
  course, research W companies) rather than generic advice.
- Updated PDF generator and results page to display both the university
  matches and the new numbered career path.

**2. Rebuilt the color system to a strict Navy / Cream / Warm Gold palette.**
Previously the "on-surface" tokens rendered as a cool blue-lavender, and
several templates used raw Tailwind utility colors (emerald green, a
hardcoded blue #6d8fd6) that fell outside the intended palette. Replaced
the entire Tailwind color config in base.html: background/surface tokens
now use true navy (#0B132B family), text tokens use warm cream (#F5F1E8
family), and primary/secondary both resolve to warm gold tones (a lighter
and a deeper shade, for subtle variety without introducing a 4th color).
Swept all templates (index, questionnaire, sample_roadmap, about_data) for
stray emerald/blue Tailwind utility classes and replaced them with
in-palette equivalents.

**3. Moved navigation from a top navbar into a left sidebar**, per explicit
request. Sidebar is fixed, full-height, with the logo/wordmark at top, nav
links stacked vertically (with active-page highlighting), and a "Start Now"
CTA pinned near the bottom. Below the lg breakpoint, the sidebar becomes an
off-canvas panel triggered by a hamburger button in a slim mobile top bar,
with a click-outside-to-close overlay. Main content and footer now offset
by the sidebar's width on desktop instead of a top navbar's height.

Tested: all 8 routes (/, /questionnaire, /sample-roadmap, /universities,
/programs, /about-data, /saved, /advisor) return 200. Confirmed sidebar
markup present, confirmed all three new palette colors present in rendered
output, confirmed zero remaining "emerald" references site-wide.

## Entry 29 — August 8, 2026 (continued)

**Color scheme flipped: beige/cream background, navy text, warm gold accent
(inverting the previous navy-background/cream-text scheme).** The full
Tailwind color token config in base.html had already been updated to this
new scheme in an earlier work session; this entry covers finishing touches
found during review:

- Fixed the page loader's "Career Compass" label, which was still using the
  old scheme's grey-blue text color (#8E97A8) — now uses navy (#1C2541) to
  match the new on-surface color.
- Fixed the outlook chart's year-axis labels (2026/2031/2036) on the sample
  roadmap page, which used the same old grey-blue and were washed out
  against the new light card background — changed to a properly contrasted
  navy-toned muted color.
- Confirmed the compass logo graphics' internal dark-navy fill (in the hero
  SVG) was correctly left unchanged, since that's an intentional design
  element of the badge/icon itself (consistent with the logo mark), not
  page background/text that should follow the page-wide theme.

Tested: all 8 routes return 200 after the fixes.

## Entry 30 — August 8, 2026 (continued)

**Significantly expanded the university dataset after user feedback that it
was too minimal and missing major institutions (specifically flagged: Habib
University).** Previous version relied primarily on general knowledge;
this update used targeted web searches to verify and add real institutions:

Added 6 new universities, each cross-checked against web search results for
founding year, sector, and program details:
- Habib University (Karachi) — private liberal arts & sciences institution,
  est. 2010, strong CS/Electrical Engineering/Communication Design programs.
  This was the specific gap the user flagged by name.
- Institute of Business Management (IoBM, Karachi) — est. 1995, four
  colleges spanning business, computer science, economics, and engineering.
- Sukkur IBA University — est. 2006, known for its Sindh Talent Hunt
  Program scholarship initiative.
- National Textile University (Faisalabad) — est. 1959, Pakistan's premier
  textile engineering institution.
- Bahria University (Islamabad/Karachi/Lahore) — Pakistan Navy-established,
  est. 2000, broad program range including Health Sciences (DPT) and AI.
  Corrected a possible fee estimation error from the previous version by
  verifying against current published figures.
- Pakistan Institute of Engineering and Applied Sciences (PIEAS) —
  est. 1967, postgraduate-focused, highly competitive, strong in nuclear
  and electrical engineering.

Total university count: 25 -> 32. Updated the module's sourcing
documentation to note which entries were general-knowledge-based (original
25) versus web-verified (newest 6), and reiterated that fee figures remain
approximate estimates requiring verification against official sources
before being treated as exact — consistent with the project's existing
data-honesty standard.

Tested: all routes still return 200, confirmed Habib University/IoBM/PIEAS
render correctly in the universities page output, confirmed the occupation
-to-university matching function still works correctly with the expanded dataset.

## Entry 31 — August 8, 2026 (continued)

**Corrected a miscommunication: reverted the main page back to navy
background/cream text, and made ONLY the sidebar beige with navy text.**

The previous entry (30, color scheme flip) had misread the user's original
request — they wanted the SIDEBAR specifically in beige/navy (as a
deliberate contrast element), while the rest of the page should stay navy
background with cream/gold text, per their original UI request. Fixed by:

- Reverted the global Tailwind color token config (background, surface
  tokens, on-surface, on-surface-variant, primary/secondary/tertiary and
  their "on-" pairs) back to the navy-background/cream-text/gold-accent
  scheme.
- Reverted the body background, page loader background, page loader text
  color, and the outlook chart's axis label colors back to their
  light-on-dark versions.
- Rewrote the sidebar and its mobile-equivalent top bar to use hardcoded
  beige (#F2EAD8) background with navy (#1C2541) text — deliberately
  bypassing the page-wide theme tokens, since this is an intentional
  contrast element rather than something that should follow the rest of
  the site's palette.

Tested: all 8 routes return 200; confirmed the main page uses navy
background while the sidebar specifically uses beige background with navy
text, verified via direct HTML output inspection.

## Entry 32 — August 8, 2026 (continued)

**Found and fixed the REAL bug behind the sidebar appearing dark instead of
beige — this was not a caching issue after all.** User provided DevTools
output showing the correct source HTML but a visually broken result, which
correctly ruled out stale files and pointed to an actual code bug.

Root cause: the sidebar used `bg-[#F2EAD8]/97` — combining an arbitrary
custom hex color with an opacity modifier. This specific combination does
not reliably generate a working CSS rule in the Tailwind CDN (Play CDN)
build being used, causing it to silently produce NO background-color rule
at all. With no background applied, the sidebar was fully transparent,
letting the navy page background show through — exactly matching the dark,
washed-out appearance reported.

Fix: removed the `/97` opacity modifier entirely, using a plain solid
`bg-[#F2EAD8]` instead (also removed the now-redundant `backdrop-blur-md`,
since blur has no visible effect over a fully opaque background). Scanned
the entire template directory for any other instance of the same risky
"arbitrary hex color + opacity modifier" pattern — none found elsewhere.

Lesson for future work: arbitrary Tailwind color values with opacity
modifiers (e.g. `bg-[#RRGGBB]/NN`) are a known fragile pattern on the CDN
build; prefer solid arbitrary colors or pre-defined theme color tokens with
opacity modifiers instead, since theme tokens use CSS custom properties
specifically designed to support opacity modifiers reliably.

Tested: all 8 routes return 200, confirmed the fixed class is present in
rendered output.

## Entry 33 — August 8, 2026 (continued)

**Swapped sidebar from beige to warm gold, per user request to try an
alternative.** Kept navy text throughout for contrast (same principle as
the beige version). Changes:
- Sidebar and mobile top bar background: beige (#F2EAD8) -> warm gold (#D4AF37)
- Border color: deepened to a darker gold (#B8952E) to remain visible
  against the new lighter gold background
- Nav link hover state: background changed from a beige tint to a deeper
  gold tint, since the original beige-toned hover wouldn't read correctly
  against a gold background
- Active link indicator: changed from a gold-tinted highlight (which would
  now blend into the gold background) to a navy-tinted highlight for
  visibility
- "Start Now" CTA button: changed from gold-on-cream to navy background
  with light gold text — this was necessary because the original gold
  button would have had very weak contrast sitting on a now-gold sidebar
  background; navy makes it pop as the clear primary action again

All changes deliberately avoided the arbitrary-hex-plus-opacity-modifier
pattern identified as buggy in the previous entry — solid colors used
throughout.

Tested: all 8 routes return 200, confirmed gold background present and no
instances of the previously buggy opacity-modifier syntax remain anywhere.

## Entry 34 — August 8, 2026 (continued)

**Built the AI Advisor (previously a stub).** A real chat interface that
answers follow-up questions using ONLY the student's own already-generated
report — same no-fabrication principle as the rest of the app.

- New route /advisor-chat (POST): takes the student's report + their
  question + recent conversation history, and asks Gemini to answer using
  only that data, explicitly instructed not to add new facts, statistics,
  company/course/university names not already in the report. If the
  question can't be answered from the report, the model is told to say so
  honestly rather than guess.
- ai_engine.generate_advisor_response(): reuses the existing Gemini model
  fallback chain (flash -> flash-lite) for rate-limit resilience, returns
  plain text instead of JSON since this is conversational.
- templates/advisor.html: real chat UI — checks sessionStorage for a
  generated report (same pattern as the results page); if none exists,
  shows a prompt to complete the assessment first. If a report exists,
  shows a live chat with suggested starter questions ("Why this career?",
  "What if I can't afford it?", "What should I do first?").

Tested: all 8 routes still return 200, confirmed /advisor-chat works
correctly end-to-end with a mocked Gemini response.
