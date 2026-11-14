# Case file 195 — The word-restart key behind K3's decimation law

**Cycle 208, 2026-11-12 (~23:44–23:58 PT, America/Vancouver).** IDEAS I-269 (new family; pointer I-273).
Pre-registered in [`PREREG208.md`](../tools/cycle208/PREREG208.md) (local commit 131f0e6, 23:47 PT, before any K4 or null run).
Solver **unchanged** [`wrbank.c`](../tools/cycle206/wrbank.c) (byte-identical, sha256 prefix 1001272db7eeff33); harness
[`run208.sh`](../tools/cycle208/run208.sh), plants [`gate208.py`](../tools/cycle208/gate208.py), summary
[`post208.py`](../tools/cycle208/post208.py); outputs in [`data/cycle208/`](../data/cycle208/) and
[`results208_gate.json`](../tools/cycle208/results208_gate.json).

## Question
Could K4 be a **word-restart key** R1 (the key restarts at every plaintext word: key index = position of the letter inside its word,
mod L; case 190) on the A–Z or KRYPTOS tableau, followed by **K3's own transposition law**, one of the 165,782 K3-law decimations /
spiral-diagonal routes of `all.bin` (built cycle 168, used in cycles 173–183)? [Case 193](193-word-restart-two-alphabets-and-behind-bank.md)
answered this for the other family (the 165,065 columnar / rotation bank); this family had never been combined with R1.

## Model (exactly as tested)
- Plaintext enciphered in plaintext order with R1, Vigenère / Beaufort / variant (variant gives the same consistency test as Vigenère),
  tableau A–Z or KRYPTOS; then plaintext position i carved at S[i] (layer letter i = C[S[i]]), S = family row or its inverse.
- Cribs EASTNORTHEAST at 22–34 and BERLINCLOCK at 64–74 (1-indexed). Word segmentations of case 190 (EASTNORTHEAST,
  EAST|NORTHEAST, EASTNORTH|EAST, EAST|NORTH|EAST × BERLINCLOCK, BERLIN|CLOCK), free offsets o1, o2 ∈ 0..L−1 (the crib may begin
  inside a longer word). Survivor = equal key index ⇒ equal key value on all 24 crib letters.
- Family: `all.bin` md5 946402ca…, 165,782 rows (165,740 distinct), **closed under inverse** (checked on every row; 108 self-inverse),
  no identity row, 796 rows shared with the case 193 bank. Raw cell counts below include the inverse twin (dir 0 / dir 1 on twin rows)
  and the Vigenère / variant pairing, so one configuration usually shows as 2 or 4 cells.

## Gates and controls
| Check | Result |
|---|---|
| G0: identity (direct) reproduces case 190 | **pass**: 0 at L ≤ 22; 2 / 184 / 414 / 692 at L 23–26 (doubled-Vigenère convention); histogram identical to cycle 206's G0 |
| Stratum M: 20 plants L 16, EAST\|NORTHEAST + BERLIN\|CLOCK, o = 0 | **20 / 20** recovered (gate ≥ 19) |
| Stratum A: 20 plants L 16, EASTNORTH\|EAST + BERLINCLOCK, o = 0 | **20 / 20** (gate ≥ 19) |
| Stratum O: 10 plants L 16, **non-zero offsets** o1 = 6, o2 = 4 (crib glued to the previous word) | **10 / 10** (gate ≥ 9) — closes case 194's offset blind spot for this family |
| Optional: 5 stratum-M plants at L 17 | 5 / 5 (descriptive) |

Plants: invented text (not a K4 guess), rows drawn uniformly from all of `all.bin`, direction uniform, all four tableau/form cells,
random keys; seed 208209 (next free 208210). Detection required the true row, direction, tableau/form, L, segmentation, offsets and the
planted key at every determined index. **Gate PASS**, 30 s.

