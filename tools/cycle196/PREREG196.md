# Cycle 196 pre-registration — audit: the columnar sandwich under ONE wrong crib letter (IDEAS I-212 via pointer I-211)

Written and pushed **before** any K4 or registered-null run. Everything before this push ran on the reserved shuffle 9191 (I-116), on uniform
random texts or on planted texts; nothing touched K4. Heavy budget ≤ 8 min; ≈ 2.0 min used before this push (structure pass 20 s, control
rehearsal 12 s + bank-level checks 12 s, meter 54 s, pre-K4 recount 2 × 9 s, timings).

## Question (audit of case 182; prior-coverage grep: cases 50, 119, 176–182 and IDEAS I-209/I-212/I-213)
Case 182 excluded the columnar sandwich (keyword pass a, period m → keyed columnar from case 50's 1,837 keyword orders, either direction
(col1, 3,674 rows), or a themed double columnar (col2, 16,928 rows) → keyword pass b, period n; A–Z>KRYPTOS, KRYPTOS>A–Z, A–Z>A–Z,
KRYPTOS>KRYPTOS; Vig/Beau/variant; S1 = a at the plaintext index, b at the carved index; S2 the reverse; 2 ≤ m, n ≤ 26 incl. m = n) only
under the **strict** test. K1–K3 all carry slips; one wrong carved or crib letter in the crib window breaks every crib cycle through its edge.
No case file has run a one-error test behind a keyed columnar with two arbitrary keys (case 181 = K3-law routes only; case 182 = strict).

## Method (exact; solver unchanged)
[`tools/cycle194/cmp194.c`](../cycle194/cmp194.c) **unchanged** (every-slot deletion, 2-core deduplication, bound U, statistic S1; I-202), with
the cycle-195 banks (hashes in [`sha196.txt`](sha196.txt) = [`tools/cycle195/sha195.txt`](../cycle195/sha195.txt) for col1/col2/ctl195).
One-tableau stacks run forms VV/VB only (BB = VV, BV = VB exactly). Decoder [`decode196.py`](decode196.py) and recount
[`recount196.py`](recount196.py) = cycle-194 files unchanged (renamed); checker [`checkctl196.py`](checkctl196.py) = checkctl194 with the bank
as an argument plus the N5 rule; plants [`plant196.py`](plant196.py) = plant194 applied to case 182's plants (plant195.py, seed 19500, re-run
and byte-identical).

## Pair selection (text-free, exact, fixed here)
The cell bound U depends only on the crib graph, so a structure-only pass (mode 2) over the **whole** bank gives the exact cell U per (model,
m, n) (no subsample estimate as in cycle 194): [`struct196.txt`](struct196.txt) (col1 then col2).
Registered: pairs with cell U ≤ 0.05 → [`pairs_fp_col1.txt`](pairs_fp_col1.txt) **139 per model** (8 with m = n, 66 with lcm > 26, up to 105;
Σ U 0.224 per model per tableau setting) and [`pairs_fp_col2.txt`](pairs_fp_col2.txt) **136 per model** (8 m = n, 63 lcm > 26, up to 105;
Σ U 0.293). 22 / 23 pairs per model sit at 0.05 < U ≤ 1 (not registered; → leftovers). Note: S2 at (m, n) has the same crib graph as S1 at
(n, m) (the edge (i mod m, S[i] mod n) is the same bipartite edge), so their U are equal; the ciphers differ (which pass comes first).
**Expected fits under the bound** (all registered cells together): col1 two-tableau 3.58, one-tableau 1.79; col2 two-tableau 4.69,
one-tableau 2.34; total ≤ 12.4 (one-tableau expected far lower, I-205).

## Meter (I-193 / I-205), 40 uniform texts (seeds 19640–19679), col1_m45 (82 rows) and col2_m209 (81 rows), all 625 pairs ([output](meter196_out.txt))
Two-tableau S1 vs U: col1 bands 1–4 z −1.38, −1.21, +1.17, −0.30; col2 −1.07, −1.10, −0.54, −0.37, band 5 one fit vs U 0.053 (S1 1, a single
event at ≈ 5 % probability, disclosed). Fits vs U in bands ≥ 3: col1 45 + 1 vs 39.6 + 1.30 (band 3 above U by 5, S1 52 vs 39.6, z +1.17,
inside noise), col2 34 + 1 + 1 vs 37.0 + 1.37 + 0.05. One-tableau (additive) bands run low and lumpy as in cases 180–182 (col1 band 1 2,342
fits vs U 104,394; band ≥ 3: 0 vs 20.5; col2 likewise), so U is conservative there. The bound tracks the two-tableau counts; labels use U.

## Timing (I-169 / I-180)
Meter rate: 82 rows × 625 pairs ≈ 0.63 s per text for both tableau types. Estimated registered run: C1 ≈ 10 s, C2 ≈ 40 s, grid ≈ 75 s,
recount ≈ 40 s.
**Dead-on-arrival line (I-151):** the registered cells are full power by construction (cell U ≤ 0.05 each); the rehearsal recovered every
one-error plant, so nothing is declared dead on arrival. The 0.05 < U ≤ 1 pairs and the U > 1 pairs are `LOW-POWER` by construction (not run).

