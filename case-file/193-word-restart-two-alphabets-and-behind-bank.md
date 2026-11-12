# 193 — Word restart beyond one tableau: behind the transposition bank, and with two alphabets (cycle 206)

> *Case 190 searched the clerk who restarts his key at every word and found nobody home, as long as he worked straight onto the copper. Tonight I asked whether he could have shuffled the page afterwards, K3-style, or kept two different alphabets in his drawer. The shuffled page left him nowhere to stand below eighteen letters of key; the second alphabet only bought him room where any random page buys the same.*

**IDEAS:** I-258 (via I-268). **Pre-registration:** [`tools/cycle206/PREREG206.md`](../tools/cycle206/PREREG206.md), local commit `25c1d74` (2026-11-12 15:48 PT), before any K4 run.
**Code:** [`wrbank.c`](../tools/cycle206/wrbank.c) (Part A, OpenMP C), [`ctl206.py`](../tools/cycle206/ctl206.py) (controls C1/C1b), [`run206.sh`](../tools/cycle206/run206.sh), [`post206.py`](../tools/cycle206/post206.py), [`sat206.py`](../tools/cycle206/sat206.py) + [`sat206_nulls.py`](../tools/cycle206/sat206_nulls.py) (Part B).
**Results:** [`results206_bank.json`](../tools/cycle206/results206_bank.json), [`results206_sat.json`](../tools/cycle206/results206_sat.json), [`runlog206_sat_nulls.txt`](../tools/cycle206/runlog206_sat_nulls.txt), histograms and survivor lines in [`data/cycle206/`](../data/cycle206/).

## Why this (labelled)
- **Fact:** [case 190](190-word-restart-key.md) excluded R1 (key index = position inside the plaintext word, mod L) on one AZ/KA tableau with no transposition, L ≤ 22 (clean at L ≤ 18 after the Voynich recount), and Quagmire III at L ≤ 10 / ≤ 7. Its open list: two different alphabets, a transposition layer, other restart markers. The coverage table had no row entry for either.
- **Inference:** K1/K2 used a keyed tableau, K3 a pure transposition; "word-restart substitution, then a K3-style shuffle" is the style profile's S1 (one substitution + one transposition, [case 10](10-style-profile.md) §5) with the new key rule. With [case 12](12-strips-and-periodic-keys.md)'s correction the "strips" are not evidence for a transposition, so this is a style-driven test, not a sourced one.
- **Other restart markers** were not retested: X restarts are case 25, W restarts case 89, restarts at any point on one tableau case 56 (vocabulary keys).

## Part A — R1 behind the 165,065-transposition bank (exact)
Model Q (cycles 133/164): word-restart encipherment in plaintext order, then a bank transposition σ (both directions, 330,130 orderings);
plaintext letter i is carved at C[S[i]]. AZ and KA tableaux, Vigenère and Beaufort (variant gives the Vigenère consistency test; it is
counted twice, as in case 190). Case 190's 4 × 2 English segmentations, free word offsets o1, o2 ∈ 0..L−1. Per ordering and tableau-form,
8·Σ L² configurations: 1.89×10¹⁰ configurations at L 1–17 (2.8×10¹⁰ counting variant), the full L 1–26 computed for K4.

| Gate / control | Result |
|---|---|
| G0: identity permutation reproduces case 190 | **pass**: 0 at L ≤ 22; 2 / 184 / 414 / 692 at L 23–26 (identical) |
| C1: invented plaintext, R1 KA Vigenère ABSCISSA (L 8), bank entry 12,345 dir 0 | **pass**: true cell found, key ABSCISSA; 12 cells survive, all with key ABSCISSA (bank entries equal on the 24 crib cells) |
| C1b: R1 AZ Beaufort PALIMPSEST (L 10), entry 98,765 dir 1 | **pass**: true cell found, key PALIMPSES? (index 9 is reached by no crib letter) |
| Null: 20 shuffled K4 (seed 206206), each over the full bank, L 1–22 | below |
| Disclosures | C1b first failed only because the checker demanded the key letter at an index no crib letter reaches; the checker now treats `?` as a wildcard (tool unchanged). One unregistered timing run on a shuffle (Python `Random(1)`, not a registered null) preceded the K4 run; its counts are not used. |