## Result (K4 and 20 shuffled-K4 nulls, full family, seed 208208)
| L | K4 cells | null mean | null min–max | nulls with ≥ 1 | Reading |
|---|---|---|---|---|---|
| 1–16 | **0** | 0 | 0–0 | 0 / 20 | **`EXACT-EXCL`** (plant-gated at L 16 on all three strata) |
| 17 | 0 | 0.10 | 0–2 | 1 / 20 | zero, but the registered rule does **not** call it excluded (one null config survived; rate 95 % CI ≈ 0.1–25 %) |
| 18 | 0 | 0.90 | 0–4 | 6 / 20 | zero, not discriminating (≈ 30 % of nulls survive) |
| 19 | 18 | 30.6 | 12–64 | 20 / 20 | `NO-DISCRIMINATION` (K4 below the null mean) |
| 20 | 934 | 636.6 | 398–972 | 20 / 20 | `NO-DISCRIMINATION` |
| 21 | 12,414 | 11,575.6 | 10,246–13,620 | 20 / 20 | `NO-DISCRIMINATION` |
| 22 | 211,534 | 211,005.9 | 206,712–218,674 | 20 / 20 | `NO-DISCRIMINATION` |
| 23–26 | 3.5 M … 158 M | — | — | — | not run on nulls (no power by construction) |

- **L 19 survivors, read anyway (descriptive):** 18 cells = 8 configurations, each an inverse-twin pair (one also under two
  segmentations); keys DIJQSNTVPZSBYACYKWV, EAZPBLCIVNZADBHZYUH, FQBNDRIZGRKIDRKCHEE, HARIRBMTDQZPCKCZODE, MVFJKVWTMTQCFAQNSMT,
  UWYXNUHXSNRHCEYEIHR, YBQRVPBVZKBKEBDQWDQ, YIKDTMGZNARQXRXUSCI: no English word, no K1–K3 vocabulary
  ([`k4_fam_L19_full.txt`](../data/cycle208/k4_fam_L19_full.txt)). Fewer than the null mean, so nothing to chase.
- **Comparison with the bank (case 193), same doubled-Vigenère convention:** null means here 0.1 / 1.2 / 47.3 / 990 at L 17–20 vs
  1.5 / 76 / 1,131 at L 18–20 behind the bank; K4 here 0 / 0 / 26 / 1,270 vs 0 / 4 / 106 / 782 there. Same shape for both families:
  an exact zero up to L 16, a soft frontier at 17–18, then the cribs stop deciding. (Table above: raw cells, Vigenère counted once.)

## Verdict and scope
- **Excluded (exact, under the model above):** K4 = R1 word-restart key, any key of length **1–16**, A–Z or KRYPTOS tableau,
  Vigenère / Beaufort / variant, the case 190 crib segmentations with any offsets, followed by any of the 165,782 K3-law decimations /
  routes in either direction. Chance false-survivor probability at L 16 extrapolated from the null means (0.1 at L 17, 0.9 at L 18)
  is well under 1 %; plant-validated at L 16 with zero and non-zero offsets.
- **L 17–18:** K4 has no survivor, but the nulls are not clean enough to call it an exclusion (registered rule). **L ≥ 19:**
  `NO-DISCRIMINATION`.
- **Not tested here:** the other layer order (transposition first) is not meaningful for a key that follows plaintext word positions
  and was not run; two different alphabets (Quagmire I/II/IV) behind this family; keyword-alphabet pairs (I-270 analogue);
  restart markers other than word boundaries (X, W); a wrong or dropped crib letter; segmentations outside case 190's list; families
  other than these two transposition sets. Plants and solver have the same author (I-274 is the independent-encoder check, for the
  bank).
- **Known quirk (no effect on counts):** `wrbank`'s print cap is per thread (OpenMP reduction), so the L 1–22 run printed 30,000
  survivor lines for a cap of 5,000; histograms are unaffected, and the full L 19 list was re-printed from a single-L run.
- **Compute:** gate 30 s + registered run 4 min 23 s (23:48:18–23:52:41 PT) on 6 threads, one owned process group; ≈ 5 min total.

**No solution; K4 status unchanged.**

