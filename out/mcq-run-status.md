# MCQ run status

Model gpt-5.6-luna. Steps per folder: generate, verify, cover, verify, then build over all folders.

| Folder | Calls (gen/ver/cover/ver) | Tokens in / out | MCQs kept | News pages with a question |
|---|---|---|---|---|
| 2026-10 | 37 / 26 / 13 / 6 = 82 | 182,596 / 101,559 | 226 | 184 / 195 |
| 2026-09 | 64 / 33 / 12 / 6 = 115 | 273,637 / 142,583 | 324 | 229 / 233 |
| 2026-08 | 51 / 27 / 13 / 8 = 99 | 239,919 / 129,442 | 290 | 197 / 200 |
| 2026-07 | 59 / 25 / 4 / 3 = 91 | 220,711 / 109,238 | 237 | 124 / 125 |
| 2026-06 | 49 / 30 / 12 / 6 = 97 | 241,715 / 127,480 | 314 | 233 / 237 |
| 2026-05 | 54 / 32 / 17 / 7 = 110 | 259,839 / 137,368 | 309 | 226 / 237 |
| 2026-04 | 48 / 28 / 10 / 5 = 91 | 216,477 / 111,925 | 274 | 186 / 190 |
| 2026-03 | 49 / 25 / 11 / 5 = 90 | 208,365 / 106,708 | 246 | 159 / 164 |
| 2026-02 | 51 / 27 / 10 / 6 = 94 | 223,295 / 113,007 | 263 | 177 / 181 |
| 2026-01 | 49 / 31 / 14 / 8 = 102 | 236,213 / 136,890 | 310 | 245 / 252 |
| 2025-12 | 30 / 17 / 0 / 0 = 47 | 105,216 / 59,069 | 132 | 64 / 64 |

## 2026-10 answer positions per format

| Format | A | B | C | D |
|---|---|---|---|---|
| Direct Recall | 19 | 26 | 35 | 18 |
| Negative / Incorrect Statement | 3 | 9 | 8 | 4 |
| Assertion-Reason | 7 | 10 | 7 | 7 |
| Statement-Based (A/B) | 8 | 2 | 9 | 9 |
| Multi-Statement Correctness | 4 | 9 | 7 | 5 |
| Chronological Ordering | 0 | 0 | 0 | 0 |
| List-Matching | 2 | 1 | 2 | 0 |
| Count-Based | 0 | 11 | 4 | 0 |

Note: Count-Based keys fall only on B/C (11/4); Chronological Ordering produced no items.

## 2026-10 sample MCQs

### 1. Direct Recall (`2026-10/01/c000#0`)

What is the Andhra Pradesh plan for greenfield Other Than Major Ports (OTMPs) by the end of 2027?

- A. Four greenfield OTMPs already operational
- B. Four greenfield OTMPs operational by the end of October 2026
- C. Four greenfield OTMPs operational by the end of 2027  **(key)**
- D. Four greenfield OTMPs operational by the end of 2026

_Explanation:_ Andhra Pradesh plans to have four greenfield OTMPs operational by the end of 2027. The end of October 2026 is only the target for finalising the operator for Ramayapatnam Port, not for making all four ports operational.

### 2. Statement-Based (A/B) (`2026-10/02/c000#1`)

With reference to the centenary of the Union Public Service Commission, consider the following statements:  
Statement A: The headquarters of the UPSC is at Metcalfe House, Delhi.  
Statement B: The first Public Service Commission was set up at Metcalfe House, Delhi.

- A. Both Statement A and Statement B are true
- B. Both Statement A and Statement B are false
- C. Statement A is true, Statement B is false
- D. Statement A is false, Statement B is true  **(key)**

_Explanation:_ Statement A is false because the UPSC headquarters is at Dholpur House, New Delhi. Statement B is true because the first Public Service Commission was set up at Metcalfe House, Delhi.

### 3. Negative / Incorrect Statement (`2026-10/04/c000#1`)

Which of the following statements regarding the RBI’s 7 October 2026 monetary policy decision is incorrect?

- A. The MPC decision was unanimous.
- B. The policy stance changed from Neutral to Calibrated Tightening.
- C. It was the first repo-rate hike since February 2023.
- D. The MPC decision was chaired by Deputy Governor Sanjay Malhotra.  **(key)**

_Explanation:_ The incorrect statement is that the decision was chaired by Deputy Governor Sanjay Malhotra. It was chaired by Governor Sanjay Malhotra; the decision was unanimous, changed the stance to Calibrated Tightening, and marked the first hike since February 2023.

### 4. Statement-Based (A/B) (`2026-10/07/c000#0`)

Consider the following statements:  
Statement A: Nameri Tiger Reserve is located in West Bengal.  
Statement B: Nameri Tiger Reserve has received CA|TS approval.