| L | K4 surviving cells | null mean | null min–max | nulls with any survivor |
|---|---|---|---|---|
| 1–17 | **0** | 0 | 0–0 | **0 / 20** |
| 18 | 4 | 1.5 | 0–12 | 6 / 20 |
| 19 | 106 | 76 | 6–634 | 20 / 20 |
| 20 | 782 | 1,131 | 332–2,812 | 20 / 20 |
| 21 | 13,570 | 17,054 | 11,224–41,094 | 20 / 20 |
| 22 | 290,094 | 314,600 | 244,584–425,846 | 20 / 20 |
| 23–26 | 4.9×10⁶ … 2.4×10⁸ | not run (saturated, case 190) | | |

**Read-out of the K4 survivors at L 18–19** (64 cells; the letters that can be decrypted without guessing word boundaries are the hidden
start of each crib word and its continuation if the word goes on; full list in `post206_out.txt`): all gibberish, e.g. the only L 18 pair
(entry 128,252 and its inverse twin, AZ Vigenère, key GSBWSRDEUEMFPIXSTA) needs a word "…AWDMLCFFYK" + EASTNORTH. None reads as English.

## Part B — R1 with two alphabets, direct (SAT)
Quagmire I (plain alphabet free, cipher A–Z), Quagmire II (plain A–Z, cipher free), Quagmire IV (both free, independent); Vigenère form
c = Y[x(p) + s_k] and Beaufort form c = Y[s_k − x(p)]; key classes as case 190 (segmentations and offsets); only the partition of the 24 crib
letters into key classes matters, so configurations were deduplicated by partition (1 / 13 / 39 / 79 / 97 / 201 / 283 / 379 / 489 / 613 / 749 / 891
partitions at L 1–12). pysat Glucose4.

| Gate / control | Result |
|---|---|
| C2 / C2b / C2c: planted QIV / QII / QI word restart (random alphabets, L 8, invented text) | **pass** (SAT at the true configuration) |
| G-mono: L = 1 is a monoalphabetic map and K4's crib sends N and O to Q, so every model must be UNSAT | **pass** (6 / 6) |
| Bug (disclosed): the first launch pinned the fixed A–Z alphabet with positive units only, so it printed K4 QI SAT at L 1 (impossible: N, O → Q). Killed after three K4 lines, fixed (every cell pinned), G-mono added, rerun from scratch; the first launch's numbers are discarded | fixed |

| Model (Vig = Beau, see note) | K4: UNSAT at L ≤ | K4 first SAT | 5 nulls (seed 206207): first SAT L |
|---|---|---|---|
| Quagmire I | **11** | 12 | 12, 12, 12, 13, 11 |
| Quagmire II | **10** | 11 | 8, 10, 10, 10, 11 |
| Quagmire IV | **5** | 6 | 5, 5, 5, 5, 8 |

Beaufort gave the same first-SAT L as Vigenère for K4 in every model; with a free alphabet the two forms are equivalent (reflect the free
alphabet), so the nulls were run on the Vigenère form. **Budget disclosure:** the registered 300 s cap stopped the null loop after QI; the same
five nulls (identical draw) were rerun for QII and QIV in parallel (`sat206_nulls.py`, 24 s), outside the cap.

## Verdict
- **EXCLUDED (exact, under these assumptions):** a word-restart key (R1) on the straight or KRYPTOS tableau, Vigenère / Beaufort / variant, any key
  of length 1–17, applied in plaintext order and followed by any of the 165,065 bank transpositions (either direction), for every English
  segmentation of the cribs and any word offset. No null survives at L ≤ 17 (0 / 20 full-bank shuffles), so the test has power there.
- **NO-DISCRIMINATION:** L 18–22 behind the bank (K4 inside the null range, below the null mean at L 20–22; decryptable fragments gibberish);
  L ≥ 23 saturated.
- **EXCLUDED (exact) direct, any alphabets:** Quagmire I word restart at L ≤ 11, Quagmire II at L ≤ 10, Quagmire IV at L ≤ 5, Vigenère and Beaufort
  forms, all case-190 segmentations and offsets. These limits are mostly the cribs' own strength: shuffled texts turn SAT at about the same L
  (QI 11–13; QII 8–11; QIV 5–8), so above them the family is **underdetermined**, not supported. K4 staying UNSAT one step longer than 4 of 5
  nulls in QII and QIV is descriptive only (n = 5).
- **Not tested:** two alphabets behind the bank (SAT per permutation is too slow; keyword-alphabet pairs would be the exact route, I-270),
  R1 behind the K3-law decimations/routes (I-269), a wrong or dropped crib letter, keys longer than the decision ranges.
- **Compute:** Part A 4 min 57 s wall on 6 threads (K4 + 20 nulls); Part B 300 s capped + 24 s supplement on one core each, partly overlapping;
  ≈ 6 min of wall-clock heavy compute.

**No solution; K4 status unchanged.**
