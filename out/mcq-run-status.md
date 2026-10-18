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
| 2025-11 | 14 / 10 / 0 / 0 = 24 | 46,384 / 24,950 | 53 | 25 / 25 |
| 2025-10 | 40 / 23 / 11 / 7 = 81 | 180,907 / 101,578 | 228 | 151 / 154 |
| 2025-09 | 37 / 24 / 10 / 4 = 75 | 170,674 / 91,680 | 217 | 159 / 165 |
| 2025-08 | 26 / 17 / 1 / 1 = 45 | 91,293 / 51,052 | 110 | 62 / 62 |
| 2025-06 | 11 / 8 / 3 / 2 = 24 | 46,165 / 26,628 | 52 | 31 / 31 |
| 2025-05 | 15 / 13 / 1 / 1 = 30 | 52,850 / 28,909 | 57 | 41 / 41 |
| 2025-04 | 13 / 11 / 5 / 3 = 32 | 58,002 / 29,281 | 60 | 42 / 44 |
| special | 25 / 9 / 0 / 0 = 34 | 77,953 / 29,457 | 69 | 29 / 29 |
| **Total** | 1363 | 3,132,211 / 1,658,804 | 3771 | 2564 / 2629 |

Final build over all folders: 3769 MCQs kept; news pages with a question 2563/2629; facts tested 7991/20515 (39.0%). No STOPPED and no script crash during the run; scripts/ca_mcqs.py unchanged.

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


## Coverage retry

- cover: 58 calls, 68 items; tokens in 100,599 out 24,638
- verify: 28 calls, 31 items; tokens in 18,239 out 2,980
- build: 3,795 MCQs kept; news pages with a question 2,588/2,629; facts tested 8,040/20,515 (39.2%)

News pages still without a question (41):

- 2025-04/01 — P2: Reliance to set up 500 Compressed Bio-Gas plants
- 2025-04/01 — P17: 3% horizontal sports quota in government jobs
- 2025-09/01 — P9: AP rationalises Dr. NTR Vaidya Seva treatments
- 2025-09/03 — P11: Rising heart disease among young Indians
- 2025-10/01 — P26: GST cuts benefit AP fisheries sector — 'Super GST – Super Savings'
- 2025-10/01 — P36: Unnati Foundation vocational training centre in Kakinada
- 2025-10/05 — P19: UN at 80 — reviving multilateralism
- 2026-01/01 — P22: Jeevan Daan organ donation record 2025
- 2026-01/05 — P6: UAE President's visit — trade target USD 200 billion
- 2026-01/05 — P32: France to ban social media for under-15s
- 2026-01/06 — P3: Samudrayaan — Matsya-6000
- 2026-01/10 — P4: Aryan Varshney — India's 92nd Grandmaster
- 2026-02/04 — P11: Soil Health Card scheme
- 2026-02/07 — P15: Cyclone Gezani hits Madagascar
- 2026-02/08 — P8: National data — organ transplants, students abroad, cyber crime, HIV
- 2026-03/03 — P0: Jal Jeevan Mission extended till December 2028
- 2026-03/03 — P1: PM-KISAN 22nd instalment
- 2026-03/05 — P16: US dollar notes to carry Trump's signature
- 2026-03/10 — P6: Para athletics — Grand Prix New Delhi and National Championships
- 2026-04/06 — P8: Defence exports record ₹38,424 crore in 2025–26
- 2026-04/07 — P6: Solid Waste Management Rules 2026 in force
- 2026-05/01 — P33: AP Cyber Guard system
- 2026-05/03 — P3: PM Surya Ghar Muft Bijli Yojana progress
- 2026-05/04 — P9: Indian Railways — 18-star logo, electrification, CHIRAG
- 2026-05/04 — P18: Bharat Maritime Insurance Pool
- 2026-05/04 — P20: RBI UDGAM portal — 30 banks integrated
- 2026-05/05 — P18: India–Canada trade target and CEPA talks
- 2026-05/10 — P8: Delhi to host Commonwealth Table Tennis Championships 2026
- 2026-05/10 — P14: F1 Sim Racing India Open 2026
- 2026-06/05 — P18: India–Venezuela energy partnership
- 2026-07/04 — P12: Markets, payments and loans — July 2026
- 2026-08/03 — P7: Jal Jeevan Mission completes 7 years
- 2026-09/06 — P14: Google Project Suncatcher — AI computing in space
- 2026-09/08 — P15: Second-hand smoke deaths in India up ~50% — Lancet
- 2026-10/03 — P4: Lakshadweep — first UT with 100% literacy under ULLAS
- 2026-10/04 — P1: GST collections September 2026 — ₹2.03 lakh crore
- 2026-10/06 — P7: CERVAVAC gets WHO prequalification
- 2026-10/06 — P30: TakeMe2Space — India's first networked orbital data centre by 2028
- 2026-10/08 — P11: India's first National Household Travel Survey (NSO)
- 2026-10/11 — P7: International Day of Rural Women — 15 October
- 2026-10/11 — P12: President Murmu visits Hidimba Devi Temple, Manali

