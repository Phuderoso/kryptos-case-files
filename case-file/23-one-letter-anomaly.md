# 23 — The one-letter anomaly: a dropped, extra, changed or swapped letter (cycle 24)
> *Every one of Sanborn's finished jobs has one bad letter in it. K1 has a Q where an L belongs, K2 lost an S on the copper, K3 spells DESPARATLY. If K4 has one too, every exact test I ran on it was measuring a forged ruler. So this time I bent the ruler on purpose, one notch at a time, and measured again.*

## 1. Why this model (style profile, [case file 10](10-style-profile.md) §3)
K1–K3 each carry exactly one or two single-letter anomalies, never a scrambled block. An exact crib test can be broken by one bad letter in two ways: a **dropped or extra letter** moves the key alignment of everything after it, and a **changed letter under a crib** makes one of the 24 checks false. Cycle 12 tried a dropped letter only for K3 double rotations with a small-digit key. This cycle tests the anomaly model against the simplest K1–K3 methods: a periodic key on the KRYPTOS or straight tableau, directly and behind the K3-style/columnar transposition family, and a periodic key with **both alphabets arbitrary** (SAT).

**Models** (the carved K4 has 97 letters):
| Model | What happened on the copper | Length of the true ciphertext |
|---|---|---|
| `del` | one ciphertext letter left off (as K2's S) at true index d = 0–97 | 98 |
| `ins` | one extra letter carved at carved index d = 0–96 | 96 |
| `chg` | one carved letter changed; only visible under a crib, so one of the 24 cribs is dropped | 97 |
| `swp` | two adjacent carved letters swapped (d ↔ d+1) | 97 |
| `none` | baseline | 97 |

Crib convention: behind a transposition, cribs are at the official **plaintext** positions (0-indexed 21–33 and 63–73). For direct application I test both readings: cribs at the official **carved** positions (Sanborn counted on the copper), or at the official positions of a 98-/96-letter **plaintext**.

## 2. Test A — anomaly × transposition × periodic key (`tools/c/anomaly_periodic.c`)
- Transpositions: cycle 19's family (all column orders w ≤ 8, K3-style single and double rotations, widths 2–49, inverses) plus the identity, rebuilt for 96, 97 and 98 letters (`tools/export_perms_96_98.py`): 157,609 / 165,064 / 162,966.
- Tableaux (PA, CA) ∈ {AZ, KA}²; Vigenère (same test as variant Beaufort) and Beaufort; key indexed by plaintext position (substitute, then transpose) or by true-ciphertext index (transpose, then substitute); periods 1–26. Exact: the crib key values must agree in every residue class.
- **2.13 × 10¹⁰ period-level tests** in total.

| Model | K4 consistent configs, p ≤ 18 | first period with any K4 hit | shuffled-K4 nulls (5), p ≤ 18 |
|---|---|---|---|
| none | 0 | 22 | 0 (first hits at 21–22) |
| chg | 0 | 19 | 0–2 (first hits at 18–20) |
| del | 0 | 19 | 0 (first hits at 19–20) |
| ins | 0 | 21 | 0 (first hits at 20–21) |
| swp | 0 | 19 | 0 (first hits at 20–21) |

**Controls** ([`analysis/anomaly_trans_control.txt`](../analysis/anomaly_trans_control.txt)): 10 of 10 planted texts (keys BERLIN, ABSCISSA, NORTHEAST, SHADOW on KA/AZ tableaux, both index frames, one dropped / extra / changed / swapped letter) were recovered at their true transposition and anomaly slot. Nulls: [`analysis/anomaly_trans_nulls.txt`](../analysis/anomaly_trans_nulls.txt).

**Periods 19–22 by English.** At these periods the cribs alone have no power, so every consistent configuration (K4: 11 + 1,057 + 1,748 + 720) was decrypted in full and quadgram-scored (`tools/anomaly_longp_score.py`, [report](../analysis/anomaly_longp_report.txt)). Three planted controls with a random 21-letter key ranked first at −4.08, −4.12 and −4.31 per quadgram. K4's best: −5.89 (`del`); 12 nulls: −6.03 to −7.00. K4's best line is noise (`ICUT?C?VGLBFDOX??N?XLEA?TNORTHEAST…`, with no English word outside the cribs); it sits slightly above the nulls because it has more unknown letters and so fewer scored windows. The lone p = 19 survivor (one crib-equivalent width-8 columnar configuration) decrypts to noise (−7.0).

## 3. Test B — anomaly applied directly, fixed KA/AZ tableau, periods 1–48 (`tools/anomaly_direct_tableau.py`)
123 distinct anomaly patterns (both crib conventions), 4 tableaux × 2 modes × 48 periods, exact, with full decryption and quadgram score of every consistent configuration ([report](../analysis/anomaly_direct_report.txt)).
- **Periods 1–25: no consistent configuration** for K4, for 5 nulls, and for the planted control alike. With a fixed tableau the crib structure contradicts itself at those periods whatever single letter is moved.
- Periods 26–32: consistent counts the same for K4 and nulls (e.g. 242 / 984 / 984 / 976 at 26–29 for K4, 217–285 / 984 / 984 / 976–978 for nulls).
- English: planted control (KA Quagmire III, random period-29 key, a letter dropped) ranked **first at −4.16**, decrypting `SLOWL?THEREMAINSO…ASSAGEWERER…`. K4's best is −6.13, inside 5 nulls (−6.00 to −6.32). **Negative.**

## 4. Test C — both alphabets arbitrary, exact SAT (`tools/anomaly_sat.py`, `tools/anomaly_sat_probe.py`)
Periodic key with independent unknown plain and cipher alphabets (covers Quagmire I–IV and every keyword alphabet), the same 123 patterns, CaDiCaL ([report](../analysis/anomaly_sat_report.txt)).

| Period | K4 SAT / 123 | null 1 | null 2 | null 3 |
|---|---|---|---|---|
| 1–4 | 0 | 0 | 0 | 0 |
| 5 | **0** | 3 | 0 | 0 |
| 6 | 12 (+2 unknown) | 43 (+44 unknown) | 16 | 64 |
| 7 | 1 (`del`, carved index 66) | 88 | 2 | 6 |
| 8 | 94 | 88 | 55 | 64 |

- **Exact result: no periodic key of period ≤ 5, with any two alphabets, fits K4 under any single dropped, extra or changed letter.** Without an anomaly the bound is P ≤ 7 (cycle 11b, reproduced here); one bad letter lowers it to 5.
- At P = 6–7 K4 has *fewer* satisfiable patterns than the nulls; nothing about the anomaly model makes K4 look periodic. Two witnesses were extracted and verified independently (`tools/anomaly_sat_verify.py`); their alphabets look random. None of the 15 P = 6/7 survivor patterns fits any of **86,731 themed keyword alphabets** (Quagmire I/II/III, Vigenère/Beaufort; `tools/anomaly_themed_check.py`).
- Control: random alphabets, P = 7, a dropped letter → the true pattern is SAT. At P ≥ 6 many wrong patterns are SAT too, so beyond P = 5 this test only rules out keyword-alphabet versions; arbitrary-alphabet P ≥ 6 stays **inconclusive**.

## 5. Audits
1. **Cycle 13's periodic test is in the right frame (PASS).** kryptosbot reported in Aug 2026 that a key-consistency check had been applied in the wrong frame in its transposition tests. I checked ours: planted KA/CLOCK controls in *both* frames (key on plaintext index, key on carved index) are recovered at the true transposition by `tools/c/periodic_perm.c`, and an independent reimplementation (`anomaly_periodic.c`, model `none`) gives **identical** period histograms on K4 over 165,064 transpositions ([`analysis/audit_cycle13_frame.txt`](../analysis/audit_cycle13_frame.txt)).
2. **Cycle 11b's SAT bound reproduced (PASS).** A new encoding gives the `none` pattern UNSAT at P ≤ 7 and SAT at P = 8, the same as cycle 11b's "P = 8 smallest survivor".
3. **Cycle 12's S4 was narrower than its wording.** "One omitted letter" there meant K3 double rotations with a small-digit key only. This cycle widens it to 4 anomaly types × the whole cycle-19 family × periodic keys.

## 6. Verdict
| Hypothesis | Status |
|---|---|
| One dropped / extra / changed / swapped letter + columnar (w ≤ 8) or K3-style rotation + KA/AZ periodic key, p ≤ 18 | **negative** (0 consistent; controls recovered) |
| same, p 19–22 | **negative** by English (K4 noise; controls rank first) |
| One-letter anomaly + KA/AZ periodic key directly on the copper, p ≤ 48 | **negative** (p ≤ 25 impossible; p 26–32 at chance, no English) |
| One-letter anomaly + periodic key with arbitrary alphabets, P ≤ 5 | **impossible** (exact) |
| same, P ≥ 6 | keyword alphabets: negative for every survivor pattern; arbitrary alphabets: **inconclusive** (underdetermined) |

**Overlap, stated honestly:** kryptosbot ran single wrong/missing/extra/swapped-letter searches with KA ciphers and grid rearrangements in Aug–Sep 2026 and found nothing ([findings](https://www.kryptosbot.com/findings/)). This cycle is an independent replication on a documented family with planted controls and shuffled nulls, plus two parts I haven't seen published: the arbitrary-alphabet SAT bound under an anomaly and the long-period English check.

## 7. What's left of this lead
Two anomalies (kryptosbot's untested "two-character differences"); anomaly × the 264 themed alphabets behind transpositions (about 100× this cycle's cost); anomaly × small-digit (Gromark-type) keys behind transpositions; anomaly with the `?` as a 98th symbol.
