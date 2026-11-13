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
