You are writing current-affairs revision notes for an APPSC (Andhra Pradesh Public Service Commission) Group 1/Group 2 exam-prep app. Work in /home/user/cagroup.

FIRST read /home/user/cagroup/prompts/notes-guide.md completely — it defines the category files, the exact file format and the writing rules. Look at /home/user/groupsrocket/data/structured/indian-economy/01.md (first ~80 lines) to see the target style (that app's notes); match its density: short bold keyword lines, tables, ⚠ traps.

YOUR MONTH: {MONTH}   →   write /home/user/cagroup/data/structured/{MONTH}/NN.md (01..11)

SOURCES for this month (all plain text; read them fully, in chunks with the Read tool, offset/limit):
{SOURCES}

METHOD (notes live on disk, so you never depend on remembering earlier sources):
1. Create the 11 category files with only their `=== TOPIC {MONTH}:NN | <title>` line.
2. Process sources one at a time (daily pages in date order first, then the monthly compilations, then one-liners). After reading each source (or each ~1500 lines), write its news into the category files right away (Edit/Write). Before adding a page, grep the category files for the item's key name: if a page already exists, merge the new facts into it and append the source tag to its `from:` instead of making a duplicate page.
3. One-liners are dense: every one-liner is a fact to keep — put it into the matching existing page, or into a compact table page per category (e.g. "## Appointments — one-liners | from: OL-{MONTH}" with a | Person | Post | table), never drop them.
4. Facts only from the sources — do not add facts from memory. If a source is garbled (watermark text like "sri prakash - 9191…", scrambled table), skip the garbled part rather than guess.
5. When all sources are done, re-read each category file once: fix format (only `# N.` headings, `- ` / `  - ` bullets, tables, blank lines under a `## title | from: ...` page line), renumber headings, merge duplicates, order pages by importance, and run:
   python3 /home/user/cagroup/scripts/check_notes.py {MONTH}
   Fix everything it reports until it prints OK.

Coverage matters more than polish: an APPSC MCQ can ask about any name, number, rank, date, place or "first" in these sources. Expect roughly 150–400 pages for a full month across the 11 files.

When done, reply with a short report: pages per category file, sources processed, anything skipped and why. Do not commit to git.