## Deep coverage

Per folder: deepen → verify → deepen (round 2) → verify, then a global build (newest month wins duplicates).

- **2026-10** — deepen 37 calls, 420 items, in 106,545/out 146,583; verify 37 calls, 389 items, in 104,800/out 23,210; deepen r2 26 calls, 51 items, in 85,185/out 25,854; verify 11 calls, 42 items, in 13,450/out 2,867 — build: 4228 MCQs kept, facts tested 8714/20515 (42.5%); this folder 645 MCQs, facts 1123/1135 (98.9%)

## 2026-10 sample deep MCQs (new deep items, copied exactly)

### 1. Direct Recall (`2026-10/11/d001#8`)

The Beti Bachao Beti Padhao programme was launched on 22 January 2015 at which place?

- A. Vigyan Bhawan
- B. New Delhi
- C. Panipat  **(key)**
- D. Rome

_Explanation:_ Beti Bachao Beti Padhao was launched on 22 January 2015 at Panipat. New Delhi and Vigyan Bhawan are associated with the Brihattar Bharat International Conference, while Rome is associated with the FAO, IFAD and WFP grouping.

### 2. Direct Recall (`2026-10/01/d002#4`)

Which statement correctly describes World Habitat Day in the context of the PMAY-U 2.0 award?

- A. It is observed on the first Monday of October, was established by the UNGA and was first observed in 1996.
- B. It is observed on the first Monday of October, was established by the UNGA and was first observed in 1986.  **(key)**
- C. It is observed on the first Friday of October, was established by the UNGA and was first observed in 1986.
- D. It is observed on the first Monday of September, was established by the UNGA and was first observed in 1986.

_Explanation:_ World Habitat Day is observed on the first Monday of October, is associated with the UNGA and was first observed in 1986. The other options alter either the weekday, month or year.

### 3. Multi-Statement Correctness (`2026-10/01/d001#10`)

Consider the following statements about sanctioned capacities associated with Andhra Pradesh’s clean-energy mobilisation:  
  
1. Green hydrogen and derivatives had a capacity of 2.20 MMTPA.  
2. Electrolyser manufacturing had a capacity of 2 GW.  
3. Compressed biogas had a capacity of 11,521 tonnes per day.  
  
Which of the statements given above are correct?

- A. 1 and 2 only
- B. 2 and 3 only
- C. 1 and 3 only
- D. 1, 2 and 3  **(key)**

_Explanation:_ All three statements are correct: the capacities were 2.20 MMTPA for green hydrogen and derivatives, 2 GW for electrolyser manufacturing and 11,521 tonnes per day for compressed biogas. Thus, the correct choice includes statements 1, 2 and 3.

### 4. List-Matching (`2026-10/04/d002#9`)

Match List-I with List-II in the context of India’s maritime sector.  
  
List-I  
(a) Maritime trade by value  
(b) Non-major ports  
(c) Exclusive Economic Zone  
(d) Ships in the fleet in mid-2026  
  
List-II  
(i) 95%  
(ii) 217  
(iii) 2.4 million sq km  
(iv) 1,609

- A. a-iii, b-iv, c-i, d-ii
- B. a-ii, b-i, c-iv, d-iii
- C. a-i, b-ii, c-iii, d-iv  **(key)**
- D. a-iv, b-iii, c-ii, d-i

_Explanation:_ The correct pairs are a-i, b-ii, c-iii and d-iv: maritime trade accounts for 95% by value, there are 217 non-major ports, the EEZ covers 2.4 million sq km, and the mid-2026 fleet had 1,609 ships. The other codes interchange these maritime indicators.

### 5. Statement-Based (A/B) (`2026-10/01/d003#7`)

Consider the following statements:  
Statement A: Article 234 deals with district judges.  
Statement B: Article 235 provides for High Court control over subordinate courts.

- A. Both Statement A and Statement B are true
- B. Both Statement A and Statement B are false
- C. Statement A is true, Statement B is false
- D. Statement A is false, Statement B is true  **(key)**

_Explanation:_ Statement A is false because Article 233 deals with district judges; Article 234 concerns other judicial services. Statement B is true because Article 235 relates to High Court control over subordinate courts.

### 6. Assertion-Reason (`2026-10/06/d000#12`)

