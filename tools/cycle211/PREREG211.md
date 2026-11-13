# PREREG211 — blind aligned-stratum plant gate for case 195 (I-280, audit slot) + million-plant JEX look at P 8 (I-279 add-on) (cycle 211, 2026-11-13)

Written 2026-11-13 ~11:47 PT (America/Vancouver), base commit 31635a4 (local; upstream main still d1f3853), **before any plant in
this cycle was run and before the sealed truths were opened**.

## Part A — I-280: 20 blind aligned plants behind `all.bin` (Voynich desk)
**Why.** The case 195 coverage audit (Voynich desk, cycle 209 addendum) found the cycle-208 plants were 53/55 mid-block and only 2/55
grid/block-aligned, so case 195's L 16 exclusion was validated mid-block and only weakly (2/2) on aligned crib boundaries.

**Input (not ours; treated as data to verify).** Box-local `voynich/kryptos-audits/case195-aligned-plants/ciphertexts.txt`, copied
verbatim here as `plants211_ciphertexts.txt`, sha256 `e2466b0e85dd5d94c9a704182242f5c4b8eabe5942f96975760ca3299845f9d3` (matches her
SHA256SUMS). 20 plants A01–A20, her seed 6429. Sealed truths: `sealed/truths.json`, sha256
**`da448d894dc4225ee1f702f0c111112685a21a662e10f09af6889d2a751189b7`**. Her stated design: stratum EAST|NORTHEAST + BERLINCLOCK, every
plant block-aligned at layer index 25 under the case 195 coverage definition; 10 decimations + 10 routes (fill-mode quota 3/4/3); L 16;
model Q (R1 word restart in plaintext order, then `C[S[i]] = layer[i]`, S = row or its inverse); o1, o2 uniform 0..8 (9 plants with
o2 ≥ 6, BERLINCLOCK key indices wrap mod 16); AZ Vig / AZ Beau / KA Vig / KA Beau; English filler (Gutenberg #1661).

**Solver.** `tools/cycle206/wrbank.c` **unchanged** (sha256 1001272d…, gcc -O3 -march=native -fopenmp), full `all.bin`
(sha256 8a9e1b32…, 165,782 rows, both directions), L 16 only, all segmentations and offsets, print every survivor
(`blind211.py`). G0 checked before registration: direct K4 reproduces case 190 (0 at L ≤ 22; 2 / 184 / 414 / 692 at L 23–26, doubled-Vigenère).

**Order (blind).** (1) commit this file; (2) run `blind211.py`, write `results211_blind.json` + its sha256 into the run log and commit;
(3) only then open `sealed/truths.json`, check its sha256 equals the hash above (mismatch → NO VERDICT), score with `score211.py`.

**Detection rule (same as PREREG208 / case 195).** A plant is recovered when a survivor line exists at the true (row, dir, tm, L = 16,
segE = EAST|NORTHEAST, segB = BERLINCLOCK, o1, o2) whose key agrees with the planted key at every determined index ('?' = undetermined).
The tableau/form index maps AZ Vig/Beau/KA Vig/Beau → tm 0/1/2/3; a planted Vigenère may also match its variant twin as printed by
wrbank (counted once). Descriptive only: hits at an equivalent configuration (duplicate row, or inverse row with the other direction).

**Gate.** ≥ 19 / 20 recovered → case 195's L 16 exclusion is plant-validated on the aligned EAST|NORTHEAST + BERLINCLOCK stratum
(both sub-strata reported separately; ≥ 9/10 each is descriptive). ≤ 18 / 20 → FAIL: the aligned stratum is not validated, each miss
is diagnosed, and no case 195 claim is widened. Clopper–Pearson 95 % interval reported. No statistical claim beyond this count.

## Part B — I-279 add-on: worst-model JEX q at ≥ 10^6 plants, 85-ban C4 mask, P 8 (`c4look211.py`)
Gates M (1,517 / 1,513 cells, forced {35,41,43,46,61,78}), R1 (case 196 JEX tag-10 q 0.0074993 exactly, 81-ban), R2 (cycle 210 JEX
tag-10 q 0.0056994 exactly, 85-ban). Fresh seed block **209216** (pool + plants), JEX only (all other models were below JEX at 10k in
cycle 210), chunks of 160,000 (tags 20–35). Looks at n = 640,000 and 2,560,000; stop at the first look with |q − 0.00625| ≥ 2 SE.
q ≤ bar − 2 SE → STAT-DISFAVOURED (Quagmire IV at P 8 under the JEX model); ≥ bar + 2 SE → LOW-POWER; still inside → UNRESOLVED.
Wall cap 330 s inside the script; if look 2 is not reached, the label says so. Next free seed after this cycle: 209217.

## Budget / process
≈ 8 min heavy compute in one owned process group (setsid + timeout); nothing outside the group touched. Nothing here is a solution
claim: a solution must be a full 97-letter coherent English decryption with both cribs at their official positions.
