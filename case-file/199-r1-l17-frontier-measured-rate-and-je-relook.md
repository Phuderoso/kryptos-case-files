# Case 199 — The L 17 frontier, measured; and the JE re-look at P 8 (cycle 213, audit)

**Slot:** audit (211 audit, 212 new family, 213 free per I-289; **214 must be a new family**). Pre-registered in
[PREREG213](../tools/cycle213/PREREG213.md) before any part ran; part C added as PREREG213b after A/B finished and before C ran.
Ideas closed: **I-277** (L 17 part), **I-288**. Code and raw results: [`tools/cycle213/`](../tools/cycle213/).

## Part A — I-288: model JE at P 8 (case 196, 85-ban C4 mask)
- `c4look213.py` = `c4look211.py` with only the model (JE for the main run) and a fresh seed block 209220 changed.
- Gates: M (1,517 / 1,513 allowed cells, forced {35,41,43,46,61,78}) **pass**; R1 (case 196 JEX tag-10 q 0.0074993) and R2 (cycle 210 JEX
  tag-10 q 0.0056994) reproduced **exactly**. Key pool 256/256 distinct.
- First look, n = 640,000 plants: **q = 0.003642 ± 0.000075** vs bar 0.00625 → **`STAT-DISFAVOURED` (Quagmire IV at P 8, model JE)**.
  Wall 38 s.
- Reading: JE sits well below the worst model (JEX, 0.00573 ± 0.00009, cycle 211), so the P 8 verdict does not rest on the worst-model
  choice made at 10k. Nothing else about case 196 changes. This is a statistical label under the registered plaintext models, not an
  impossibility claim for Quagmire IV at P 8.

## Part B — I-277: the R1 L 17 frontier with a measured chance rate
- Unchanged `wrbank.c` (sha256 1001272d…, `tools/cycle206/`), **L 17 only**, behind the 165,065-row bank (`bank.bin`, sha 004ffc24…) and the
  165,782 K3-law decimations/routes (`all.bin`, sha 8a9e1b32…), both directions, case 190 segmentations, all offsets, AZ/KA × Vig/Beau.
- **G0:** K4 gives **0 cells at L 17 in both families** (reproduces cases 193/195).
- **Nulls:** 100 fresh shuffled-K4 ciphertexts (`random.Random(209221)`), each through both families (`null213.py`, 6 workers, 136 s).

| family | K4 at L 17 | fresh nulls with ≥ 1 survivor | p ± SE | registered label |
|---|---|---|---|---|
| bank (case 193) | 0 | **1 / 100** (null 58: 8 cells) | 0.010 ± 0.010 | **L 17 exclusion `DISCRIMINATING`** (p ≤ 0.05 − 2 SE) |
| decimations/routes (case 195) | 0 | **0 / 100** | 0 (rule-of-three ≤ 3 %) | **L 17 exclusion `DISCRIMINATING`** |

- Descriptive pooling with earlier nulls (not used for the label): bank 2 / 140, decimations 1 / 120.
- **Cluster-aware reading (I-291, descriptive):** null 58's 8 cells are 4 inverse-twin pairs on rows 74,781–77,662, all KA-Beaufort,
  EASTNORTH|EAST + BERLINCLOCK, o1 10, o2 4, with 4 keys that agree on 10 of 17 letters (e.g. `WNDUZSJGQZOVMFDCO`) — one near-equivalent
  cluster, not 8 independent hits.

## Part C — PREREG213b: L 17 planted controls on both families
- `gate213.py` = cycle 208's `gate208.py` (invented templates M/A/O, random 17-letter keys, all 4 tableau modes) with L 17, 10 plants per
  stratum, seed 209222. **Disclosure:** PREREG213b said the row index is drawn from the bank's row count and applied to each file; in fact the
  unchanged gate logic draws it from the row count of the file it is given, so the two runs share the RNG seed but not the exact rows. The
  pass rule is unaffected.
- **bank: 30 / 30 recovered** (survivor lines per plant median 72, max 2,880 — twins and near-equivalent rows); **all.bin: 30 / 30**
  (median 30, max 72). Both **PASS** (≥ 29/30). With cycle 208's 5/5 on `all.bin`, L 17 recovery is now plant-shown on both families.

## Verdict and scope
- **R1 (word-restart key, single AZ/KA tableau, Vig/Beau) behind the bank: `EXCLUDED` (exact) at L 1–17**, now discriminating at L 17
  (measured chance rate 1 %, boundary band clear) and plant-gated at L 17 (30/30). Was `UNRESOLVED` at L 17 since cycle 209.
- **R1 behind the K3-law decimations/routes: `EXCLUDED` (exact) at L 1–17**, discriminating at L 17 (0/100) and plant-gated (30/30 + 5/5).
- **Unchanged:** L 18 behind the bank stays `NO-DISCRIMINATION` (K4 has one gibberish configuration there, case 193); L 18 behind the
  decimations stays not excluded (6/20 nulls, case 195). Exact under the stated assumptions: the plaintext word boundaries fall in one of the
  case 190 segmentations of the cribs, no wrong crib letter, transposition inside the bank / K3-law family. L 17 controls are all mid-block
  or offset templates from cycle 208's design; the grid-aligned bank population with wrapped offsets is still unplanted (I-292).
- **No solution.**
