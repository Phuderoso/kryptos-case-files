# PREREG213 — cycle 213 (2026-11-13, ~19:55 PT), audit slot

Filed before any part below was run. Slots: 211 audit, 212 new family (I-284), so 213 is free (pointer I-289); **cycle 214 must be a new family**
(I-290 or a family absent from the coverage table). I-292 (aligned bank plants with offsets) waits on the Voynich desk: no plants delivered yet.

## Part A — I-288: JE re-look at P 8 (case 196)
- Tool `c4look213.py` = `tools/cycle211/c4look211.py` with only: model JE instead of JEX for the main run, seed block **209220** (fresh).
  Gates unchanged: M (1,517 / 1,513 cells, forced {35,41,43,46,61,78}), R1 (seed 209211 JEX tag-10 q 0.0074993 exactly), R2 (seed 209212
  JEX tag-10 q 0.0056994 exactly). Looks at 640,000 and 2,560,000 plants, stop at |q − 0.00625| ≥ 2 SE.
- Labels as cycle 211: q ≤ bar − 2 SE → `STAT-DISFAVOURED (model JE)`; ≥ bar + 2 SE → `LOW-POWER`; else `UNRESOLVED`.
- Expected (not a gate): JE was 0.0050 ± 0.0007 at 10k (cycle 210), below JEX, so a P 8 verdict should not change; this run only closes I-288.

## Part B — I-277: the L 17 R1 frontier with a measured chance rate
- Unchanged `wrbank.c` (sha256 1001272d…, `tools/cycle206/`), L 17 only, behind the bank (`bank.bin`, 165,065 rows, sha 004ffc24…) and the
  K3-law decimations/routes (`all.bin`, 165,782 rows, sha 8a9e1b32…), both directions, all segmentations and offsets, as cases 193/195.
- **G0:** K4 gives 0 cells at L 17 in both families (reproduces cases 193/195). Fail → no label.
- **Nulls:** 100 fresh shuffled-K4 ciphertexts, `random.Random(209221)` (the i-th shuffle of K4), each run behind both families
  (`null213.py`, 6 workers, resumable JSONL checkpoint, wall cap 420 s; unfinished nulls carry to cycle 214 under the same seed and are labelled
  `INCOMPLETE` until n = 100).
- **Labels per family (I-281 boundary band, α = 0.05):** k = 0 / 100 → L 17 exclusion `DISCRIMINATING` (rule-of-three upper bound 3 %);
  p ≤ α − 2 SE → `DISCRIMINATING`; p ≥ α + 2 SE → `NOT DISCRIMINATING`; otherwise `UNRESOLVED`. Fresh nulls alone decide; the earlier
  nulls (bank 1/40, decimations 1/20) are pooled only descriptively.
- **Blind spot, stated now:** no planted key at L 17 is run in this cycle. The solver is plant-validated at L 16 (cases 194/195: 20/20, 10/10,
  48/48 mid-block) and the L loop is the same code; an L 17 exclusion label is read within that scope.
- Null survivor cells are also reported as distinct configurations where the S lines allow it (I-291, descriptive).
