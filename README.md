# CA Prep: APPSC current affairs (Android, offline)

CA Prep is an offline Android app for APPSC current affairs, built for Group 2. Every month of news is
rewritten into structured keyword pages, with numbered headings, `**Label:**` lines, tables and ⚠ traps. The
app shows these pages with read marks, bookmarks, read-aloud, word meanings, key terms and a revision plan.
It reuses the code of **Rocket Prep** (`groupsrocket/android`, Kotlin + Jetpack Compose), with CA notes in
place of the ROCKET sheets.

## Sources

Everything comes from the Google Drive folder **"for caformy app"**:

| Source | In `from:` tags | Local copy |
|---|---|---|
| KPIAS **APPSC CARE** daily current-affairs pages (saved web pages) | `YYYY-MM-DD` | `sources/daily_html/` → `sources/text/YYYY-MM/daily/` |
| **APPSC CARE** monthly compilations | `CARE-YYYY-MM` | `sources/pdf_text/monthly/` |
| **AP current-affairs** monthly magazines / news summaries | `APCA-YYYY-MM` | `sources/pdf_text/monthly/` |
| **Praveen Sir CA-360** magazines | `CA360-YYYY-MM` | `sources/pdf_text/praveen/` |
| **Praveen Sir one-liners** | `OL-YYYY-MM` | `sources/pdf_text/praveen/` |
| Topic PDFs (Union / AP budget, Finance Commission, Padma awards, Ramsar sites, reports …) | `TOPIC-<name>` | `sources/pdf_text/other/` |

The raw downloads (`sources/daily_html/`, `sources/pdf/`) are not kept in git.

## Notes format

`data/structured/<folder>/NN.md` holds one file per category of a month (`YYYY-MM`, 2025-04 … 2026-10). The
categories are 01 Andhra Pradesh, 02 Polity & Governance, 03 Schemes & Social Sector, 04 Economy, Banking &
Budget, 05 International Relations, 06 Science, Tech, Space & Defence, 07 Environment & Geography, 08 Reports,
Indices & Rankings, 09 Awards, Persons & Appointments, 10 Sports and 11 Important Days & Events. The folder
`special` holds the topic PDFs. The full spec is in `prompts/notes-guide.md`; in short:

```
=== TOPIC 2026-09:01 | Andhra Pradesh

## Quantum Valley Amaravati | from: 2026-09-03, CARE-2026-09, CA360-2026-09
# 1. What and where
- **Project:** **Amaravati Quantum Valley** — India's first **quantum computing** hub
  - sub-point
| Item | Detail |
|---|---|
# 2. Exam angle
- ⚠ trap line
```

## How the notes appear in the app

| App level | CA Prep |
|---|---|
| Book | A period, newest first: Sep–Oct 2026, Jun–Aug 2026, Mar–May 2026, Dec 2025–Feb 2026, Apr–Nov 2025, then Special topics. A book appears only once it has notes. Its id is fixed (11–16), so a period keeps its progress when others are added |
| Part (unit) | A month (for example "October 2026"), newest first |
| Topic (row) | A category file (for example "Andhra Pradesh") |
| Page | A `## page`, shown after a grey line such as "Sources: Daily 12 Oct · APPSC CARE monthly · CA-360 · One-liners" |

- **Plan:** a revision plan that starts on **19 Oct 2026**. It goes from the latest month to the oldest at
  about 60 pages a day (a big month spans several days); Special topics come last, and every 7th day is a
  weekly review — 63 days in all (54 study, 9 review) for the 2,629 pages. The plan shows "N days left in plan" and no exam date.
- **MCQs:** 11,456 exam-style MCQs testing 97.8% of the notes' 20,515 facts (2,627 of 2,629 pages have questions):
  1–3 headline questions per news item, then deep coverage of every remaining fact (`deepen`), no duplicates, made with the
  OpenAI API by `scripts/ca_mcqs.py` from the facts of each page (`scripts/ca_facts.py`). Each question cites
  the facts it tests ("From your notes"); a second, independent API call must reach the same key with exactly
  one correct option, or the item is dropped. Safeguards, per-format answer spread and the dropped items:
  `out/mcq-report.md`, `out/mcq-run-status.md`.
- **MCQ practice (1.4):** topic and day cards add a **Practise** set (wrong on the latest try, or answered after
  seeing the answer). Progress shows **MCQ results** (right first time, right on a retry, still wrong, answer seen)
  with one "MCQs to practise" set drawn from all books.

## Build

```bash
pip install beautifulsoup4
python scripts/extract_daily.py              # daily HTML pages -> sources/text/YYYY-MM/daily/*.md
python scripts/month_sources.py 2026-09      # lists a month's source texts (input for writing the notes)
python scripts/check_notes.py                # checks data/structured/*/*.md against the format (or: ... 2026-09)
python scripts/build_ca_assets.py            # notes -> android/app/src/main/assets (books, plan, key terms)

cd android                                   # needs the Android SDK: local.properties with sdk.dir=/opt/android-sdk
./gradlew assembleRelease                    # -> app/build/outputs/apk/release/app-release.apk
./gradlew testDebugUnitTest                  # unit tests (Robolectric)
./gradlew recordRoborazziDebug --tests '*ScreenshotTest'   # screenshots -> app/screenshots/
```

You can run `build_ca_assets.py` again at any time. It reads whatever months and files exist, skips a file
that does not parse yet, and lists format problems without stopping. It also runs `build_key_terms.py`.
`structured_md.py` (markdown to app blocks) and `build_key_terms.py` come from Rocket Prep. The assets
`abbr.json`, `acronyms.json`, `india.json` and `dict/` (read-aloud short forms and the offline dictionary)
are copied unchanged from Rocket Prep.

The APK is signed with `android/keystore/ca-prep.jks` (alias `ca-prep`, password `caprep`), so new builds
install over old ones and keep progress. The app id is `com.cagroup.caprep`. The latest build is
`release/CA-Prep-1.0.apk`.