Assertion (A): Tera, peta and exa denote trillion, quadrillion and quintillion FLOPS respectively, and India generates about 20% of the world's data.  
Reason (R): The world's fastest system in 2026 operated at about 2.19 petaFLOPS.

- A. Both A and R are true, and R is the correct explanation of A
- B. Both A and R are true, but R is NOT the correct explanation of A
- C. A is true, but R is false  **(key)**
- D. A is false, but R is true

_Explanation:_ Assertion A is true: tera, peta and exa represent trillion, quadrillion and quintillion FLOPS, and India generates about 20% of the world's data. Reason R is false because the world's fastest system in 2026 was stated at about 2.19 exaFLOPS, not petaFLOPS.

### 7. Count-Based (`2026-10/01/d002#6`)

How many of the following statements regarding Andhra Pradesh exports are correct?  
1. Exports in 2025–26 were valued at ₹1,76,503.37 crore.  
2. Exports in 2024–25 were valued at ₹1,75,754 crore.  
3. Exports in 2022–23 were valued at ₹1,63,563 crore.  
4. Exports increased by 7.39% over two years.

- A. Only one
- B. Only two  **(key)**
- C. Only three
- D. All four

_Explanation:_ Only two statements are correct: the 2025–26 value was ₹1,76,503.37 crore and the 2024–25 value was ₹1,75,754 crore. The corresponding earlier year was 2023–24, not 2022–23, and the increase over two years was 7.93%, not 7.39%.

### 8. Negative / Incorrect Statement (`2026-10/04/d000#4`)

Which of the following statements regarding September 2026 GST growth in the southern region is incorrect?

- A. Telangana recorded 18% growth, the highest September growth in the south.
- B. Karnataka recorded 16% growth in September 2026.
- C. Andhra Pradesh recorded 11% growth in September 2026.  **(key)**
- D. Tamil Nadu recorded a negative growth of 5%.