- A. Both Statement A and Statement B are true
- B. Both Statement A and Statement B are false
- C. Statement A is true, Statement B is false
- D. Statement A is false, Statement B is true  **(key)**

_Explanation:_ Statement A is false because Nameri Tiger Reserve is in Sonitpur, Assam. Statement B is true because Nameri Tiger Reserve is CA|TS Approved.

### 5. Multi-Statement Correctness (`2026-10/08/c000#1`)

With reference to the Global Innovation Index 2026, consider the following statements:  
1. It was published by WIPO, headquartered in Geneva, and was the 19th edition.  
2. Its theme was "Powering Entrepreneurs at the Frontier of Science".  
3. India ranked first in Central & Southern Asia and first globally in ICT services exports.  
  
Which of the statements given above are correct?

- A. 1 and 2 only
- B. 2 only
- C. 1 and 3 only
- D. 1, 2 and 3  **(key)**

_Explanation:_ All three statements are correct. The 2026 edition was WIPO's 19th edition, carried the stated theme, and recorded India's first position in Central & Southern Asia and in global ICT services exports; therefore, the tempting option “1 and 2 only” is incomplete.

### 6. Multi-Statement Correctness (`2026-10/11/c000#2`)

With reference to the new UNESCO Tentative List entries, consider the following statements:  
1. Bagh Cave Paintings comprise 9 Buddhist rock-cut caves.  
2. Udaigiri Caves comprise 18 caves.  
3. The Sites of Satyagraha have 8 components.  
Which of the statements given above is correct?

- A. 2 only
- B. 1 only  **(key)**
- C. 3 only
- D. 1, 2 and 3

_Explanation:_ Only statement 1 is correct: Bagh Cave Paintings comprise 9 Buddhist rock-cut caves. Udaigiri has 20 caves, not 18, and the Sites of Satyagraha have 9 components, not 8.

### 7. Assertion-Reason (`2026-10/06/c000#2`)

Assertion (A): Jaya is an autonomous underwater vehicle.  
Reason (R): An AUV operates autonomously, whereas an ROV is remotely operated.

- A. Both A and R are true, and R is the correct explanation of A  **(key)**
- B. Both A and R are true, but R is NOT the correct explanation of A
- C. A is true, but R is false
- D. A is false, but R is true

_Explanation:_ Both statements are true, and the reason explains the assertion: Jaya is an indigenous Autonomous Underwater Vehicle, while an AUV is autonomous in contrast to a remotely operated ROV. The distinction concerns the mode of operation.

### 8. Count-Based (`2026-10/05/c000#3`)

How many of the following statements about the US Permanent Labor Certification (PERM) programme are correct?  
  
1. PERM is administered by the US Department of Labor.  
2. The employer files Form ETA-9089 in the PERM process.  
3. PERM certification is valid for 365 days.  
4. PERM is a Green Card.

- A. Only one
- B. Only two  **(key)**
- C. Only three
- D. All four

_Explanation:_ Only statements 1 and 2 are correct: PERM is administered by the US Department of Labor and involves employer-filed Form ETA-9089. The certification is valid for 180 days, not 365 days, and PERM is neither a visa nor a Green Card.

### 9. Assertion-Reason (`2026-10/08/c000#4`)

Assertion (A): India was projected to be the fastest-growing major economy in 2026, with GDP growth of 7.3%.  
Reason (R): Asia accounted for 59% of global growth.

- A. Both A and R are true, and R is the correct explanation of A
- B. Both A and R are true, but R is NOT the correct explanation of A  **(key)**
- C. A is true, but R is false
- D. A is false, but R is true

_Explanation:_ Both the assertion and the reason are true: India's projected GDP growth was 7.3% in 2026, and Asia accounted for 59% of global growth. However, the Asian share of global growth is not stated as the explanation for India's specific growth projection, making the second option correct.

### 10. Count-Based (`2026-10/03/c000#7`)

With reference to the UNICEF child marriage data for India and the world, consider the following statements:  
1. About 22.24 crore girls and women in India were married before the age of 18.  
2. About 9.05 crore girls and women in India were married before the age of 18.  
3. According to NFHS-5, 23.3% of women aged 20–24 were married before the age of 18, compared with 26.8% in NFHS-4.  
4. Globally, about 1.2 crore girls are married before the age of 18 each year, or one every 3 seconds.  
How many of the above statements are correct?

- A. Only one
- B. Only two
- C. Only three  **(key)**
- D. All four

_Explanation:_ Only three statements are correct. Statement 2 is incorrect because 9.05 crore refers to girls and women married before the age of 15, not before the age of 18; statements 1, 3 and 4 correctly state the reported figures.

