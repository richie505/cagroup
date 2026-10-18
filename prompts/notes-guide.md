# CA notes guide — structured keyword pages (Rocket Prep / APPSC Prep format)

The CA app shows current affairs the same way Rocket Prep shows the ROCKET sheets: every month is
rewritten into **structured keyword pages** — numbered headings, `**Label:**` lines, tables, ⚠ traps —
so a reader can revise a news item in 30 seconds and every exam-able fact is bold.

## Files

`data/structured/<YYYY-MM>/NN.md` — one file per **category** of that month (NN = the category number
below, two digits). Skip a category only if the month truly has nothing for it.

| NN | Category (topic title) | What goes in |
|---|---|---|
| 01 | Andhra Pradesh | AP govt schemes, policies, MoUs, investments, projects, AP persons, AP awards, AP districts/places, AP budget, AP firsts |
| 02 | Polity & Governance | Constitution, Parliament, bills/acts, judiciary, elections, constitutional/statutory bodies, centre-state |
| 03 | Schemes & Social Sector | Central schemes, missions, health, education, women/children, welfare, social justice |
| 04 | Economy, Banking & Budget | RBI, monetary policy, GDP/inflation data, budget, taxes, banking, trade, agriculture economy, infrastructure |
| 05 | International Relations | Bilateral visits, agreements, summits, international organisations, world events, groupings |
| 06 | Science, Tech, Space & Defence | ISRO/space, AI/IT, biotech, health science, defence exercises, missiles, ships, inventions |
| 07 | Environment & Geography | Climate, biodiversity, protected areas, Ramsar, tiger reserves, species, disasters, places in news, GI tags |
| 08 | Reports, Indices & Rankings | Every index/report with publisher, India's rank, top/bottom countries/states |
| 09 | Awards, Persons & Appointments | Awards and honours, appointments, obituaries, books & authors, persons in news |
| 10 | Sports | Tournaments, winners, venues, records, players |
| 11 | Important Days & Events | Days and themes, conferences, festivals, firsts, miscellaneous |

## File format (parsed by the app — follow exactly)

```
=== TOPIC 2026-09:01 | Andhra Pradesh

## Quantum Valley Amaravati | from: 2026-09-03, 2026-09-16, CARE-2026-09, CA360-2026-09
# 1. What and where
- **Project:** **Amaravati Quantum Valley** — India's first **quantum computing** hub
- **Partners:** **IBM**, **TCS**, **L&T**
  - **IBM Quantum System Two** — **156-qubit Heron** processor
| Item | Detail |
|---|---|
| **Launch** | **January 2026** |
# 2. Exam angle
- ⚠ **National Quantum Mission** was approved in **April 2023** (not 2024) — outlay **₹6,003 crore**
```

Rules:
- Line 1 `=== TOPIC <YYYY-MM>:<NN> | <Category title>` exactly as in the table.
- Each news item (or a tight cluster of related items) is one **page**: `## <short title> | from: <sources>`.
  `from:` lists the daily dates (`YYYY-MM-DD`) and/or source tags: `CARE-YYYY-MM` (APPSC CARE monthly PDF),
  `APCA-YYYY-MM` (AP current-affairs monthly magazine / news summary), `CA360-YYYY-MM` (Praveen Sir CA-360 magazine),
  `OL-YYYY-MM` (Praveen one-liners), `TOPIC-<name>` (topic PDF such as Union Budget). Comma-separated, no `#`.
- Inside a page only these line kinds are allowed:
  - `# N. Heading` (numbered from 1 in each page)
  - `- **Label:** text` bullet; `  - text` sub-bullet (two spaces)
  - markdown tables (`| a | b |` lines, header row then `|---|---|`)
  - blank lines
- Bold (`**…**`) every exam-able token: names, numbers, dates, places, organisations, ranks, firsts,
  article numbers, schemes. Do not bold whole sentences.
- ⚠ marks a trap: a commonly confused fact, a "first/only/largest" claim, a superlative, a changed number,
  a near-miss option (e.g. "⚠ **not** the first — Kerala was first in 2019").
- Background static GK that the article gives (constitutional articles, what an organisation is,
  HQ, founded year, head) goes in its own `# N. Background` heading — keep it short and exam-useful.
- Keep EVERY fact that could be asked in a Prelims MCQ: who/what/where/when/how much/rank/first/theme/
  venue/winner/outlay/HQ/launched by. Drop editorial opinion, "way forward", mains essay padding,
  FAQs that repeat facts, and the sources' own MCQs (but keep any fact those MCQs test).
- Tables for anything list-like: award winners, index ranks, tournament results, MoU lists, days & themes.
- One fact once: when two sources give the same news, merge into one page and list both in `from:`.
  When they disagree on a number/date, keep the more specific one and add ⚠ noting the other.
- Order pages inside a category by importance for APPSC (AP-related and big national items first).
- English only. No emojis except ⚠. No links/URLs. No "Source: The Hindu" lines.