## Controls (rehearsed 16/16 before this push; [rehearsal output](controls196_rehearsal.txt); the same script is re-run as the registered control run after this push)
[`run_controls196.sh`](run_controls196.sh), all 625 pairs on ctl195.bin (7 rows), print U ≤ 1 (looser than the registered 0.05, I-214).
Positives (fit at row, tableau pair, reduced form, model, (m, n); deletion of the planted slot reproduces the planted plaintext at every
determined position except the corrupted one): P1–P9 = case 182's P1–P9 (incl. **P5 PALIMPSEST → KRYPTOS keyed columnar → ABSCISSA**,
P4 width-14 ALEXANDERPLATZ, P6 double KRYPTOS+PALIMPSEST, P8 m = n, P6/P7 one-tableau, P3/P9 model S2), each with one wrong carved crib letter
(+7) on a 2-core slot. P0 = P1 without error (strict fit). **PD = P1 with the wrong letter on pendant slot 0: strict fit, reported as an
undetectable error** (rehearsal: the strict decryption is wrong at 8 positions, the pendant edge's residue class). Negatives (no fit with
U ≤ 1e−4 at the row): N1 three passes, N2 random key, N3 = P1 with two wrong letters (slots 1 and 2), N4 a case-178 compound key; **N5 the
K3-route sandwich: no fit at any columnar row** (its own route row reported). Bank-level: **P5 with one wrong letter on all 3,674 rows of col1
(registered pairs, print U ≤ 0.05): rehearsal found it at row 0 (config U 1.3 × 10⁻⁶) plus 3 chance fits on other rows** (2471 15 × 2 U
2.9 × 10⁻⁸, 1086 6 × 12, 2294 6 × 13; one-error chance fits at the bound rate — the reason every fit is decoded); P6 with one wrong letter on
all of col2 at its (low-power) pair 3 × 25: found at row 2.
**Rehearsal notes (disclosed):** reported slots are the first of a deduplicated 2-core (P1 4 for 5, P3 4 for 23, P4 1 for 4, P6 3 for 22;
I-195); the rehearsal printed the P5 bank check at U ≤ 1e−6 first, which hid P5's own row (config U 1.3 × 10⁻⁶ under one
error; the I-214 lesson again), so the script now prints at the registered 0.05; P6/P7/P9 show equivalent cells (period multiples, swapped models in one-tableau stacks), listed not counted. The pre-K4 recount script
first interleaved the stdout of its two parallel recount processes (spurious "DIFFER"); fixed by writing separate files, then identical.

## Pre-K4 exactness recount
[`prercount196.sh`](prercount196.sh): recount196.py (literal tables, all 25 deletions, no reduction; no shared code) vs cmp194 on a uniform
random text (seed 19640), ctl195 rows 0 (col1) and 4 (col2), all 1,250 model-pairs, tab2 × 4 forms + tab1s × VV/VB: **13,712 fits identical**.

## Registered run ([`run_cycle196.sh`](run_cycle196.sh))
- **C1** K4, all 3,674 rows of col1, pairs_fp_col1, tab2 (4 forms) then tab1s (VV/VB), S1 + S2; print every fit with config U ≤ 0.05
  (so every fit of a full-power cell is printed).
- **C2** K4, all 16,928 rows of col2, pairs_fp_col2, same.
- **Grid** K4 + 19 shuffles (seeds 19611–19629, [`nulls196.txt`](nulls196.txt), `random.Random(seed).shuffle(list(K4))`), tab2 + tab1s on
  col1_s8 (= col1.bin[::8], 460 rows), **all 625 pairs**; budget gate: starts only if elapsed ≤ 150 s.
- **Recount** recount196.py vs cmp194 (all fits) on ctl195 (7 rows), **all 1,250 model-pairs**, tab2 × 4 + tab1s × 2, texts K4, P1, P5, P6,
  n19611: fit sets identical.

## Labels (as cycles 192–195)
Cell = (bank, model, tableau pair, form, m, n) over the whole bank. Cell U ≤ 0.05 = full power (one-error scope): K4 0 fits →
**`EXACT-EXCL` (one-error)**; any fit there is decoded with `decode196.py` under every consistent deletion before any label. A solution needs
a full coherent English 97-letter decryption with EASTNORTHEAST (0-based 21–33) and BERLINCLOCK (0-based 63–73) at the official positions,
reproducible. Fits that decode to gibberish with a total at or below the bound → **`EXACT-EXCL` (one-error scope; chance fits decoded and
rejected)**. A total clearly above the bound (Poisson p < 0.01 against Σ U) would be reported as an excess and not labelled until decoded and
checked against shuffles. U > 0.05 (not run) → **`LOW-POWER`**. Grid: p⁺ = (1 + #nulls ≥ K4)/20, floor 0.05, rank flag only (I-182/I-203:
a flag goes to a pooled reference, not a claim). Missing `END` = not run.

## Not covered (stated in advance)
Pairs with cell U > 0.05 under one error; themed × {A–Z, KRYPTOS} tableau pairs (case 182's C3) under one error; two or more wrong letters;
dropped/extra letters (I-196); double columnar beyond themed × themed; disrupted/Myszkowski columnars (I-213); m or n = 1 or > 26; three passes.
