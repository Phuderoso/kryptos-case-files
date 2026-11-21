# PREREG231 — cycle 231 pre-registration (filed before the registered run)

Filed 2026-11-21 11:42 MST (America/Dawson_Creek, UTC-7), before any run. Slots: 230 new family, **231 free slot**, 232 audit (I-342), 233 new family.
Seeds: 209588–209607 (20 fresh shuffled-ciphertext nulls, `random.Random(seed)` shuffle of the K4 letters), 209608 (plants).
**Next free seed after this cycle: 209609.** Base: origin/main a96260d (tree 23f6f25a).

## Item chosen: I-344 (replicate of the case 216 W ≤ 9 / W ≤ 10 descriptive result on FRESH data) + HASHES

**Why this item.** Case 216 left K4 direct with 47 cells / 22 clusters at W ≤ 10 against a null-equivalent from only 10 nulls at 1/20
scale (5 events); Voynich's blind recount (voynich-case-files 254c4ac, index 4d3050f) confirms the counts and finds K4 ≤ the
null-equivalent in every scope, but the null-equivalent is an expectation resting on 2–3 of 10 nulls having survivors. I-344 asks for more
nulls. Her K096 lesson applies: a follow-up of cells *selected* from K4 on the same data is post-selection description, so the only
new evidence here is **fresh shuffled-ciphertext nulls (new seeds)**. The K4 side is NOT re-run: the K4 cell lists are the published
case 216 files (`data/cycle230/R/k4_*.txt`, unchanged `bsk230` binary sha 52c8d591…, source 580159e6…); nothing about K4 is re-selected.
No new K4 information can arise from this cycle's runs; K4 numbers are re-read only to compare with the new nulls.

**Held-out statement.** The 20 nulls and plant seed 209608 were not used for any threshold in case 216 or earlier; thresholds
(W ≤ 9 primary, W ≤ 10 descriptive, same cluster rule as case 216 `clus230.py`) are the case 216 ones, unchanged.

## Runs (tool `bsk230`, unchanged; thresholds WMAX 10 DMAX 6; D cells are not analysed here)
- Gate P: 20 fresh plants (`plant230.py 209608`, same generator as case 216, independent encryptor), full-scale recovery as in case 216.
  Pass ≥ 19/20, Wilson interval printed beside it.
- Nulls 0–19 (seeds 209588+i): bank and all.bin at **1/20 scale** (row stride 20, row offset i, so the 20 nulls together tile the 20 offsets
  of the row space once; 144² pairs × 3 forms full), all 20 nulls. Direct at **1/5 scale** (X stride 5, offset i) for nulls 0–7 only
  (time budget), Y over all 86,731.
- K4 comparison: per-null-equivalent = (sum of null counts) × scale / n_nulls, versus the published full-scale K4 count. Raw cells and
  clusters (case 216 rule) both reported.

## Decision rules (fixed now)
1. Plants gate P ≥ 19/20 or no label is issued.
2. For each scope × {W ≤ 9, W ≤ 10}, rank rule on clusters per null-slice: let n_f = number of fresh nulls and m_f = number of those with ≥ 1
   surviving cell. If K4's *per-slice mean* (full K4 count / scale) is **above the maximum fresh null slice** → "K4 EXCESS (descriptive,
   post-selection, not a lead)"; if within [min, max] → NO-SIGNAL (equivalent to chance); if the fresh nulls cannot resolve (m_f < 3) →
   INSUFFICIENT-DISCRIMINATION. A pooled estimate with the 10 case 216 nulls is reported as descriptive only.
3. EXACT-EXCL labels of case 216 are not changed by this cycle (they depend on K4 count 0 at W ≤ 8/9 in the stated scopes).
4. No decode, no new threshold, no post-hoc change of scale or of the cluster rule. A coherent 97-letter English plaintext would be needed
   for a solution; this item cannot produce one (filter-only).

## Part B (mandatory housekeeping): HASHES
`HASHES231.txt` carries the full sha256 of `bank.bin` (004ffc24…e862), `all.bin`, `alpha.bin`, `themed144.bin`, `qg.bin`, `bsk230` binary, `bsk230.c`, `k4.txt`,
recomputed from the files actually used. Cited in the case: Voynich's blind recount of c230 (254c4ac, index 4d3050f): 33 files byte-identical;
tool 580159e6 / binary 52c8d591 match; K4 raw lines 3 / 6 / 4 = clusters 1 / 2 / 1 (her rule) and 2 / 2 / 1 (I-291); null-equivalent is an expectation;
read-only leak she disclosed (bank/all/alpha.bin read from /workspace/k4c214/w).
