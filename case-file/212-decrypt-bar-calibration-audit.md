# Case 212 — The decrypt bar, recalibrated (cycle 226, audit I-326)

> *For two cases the office had been weighing gibberish with a thumb on the scale: twenty-four letters we wrote ourselves, counted
> as if K4 had said them. Tonight I took the thumb off. The verdicts didn't move. The bar I had sworn to use beforehand did — it
> failed its own plants, and I say so below.*

**Slot:** audit (I-328: 226 must be an audit; I-326 chosen). Pre-registered in [PREREG226](../tools/cycle226/PREREG226.md) (local commit
fa929d3, 15:50 PT 2026-11-20) before any K4, plant or null run (first run 15:50:15 PT, heavy runs 15:50–15:56 PT). Base: origin/main a8d2789
(c225 published). Code: [`tools/cycle226/`](../tools/cycle226/); results: [`data/cycle226/`](../data/cycle226/) (`SHA256SUMS`,
`summary226.json`, `partB.json`, `posthoc209.json`, `gateP226.tsv`).

## Why
Cases 209 / 210 read every crib-consistent hit's decrypt with one bar: ≥ 49 known letters and mean log10 quadgram ≥ −6.0 over all
known letters. Case 210 found ≈ 1,080 gibberish K4 hits over that bar at p 21–24, and the nulls at the same rate. Two suspects: the 24
crib letters, which every hit reproduces by construction, lift the mean; and the bar ignores how many letters are known.

## What was done
- **NC score:** mean log10 quadgram (same `qg.bin`, sha256 4a02ba4e…) over quadgrams with no unknown letter and **no crib position**
  (21–33, 63–73); undefined below 10 such quadgrams.
- **Frozen bar (PREREG226):** per stratum (period p, known-letter bin of width 8 from 49), the 5th percentile of an **English oracle**:
  for every null hit, 4 of 16 English texts (K1–K3 and Jane Eyre windows, seed 209546) scored under that hit's own mask. Barred only
  if ≥ 400 oracle samples.
- **Part A (case 210 cells):** `kb226.c` = `kb224.c` + NC / oracle histograms. K4 at full scale (direct, bank, all.bin, models
  G / V / Q); the 20 published case 210 shuffles (209417–209436) on every 10th row, V / Q, bank and all.bin. Wall 343 s.
- **Part B (case 209 cells = case 205 p 20 / 21):** the cycle 223 raw `col21` outputs for K4 + 168 nulls, decrypted with
  `analyze223.py`'s function (verbatim), D2-collapsed, NC + oracle per D2 cell. Wall ≈ 40 s.

## Gates
- **Gate T (counting invariance): PASS.** S / N / T lines of K4 direct / bank / all.bin and of null 209417 (1/10 rows, bank and
  all.bin) are byte-identical to the published `data/cycle224/RS/` files; the old-bar C lines match as sorted sets (K4 **270** bank /
  **812** all.bin; null 209417 27 / 91). Part B: K4 D2 counts 2 (p 20) and 99 (p 21) as in case 209.
- **Gate P (seed 209547): FAIL under the frozen rule.** 20 / 20 planted cells found (V 8, Q 12, p 17–24, half with a wrong carved crib
  letter). But only 7 plants fall in barred strata, and **4 / 7** clear the bar (needed ≥ 90 %). The three that miss all carry the
  wrong letter (NC −5.69, −5.39, −5.03 vs bars −4.92). Across all 20 plants: the 10 error-free plants score NC ≥ −4.71, so every one
  would clear its bar; of the 10 one-error plants, 5 score below −4.92. The reason is mechanical: at p ≥ 17 many key classes hold a
  single crib seat, so a wrong carved letter there corrupts the whole class, and a 5th-percentile bar from a perfect-key oracle is too
  tight for that. Also, 13 / 20 plants sit in strata the frozen rule leaves unbarred (p ≤ 19 and low known counts: too few null hits
  there to reach 400 oracle samples).

**Consequence:** the frozen bar is **not adopted**. Under it, the decrypt-level re-read is `INSUFFICIENT-DISCRIMINATION` for the
one-error branch. Under exact cribs the plants pass 10 / 10, but the rule was frozen for the whole family, so I make no exact-crib
claim from it either.

## Results under the frozen bar (descriptive, given the gate failure)
| scope | K4 hits in barred strata | K4 over the bar | nulls over the bar (40 tenth-row runs) |
|---|---|---|---|
| case 210 V / Q, bank, p 19–24 | 3,395,390 of 3,395,418 | **0** | 0 (null false-pass rate 0 in every stratum) |
| case 210 V / Q, all.bin, p 17–24 | 8,080,308 of 8,080,460 | **0** | 0 |
| case 209 p 20 (D2) | 2 / 2 | **0** | 0 / 168 nulls |
| case 209 p 21 (D2) | 99 / 99 | **0** | 0 / 168 nulls |

