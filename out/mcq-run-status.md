# MCQ run status — pilot (October 2026 only)

Stopped after the pilot as instructed; no other months run.

## Run

- Model: **gpt-5.6-luna** (the default; listed as available by `models`, `OPENAI_MODEL` already set to it)
- Key: `OPENAI_API_KEY` worked; no crashes, **no script changes** were needed.
- Steps: generate → verify → cover → verify → build, all `--folders 2026-10`.

| Step | Calls | Items | Tokens in | Tokens out |
|---|---|---|---|---|
| generate | 37 | 581 | 80,251 | 139,824 |
| verify | 50 | 539 | 137,519 | 45,991 |
| cover | 37 | 247 | 101,524 | 116,307 |
| verify (2nd) | 23 | 232 | 56,173 | 18,116 |
| **Total** | **147** | | **375,467** | **320,238** |

## Result

- MCQs kept: **710**
- Facts tested: **1063 / 1135 (93.7%)**
- Answer positions: A 213, B 160, C 139, D 198 (A/D lean comes from the fixed-order formats: A-R, A/B, Count-Based, Multi-Statement)
- Formats kept: Direct Recall 269, Negative/Incorrect 98, List-Matching 92, Multi-Statement 78, Assertion-Reason 59, Statement-Based (A/B) 56, Count-Based 37, Chronological 21

## Dropped items by reason (from out/mcq-report.md)

| Reason | Items |
|---|---|
| code | 57 |
| verify:not_in_facts | 36 |
| verify:two_correct | 6 |
| duplicate | 5 |
| verify:none_correct | 4 |
| verify:garbled | 3 |
| verify:explanation_contradicts | 3 |
| verify:second reader picked option 3, key 0 | 2 |
| verify:second reader picked option 1, key 0 | 1 |
| verify:ambiguous_stem | 1 |

"code" breakdown (recomputed with `problems_of`): numbers not in the cited facts 55, duplicate options 1, explanation mentions the source 1.

Observation for review: several `verify:not_in_facts` drops are strict calls where the facts confirm the key but don't explicitly rule out the distractors (e.g. INS Surya, National Supercomputing Mission) — the second reader may be over-rejecting valid Direct Recall items.

## 10 sample MCQs (copied from data/mcqs/2026-10/*.json, one per category file 01–10)

### 2026-10/01/c000#4 — Andhra Pradesh — List-Matching

**Q.** Match List-I with List-II regarding Andhra Pradesh’s four greenfield ports.

List-I
(a) Ramayapatnam
(b) Mulapeta
(c) Machilipatnam
(d) Kakinada Gateway Port

List-II
(i) Multi-cargo facility developed by Aurobindo Group under PPP model
(ii) State port in Srikakulam
(iii) State port in Prakasam; operator selection through an RFP
(iv) State port built by MEIL

Which of the following codes is correct?

- (A) a-i, b-iv, c-iii, d-ii
- (B) a-ii, b-iii, c-i, d-iv
- (C) a-iv, b-i, c-ii, d-iii
- (D) a-iii, b-ii, c-iv, d-i

**Key:** (D) a-iii, b-ii, c-iv, d-i

**Explanation:** The correct pairs are Ramayapatnam–Prakasam and RFP, Mulapeta–Srikakulam, Machilipatnam–MEIL, and Kakinada Gateway Port–Aurobindo Group PPP facility. The other codes interchange these port details.

### 2026-10/02/c000#4 — Polity & Governance — Negative / Incorrect Statement

**Q.** With reference to the constitutional provisions relating to the UPSC, which of the following statements is incorrect?

- (A) Article 323 provides for an annual report to the President, to be laid before Parliament.
- (B) Article 322 provides that expenses are charged on the Consolidated Fund of India.
- (C) Article 319 makes the UPSC Chairman eligible for further government employment after leaving office.
- (D) Article 318 empowers the President to regulate conditions of service.

**Key:** (C) Article 319 makes the UPSC Chairman eligible for further government employment after leaving office.

**Explanation:** The incorrect statement changes the post-office rule in Article 319. A UPSC Chairman is ineligible for further government employment; Articles 318, 322 and 323 respectively concern conditions of service, expenses and the annual report.

### 2026-10/03/c000#3 — Schemes & Social Sector — Statement-Based (A/B)

**Q.** Consider the following statements:
Statement A: Between 2015 and 2024, India's new TB case rate declined by 21%, compared with a global decline of 12%.
Statement B: India's TB treatment coverage was 92%, compared with the global figure of 78%.

- (A) Both Statement A and Statement B are true
- (B) Both Statement A and Statement B are false
- (C) Statement A is true, Statement B is false
- (D) Statement A is false, Statement B is true

**Key:** (A) Both Statement A and Statement B are true

**Explanation:** Both statements are true. India recorded a 21% decline in the new TB case rate and 92% treatment coverage, against global figures of 12% and 78%, respectively.