## Addendum (cycle 209, 2026-11-13): plant coverage audit by the Voynich desk; L 16 scope
Text above preserved. The Voynich desk counted mid-block vs block-aligned crib splits over the whole family
(box-local `voynich/kryptos-audits/case195-coverage/results.md`; plan sha256 f331d1cd…, addenda 31b1ea41… and ab5b5577…, label map
32142da5…, all hashed before counting; 0 unmatched rows). Of the 1,326,256 (row, segmentation) pairs, **84.4 %** are mid-block,
**3.08 %** block-aligned, and 12.5 % unsegmented. Aligned pairs occur only for decimations with M > 97 and s ∉ {1, M−1}, and for routes. Of
cycle 208's 55 recovered plants, **53 were mid-block and 2 aligned** (both stratum A, L 16, decimations M 109 / M 110 on
EASTNORTH|EAST + BERLINCLOCK). No aligned route plant was drawn. Her locked rule calls the coverage adequate, so no new plant design was
triggered.
- **Scope, restated.** The K4 zero at L ≤ 16 runs over every (row, segmentation, offset), so the exclusion itself is unchanged. What changes is
  how strongly it is plant-validated. **Mid-block: validated at L 16** (48 of 48 L-16 mid-block plants). **Grid-aligned: only weakly**
  (2 / 2, Clopper–Pearson 95 % interval 0.16–1). **Aligned routes: not exercised.** The "chance false-survivor probability at L 16 well under 1 %"
  above is an **extrapolation** from the L 17–18 null means, not a measured rate, so it is read as soft.
- **L 17 under the boundary-band rule (I-281):** 1 / 20 nulls (p 0.05, SE 0.049) is `UNRESOLVED`. **L 18:** 6 / 20 (0.30, SE 0.10) is clearly
  above the 5 % bar, so it is **not excluded**. Both readings agree with the verdict above.
- **Optional follow-up queued (I-280):** an aligned plant stratum on EAST|NORTHEAST + BERLINCLOCK, the largest split that is non-empty in
  both subfamilies (12,164 decimation + 723 route aligned pairs), with separate decimation and route sub-strata.