_Explanation:_ The incorrect statement is that Andhra Pradesh recorded 11% growth. Andhra Pradesh recorded 6%; 11% was Kerala’s growth, while Telangana recorded the highest southern growth at 18%.
- **2026-09** — deepen 64 calls, 718 items, in 179,620/out 255,427; verify 60 calls, 659 items, in 178,995/out 39,190; deepen r2 48 calls, 110 items, in 152,976/out 62,679; verify 13 calls, 86 items, in 26,197/out 6,223 — build: 4931 MCQs kept, facts tested 9802/20515 (47.8%); this folder 1032 MCQs, facts 1769/1809 (97.8%)
- **2026-08** — deepen 51 calls, 580 items, in 146,964/out 198,633; verify 48 calls, 509 items, in 137,302/out 29,405; deepen r2 39 calls, 99 items, in 127,053/out 47,267; verify 13 calls, 75 items, in 21,282/out 4,386 — build: 5489 MCQs kept, facts tested 10667/20515 (52.0%); this folder 854 MCQs, facts 1532/1564 (98.0%)
- **2026-07** — deepen 59 calls, 721 items, in 162,670/out 245,581; verify 60 calls, 658 items, in 179,057/out 39,164; deepen r2 46 calls, 122 items, in 149,683/out 61,045; verify 15 calls, 103 items, in 29,588/out 7,519 — build: 6201 MCQs kept, facts tested 11801/20515 (57.5%); this folder 951 MCQs, facts 1632/1667 (97.9%)
- **2026-06** — deepen 49 calls, 518 items, in 144,876/out 180,599; verify 43 calls, 464 items, in 128,267/out 27,699; deepen r2 37 calls, 89 items, in 120,069/out 45,777; verify 11 calls, 74 items, in 22,158/out 5,122 — build: 6708 MCQs kept, facts tested 12586/20515 (61.4%); this folder 825 MCQs, facts 1343/1367 (98.2%)
- **2026-05** — deepen 53 calls, 578 items, in 154,179/out 203,735; verify 51 calls, 534 items, in 146,905/out 32,270; deepen r2 38 calls, 109 items, in 126,734/out 51,621; verify 13 calls, 83 items, in 23,382/out 6,392 — build: 7279 MCQs kept, facts tested 13474/20515 (65.7%); this folder 885 MCQs, facts 1560/1598 (97.6%)
- **2026-04** — deepen 48 calls, 511 items, in 135,832/out 176,183; verify 41 calls, 451 items, in 121,445/out 29,664; deepen r2 38 calls, 99 items, in 122,096/out 51,843; verify 14 calls, 80 items, in 24,147/out 5,231 — build: 7769 MCQs kept, facts tested 14227/20515 (69.3%); this folder 769 MCQs, facts 1305/1338 (97.5%)
- **2026-03** — deepen 48 calls, 525 items, in 132,978/out 180,977; verify 46 calls, 489 items, in 131,084/out 27,477; deepen r2 35 calls, 71 items, in 111,240/out 39,212; verify 12 calls, 63 items, in 20,239/out 5,181 — build: 8290 MCQs kept, facts tested 15017/20515 (73.2%); this folder 766 MCQs, facts 1292/1319 (98.0%)
- **2026-02** — deepen 51 calls, 543 items, in 144,731/out 195,751; verify 46 calls, 488 items, in 132,157/out 29,277; deepen r2 39 calls, 95 items, in 127,669/out 46,910; verify 12 calls, 84 items, in 22,965/out 4,514 — build: 8834 MCQs kept, facts tested 15894/20515 (77.5%); this folder 809 MCQs, facts 1481/1498 (98.9%)
- **2026-01** — deepen 49 calls, 520 items, in 139,988/out 187,395; verify 43 calls, 471 items, in 123,564/out 28,924; deepen r2 39 calls, 86 items, in 126,075/out 43,578; verify 12 calls, 72 items, in 20,852/out 4,497 — build: 9342 MCQs kept, facts tested 16681/20515 (81.3%); this folder 823 MCQs, facts 1441/1465 (98.4%)
- **2025-12** — deepen 30 calls, 356 items, in 77,704/out 118,381; verify 31 calls, 321 items, in 80,801/out 16,769; deepen r2 26 calls, 50 items, in 77,110/out 24,474; verify 10 calls, 33 items, in 10,971/out 1,891 — build: 9686 MCQs kept, facts tested 17227/20515 (84.0%); this folder 475 MCQs, facts 822/842 (97.6%)
- **2025-11** — deepen 14 calls, 142 items, in 33,996/out 47,973; verify 15 calls, 126 items, in 33,499/out 7,092; deepen r2 10 calls, 22 items, in 27,932/out 11,268; verify 6 calls, 20 items, in 6,973/out 1,264 — build: 9827 MCQs kept, facts tested 17439/20515 (85.0%); this folder 194 MCQs, facts 330/335 (98.5%)
- **2025-10** — deepen 39 calls, 423 items, in 106,716/out 151,700; verify 35 calls, 374 items, in 97,943/out 22,338; deepen r2 30 calls, 83 items, in 94,306/out 34,901; verify 11 calls, 66 items, in 18,827/out 4,209 — build: 10247 MCQs kept, facts tested 18090/20515 (88.2%); this folder 649 MCQs, facts 1158/1183 (97.9%)
- **2025-09** — deepen 37 calls, 385 items, in 102,739/out 137,470; verify 34 calls, 354 items, in 92,548/out 19,006; deepen r2 25 calls, 47 items, in 78,111/out 21,452; verify 8 calls, 32 items, in 10,086/out 2,223 — build: 10618 MCQs kept, facts tested 18671/20515 (91.0%); this folder 592 MCQs, facts 1076/1101 (97.7%)
- **2025-08** — deepen 26 calls, 244 items, in 63,290/out 83,996; verify 24 calls, 208 items, in 54,951/out 11,664; deepen r2 18 calls, 46 items, in 51,194/out 20,836; verify 8 calls, 29 items, in 9,647/out 1,825 — build: 10839 MCQs kept, facts tested 19019/20515 (92.7%); this folder 331 MCQs, facts 592/613 (96.6%)
- **2025-06** — deepen 10 calls, 104 items, in 26,057/out 33,253; verify 12 calls, 98 items, in 25,224/out 5,590; deepen r2 7 calls, 16 items, in 21,118/out 8,580; verify 5 calls, 12 items, in 4,836/out 909 — build: 10939 MCQs kept, facts tested 19172/20515 (93.5%); this folder 152 MCQs, facts 275/282 (97.5%)
- **2025-05** — deepen 15 calls, 119 items, in 35,166/out 45,003; verify 15 calls, 105 items, in 30,333/out 5,963; deepen r2 9 calls, 21 items, in 24,965/out 11,356; verify 6 calls, 18 items, in 6,593/out 1,384 — build: 11055 MCQs kept, facts tested 19347/20515 (94.3%); this folder 173 MCQs, facts 295/302 (97.7%)
- **2025-04** — deepen 13 calls, 106 items, in 32,227/out 39,234; verify 12 calls, 98 items, in 26,571/out 5,431; deepen r2 8 calls, 12 items, in 23,893/out 4,472; verify 4 calls, 8 items, in 3,380/out 498 — build: 11158 MCQs kept, facts tested 19504/20515 (95.1%); this folder 163 MCQs, facts 312/316 (98.7%)