### 2026-10/04/c000#6 — Economy, Banking & Budget — Multi-Statement Correctness

**Q.** [Multi-Statement Correctness] With reference to GST collections in September 2026, consider the following statements:
1. Domestic GST collection was ₹1,37,996 crore.
2. GST collection from imports was ₹65,525 crore.
3. Net GST collection was ₹2,03,521 crore.

- (A) 1 and 2 only
- (B) 2 only
- (C) 1 and 3 only
- (D) 1, 2 and 3

**Key:** (A) 1 and 2 only

**Explanation:** Statements 1 and 2 are correct: domestic GST was ₹1,37,996 crore and imports contributed ₹65,525 crore. Statement 3 is incorrect because ₹2,03,521 crore was gross GST, while net GST was ₹1,76,520 crore.

### 2026-10/05/c000#5 — International Relations — Direct Recall

**Q.** (Direct Recall) When and where was the first dedicated BIMSTEC Home Ministers’ meeting held?

- (A) 13 October 2026, New Delhi
- (B) 5–9 October 2026, Arusha
- (C) 10 March 2024, Geneva
- (D) 20 May 2024, Colombo

**Key:** (A) 13 October 2026, New Delhi

**Explanation:** The first dedicated BIMSTEC Home Ministers’ meeting was held on 13 October 2026 in New Delhi. The other options refer to the IPU Assembly, the TEPA signing, or the date on which the BIMSTEC Charter came into force.

### 2026-10/06/c000#13 — Science, Tech, Space & Defence — Assertion-Reason

**Q.** Assertion (A): The National Knowledge Network is described as the backbone of the National Supercomputing Mission.
Reason (R): C-DAC designed the Rudra servers.

- (A) Both A and R are true, and R is the correct explanation of A
- (B) Both A and R are true, but R is NOT the correct explanation of A
- (C) A is true, but R is false
- (D) A is false, but R is true

**Key:** (B) Both A and R are true, but R is NOT the correct explanation of A

**Explanation:** Both the Assertion and Reason are true: the National Knowledge Network is the mission’s backbone, and C-DAC designed the Rudra servers. However, C-DAC’s server design does not explain why the National Knowledge Network is called the backbone.

### 2026-10/07/c000#12 — Environment & Geography — Count-Based

**Q.** How many of the following are listed as CA|TS-accredited tiger reserves in Tamil Nadu?
1. Mudumalai
2. Anamalai
3. Sathyamangalam
4. Bandipur

- (A) Only one
- (B) Only two
- (C) Only three
- (D) All four

**Key:** (C) Only three

**Explanation:** Mudumalai, Anamalai and Sathyamangalam are listed under Tamil Nadu, while Bandipur is listed under Karnataka. Thus, only three of the four reserves belong to the Tamil Nadu list.

### 2026-10/08/c001#15 — Reports, Indices & Rankings — Chronological Ordering

**Q.** Arrange the following events in chronological order:

1. Global release of the World Development Report 2026
2. Publication of “India and Artificial Intelligence: Seizing the Development Opportunity”

- (A) 1–2
- (B) 2–1
- (C) 1 and 2 occurred on the same date
- (D) The order cannot be determined

**Key:** (A) 1–2

**Explanation:** The World Development Report 2026 was globally released on 4 August 2026. The report on India and Artificial Intelligence was published on 6 October 2026, so event 1 preceded event 2.

### 2026-10/09/c000#4 — Awards, Persons & Appointments — Multi-Statement Correctness

**Q.** Consider the following statements about the development of optogenetics:
1. Peter Hegemann studied Chlamydomonas in the early 1990s.
2. Georg Nagel expressed ChR-1 and ChR-2 in frog egg cells.
3. Karl Deisseroth introduced ChR-2 into rat neurons in 2005.

- (A) 1 and 2 only
- (B) 2 only
- (C) 1 and 3 only
- (D) 1, 2 and 3

**Key:** (D) 1, 2 and 3

**Explanation:** All the statements are correct. Hegemann studied Chlamydomonas, Nagel expressed the channels in frog egg cells, and Deisseroth introduced ChR-2 into rat neurons in 2005.

### 2026-10/10/c000#6 — Sports — Assertion-Reason

**Q.** Assertion (A): The 20th Asian Games were declared open at Mizuho Park Athletic Stadium in Nagoya.
Reason (R): The opening ceremony was held on 19 September and had the theme “Harmonic Heart Beat”.

- (A) Both A and R are true, and R is the correct explanation of A
- (B) Both A and R are true, but R is NOT the correct explanation of A
- (C) A is true, but R is false
- (D) A is false, but R is true

**Key:** (B) Both A and R are true, but R is NOT the correct explanation of A

**Explanation:** Both statements are true: the opening took place at Mizuho Park Athletic Stadium in Nagoya on 19 September, with the theme “Harmonic Heart Beat”. The theme describes the ceremony but does not explain why the stadium was the venue.

