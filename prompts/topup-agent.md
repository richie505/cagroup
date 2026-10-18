You are completing the current-affairs revision notes for month {MONTH} of an APPSC exam-prep app, in /home/user/cagroup. The notes already exist in /home/user/cagroup/data/structured/{MONTH}/NN.md (11 category files). Read /home/user/cagroup/prompts/notes-guide.md first (format + rules).

Why: the first writer read a BROKEN text of Praveen Sir's CA-360 magazine — Drive's export stopped at PDF page 80 (the last 10–60 pages: usually Defence, S&T, Economy, Rankings/Indices, National, Books, Days & Themes, were missing), and the magazine and one-liner texts were scrambled by a diagonal watermark, so many facts were skipped. Complete, watermark-free texts now exist:
- CA-360 magazine: {CA360}
- One-liners: {OL}
(`=== PDF PAGE N ===` marks each page.)

Do:
1. Read the magazine from `=== PDF PAGE 79 ===` to the end in full, and put every exam-able fact into the category files: merge into an existing page when the item is already there (grep the key name; add `CA360-{MONTH}` to its `from:` if missing), else add new pages / table rows. Ranks, indices, days & themes, books & authors, defence exercises, appointments — all of it.
2. Then read pages 1–78 of the magazine and the whole one-liners file quickly, looking only for facts that are NOT yet in the notes (the earlier writer skipped many watermark-garbled passages — e.g. ranks of indices, scheme numbers, award lists, venues). Add them. Where the earlier notes have a ⚠ "sources disagree" note that came from a garbled reading, fix it if the clean text settles it.
3. Facts only from these sources. Keep format exact; keep scripts/temp files only in /tmp/claude-0/-home-user/d5f64eb2-7d6a-55ee-935e-4f32f48ae647/scratchpad/t-{MONTH}/.
4. Run `python3 /home/user/cagroup/scripts/check_notes.py {MONTH}` until OK. Do not commit.

Report: pages before → after per file, main additions, anything still unreadable.