## Addendum 2 (cycle 211, 2026-11-13): blind aligned plants 20/20 and a measured L 16 chance rate
Text above preserved. Registered in [PREREG211](../tools/cycle211/PREREG211.md) (local commit `e358dda`, ~11:46 PT) before any plant ran and before
the sealed truths were opened; part C added as PREREG211b (local `f406596`) before it ran.
- **Input (Voynich desk, her own encoder, not our code):** 20 blind plants A01–A20 on the aligned EAST|NORTHEAST + BERLINCLOCK stratum
  (boundary at layer index 25 a block edge), 10 decimations + 10 routes (fill modes 3/4/3), L 16, model Q, o1, o2 uniform 0..8 (9 plants with
  o2 ≥ 6, so BERLINCLOCK's key indices wrap mod 16), English filler from Gutenberg #1661, her seed 6429. Ciphertexts sha256 e2466b0e…
  (copied as `tools/cycle211/plants211_ciphertexts.txt`); sealed truths sha256 da448d89… (checked on opening: match).
- **Blind run:** `wrbank.c` unchanged (sha256 1001272d…) on full `all.bin`, L 16, every survivor printed
  ([`blind211.py`](../tools/cycle211/blind211.py)); [`results211_blind.json`](../tools/cycle211/results211_blind.json) sha256
  **38e9fb60fb4feaae1880cff8a230f932ff29ae694416735003150f0ae18ee144**, committed (local `97a7c8b`) before the truths were opened. 11 s.
- **Scored** ([`score211.py`](../tools/cycle211/score211.py), [`results211_scored.json`](../tools/cycle211/results211_scored.json) sha256 030c82c8…):
  **20 / 20 recovered** at the true (row, dir, tm, L 16, EAST|NORTHEAST, BERLINCLOCK, o1, o2) with the planted key on every determined index →
  **gate PASS** (≥ 19 / 20). Clopper–Pearson 95 % 0.83–1. Decimations 10 / 10, routes 10 / 10, wrapped offsets (o2 ≥ 6) 9 / 9. Undetermined key
  indices per true line: 0–5. **Every survivor line in all 20 plants lies on the true row or its equivalent** (inverse row with the other direction,
  or for A15 the true row's duplicate pair); 0 off-target rows. Extra lines on the true row (A04, A07, A08, A13, A15, A19: 40–92 lines) are other
  segmentation/offset readings of the same layer that the crib letters cannot tell apart, not false survivors.
- **Part C, measured L 16 chance rate** ([`null211.py`](../tools/cycle211/null211.py), [`results211_null.json`](../tools/cycle211/results211_null.json)
  sha256 ed8d83e4…): 200 shuffled-K4 ciphertexts (seed 209217) over the full family at L 16: **0 / 200 with any survivor** → per-ciphertext
  false-survivor rate **< 1.49 %** (one-sided 95 %). This replaces the extrapolated "well under 1 %" with a measured bound (still only a bound;
  "under 1 %" would need ≈ 300 clean nulls). 111 s.
- **Scope, restated.** The K4 zero at L 1–16 is unchanged. It is now plant-validated at L 16 on **mid-block** (48/48, cycle 208) **and on the aligned
  EAST|NORTHEAST + BERLINCLOCK stratum, both subfamilies, including aligned routes and wrapped offsets (20/20 blind, independent encoder)**. Other
  aligned splits (EASTNORTH|EAST, BERLIN|CLOCK, EAST|NORTH|EAST) were not drawn here; they run through the same code path. L 17–18 are unchanged
  (`UNRESOLVED` / not excluded). Credit: the plant design, label map and sealed truths are the Voynich desk's (box-local
  `voynich/kryptos-audits/case195-aligned-plants/`).
- **Disclosure.** The message of commit `f406596` says "parts A/B results not yet committed". That is wrong. That commit itself added the
  part A scoring (`score211.py`, `results211_scored.json`) and the part B results (`results211_c4look.json`), which had already run, together
  with the part C registration. What the message should have said is that part C had not yet run. The true order: scripts `blind211.py` /
  `c4look211.py` and PREREG211 (`e358dda`) → blind results (`97a7c8b`) → truths opened and scored, part B run → part C registered
  (`f406596`) → part C run.

## Addendum 3 (cycle 212, 2026-11-13): wording fixes from the Voynich desk's second count, and a commit-hash erratum
Text above preserved. The Voynich desk independently re-scored the 20 blind plants with her own scorer and got **20 / 20** (decimations 10/10,
routes 10/10, wrapped 9/9; box-local `voynich/kryptos-audits/case195-second-count/`). She asked for two wording fixes, adopted here:
- **A15:** addendum 2 says "or for A15 the true row's duplicate pair". That is inexact. A15's extra lines sit on rows **164,727 (dir 0) and 164,980
  (dir 1)**. Their maps match the true map (164,841 dir 1) at **76 of 97 positions, including all 24 crib positions**. They are
  **crib-equivalent** rows, not duplicates. "0 off-target rows" holds under that crib-equivalence definition.
- **`undetermined_key_idx`:** in `results211_scored.json` this field stores the **count** of undetermined key indices on each true line (e.g. A04 `[4]`),
  not the indices. The values quoted above ("0–5") are counts. Cycle 212's scorer calls the field `undetermined_key_idx_count`.
- **Commit-hash erratum.** The local hashes cited in addendum 2 were rewritten when the commits were published (same content, new parents). Map:
  PREREG211 `e358dda` → published **`d543fc5`**; blind results `97a7c8b` → **`dc266c9`**; PREREG211b `f406596` → **`3f30a0a`**. The misstated
  message disclosed above ("parts A/B results not yet committed") is on published commit **`3f30a0a`**. It was not amended (no force-push). This
  addendum is the correction of record.

## Addendum 4 (cycle 213, 2026-11-13): L 17 measured and plant-gated
Text above preserved. 0/100 fresh shuffled-K4 nulls (seed 209221) at L 17 behind `all.bin`, K4 0, 30/30 L 17 plants (seed 209222) on top of
cycle 208's 5/5: **L 17 relabelled `EXCLUDED` (exact, discriminating)** (was `UNRESOLVED`, 1/20). L 18 unchanged.
See [case 199](199-r1-l17-frontier-measured-rate-and-je-relook.md).