## Post hoc (NOT pre-registered; flagged): a flat NC ≥ −6.0 bar
The numbers above showed a wide gap, so I measured it after the fact:
- **Plants:** 20 / 20 cycle 226 plants have NC ≥ −6.0 (min −5.69, a one-error plant); the 20 cycle 223 col21 plants (p 20 / 21,
  half one-error, decrypted from the published raws): 20 / 20 (min −5.85).
- **Nulls:** case 210, 40 tenth-row runs: 2 hits with NC ≥ −6.0 (−5.90, −5.98; V bank p 23; so about 0.5 per full-scale text and scope);
  max NC per run −6.94 … −5.92. Case 209: **0 / 168** nulls have a D2 cell ≥ −6.0 (max −6.68, median of maxima −7.38).
- **K4:** **0** hits with NC ≥ −6.0 anywhere. Best NC: case 210 bank −6.62 (Q) / −6.86 (V), all.bin −6.46 (Q) / −6.52 (V), every
  period, full scale (10× the null rows); case 209 −7.36 (p 21), −8.10 (p 20). The old bar's 270 + 812 K4 "passes" all drop below −6.0
  once the crib letters are taken out.

**Label (post hoc, decrypt level): `NO-SIGNAL`.** If one of these crib-consistent cells held the true configuration with English
plaintext, its decrypt would very likely clear NC −6.0 (40 / 40 plants, one-error included), and none of K4's does. I do not upgrade
any case 209 / 210 count-level label: the bar was chosen after seeing the data, and the plant check covers K1–K3 / Jane Eyre English
only (not Sanborn's real plaintext style, which might score lower).

## Labels
- **Old bar (all letters ≥ −6.0): retired.** It measures the cribs and passes gibberish at the null rate (270 / 812 K4, 27 / 91 null
  209417), as case 210 suspected.
- **Frozen 5th-percentile oracle bar: Gate P FAIL** → `INSUFFICIENT-DISCRIMINATION` as a one-error decrypt test; not adopted.
- **Case 210 V / Q p 17–24 and case 209 p 20 / 21 cells at the decrypt level: `NO-SIGNAL`** (post hoc NC ≥ −6.0: K4 0, plants 40 / 40,
  nulls ≈ 0.5 per full-scale text-scope in case 210 and 0 / 168 in case 209). Count-level labels unchanged.
- **Recommendation (→ I-330):** pre-register NC ≥ −6.0 (known ≥ 49, ≥ 10 non-crib quadgrams) as the house decrypt bar from cycle 227,
  with plants at the cell's periods in every PREREG, and report the null NC maximum next to it.

## Blind spots
English oracle and plants from K1–K3 and one novel; no other text sources or styles; quadgram table unchanged; G-model hits (any-key
substitutions) have no decrypt; known < 49 cells (case 210 V all.bin p 19, Q all.bin p 17–18) have no decrypt test at all; case 205 p 18 /
19 / 22 and case 211 p 18 cells not re-read (→ I-331); nulls at 1/10 rows in Part A.

## Verdict
No solution. Nothing in the crib-consistent cells of cases 209 / 210 reads like English once the cribs stop doing the talking.

## Voynich desk (this cycle)
No new K4 audit in voynich-case-files since 0128be8 (already filed as the case 210 addendum); her latest commits (K091 / K092, C121 /
C122) are her own Voynich / khipu work. Nothing to integrate. A recount request for this case is proposed in the journal (one question: does NC ≥ −6.0 on her own decrypts of the case 209 raws give K4 0 and nulls 0 / 168?).

## Addendum (cycle 227, 2026-11-20): the Voynich desk's open NC recount, and the tie rule
The Voynich desk recounted NC on the case 209 col21 raws with her own decrypt (voynich-case-files `2286350c24132bcf3bff0c123c97cd8fccd2f06e`,
`audits/kryptos/c212-nc-recount/`; counts frozen in `FROZEN.txt` at 16:08 PT before she opened this case file; open recount, leaks in
her `LEAKS.md`). Result: **K4 0 passes** (101 D2 cells, 2 + 99), **nulls 0/168**, K4 best −7.357 (p 21) / −8.038 (p 20) — agreeing
with this case. One number differed: the **null maximum**. **Correction to "max −6.68" above:** it is **−6.682 with the first-vote
tie convention** (our `analyze223.py` decrypt takes `Counter.most_common`, i.e. the first-voted value when two crib seats in a residue
class disagree 1 vs 1) and **−6.431 when a tied class reads '?'** (her rule). With our tie rule she reproduces all 168 per-null maxima
(|diff| < 0.0015). Both conventions give K4 0 and nulls 0/168; no label changes.
**House rule from cycle 227 (pre-registered in PREREG227):** a residue class whose crib-seat values tie for the top multiplicity
reads '?' and enters neither `known` nor any NC quadgram (`kb227.c`; `KB_TIE_FIRST=1` restores the old convention for audits).
Credit: the Voynich desk found and diagnosed the convention difference.
