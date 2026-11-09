# Case file 155 — Segment-shifted period-7 key: one keyword, shifted per sentence (cycle 167)

**Status:** negative. **Type:** variant/audit (cycle 166 opened a new family). IDEAS **I-082** (follow-up of I-070,
[case 154](154-three-segments-returning-key.md)), plus the **I-078** run-folder sweep. One period-7 key shifted by a constant in each
of three segments (k | k + d2 | k + d3) is `EXACT-EXCL` for all 86,731 Quagmire-III alphabets directly (strict and one error),
behind the whole 165,065-entry bank for A–Z/KRYPTOS (strict and one error), and with all alphabets on 1/4000 of the bank.
Every cell has K4 0 and nulls 0. The I-078 sweep found no other run that was declared unfinished but had in fact finished.

## 1. Why this, and why it is a variant
Case 154's three independent keys (model T) had no power: each segment frees 7 key values, leaving as few as 4 crib checks.
A clerk who keeps one keyword and moves to another row of the tableau at each sentence frees only 2 values (the shifts), so the
test regains power. This model is a strict sub-model of T with the forms held fixed (k2 = k1 + d2, k3 = k1 + d3). It is therefore a
variant of case 154, not a new family. Two-segment shifts (k | k + d) are already inside case 150 (two independent keys, exact),
and a single key is case 123. Here they are flagged as degenerate (`deg`) and expected to be 0.

Chosen over I-072 (S1e null lineup, ~35 min over several cycles, can only re-rank decoded gibberish) because I-082 is P2, cheap,
and closes the one power gap that case 154 left open. The I-078 sweep is a few minutes of reading and ran alongside.

## 2. Model
- Index positions 0–96: direct, plaintext index behind a bank permutation (model Q), or carved index (transpose first). The key
  letter is chosen by index mod 7, phase from position 0 (as in cases 150/154).
- One keyed alphabet A on both sides (Quagmire III), all 86,731 of `alpha.bin` (0 = A–Z, 1 = KRYPTOS).
- Segments [0, b1) | [b1, b2) | [b2, 97), boundaries free (also inside a crib). Segment j uses key value k[i mod 7] + d_j in
  A-index space (d_1 = 0). Moving the key by d along the keyed alphabet is the same as reading the next rows of the Kryptos tableau.
- Form per segment: Vigenère (A⁻¹(c) − A⁻¹(p); variant Beaufort has the same consistency) or Beaufort (A⁻¹(c) + A⁻¹(p)).
  **Primary S:** the same form in all segments. **Secondary SM:** mixed forms (6 more triples).
- A fit counts as three-segment only if every segment holds at least one crib letter.

## 3. Exact test (`tools/cycle167/shift3.c`)
Each crib gives k[r] + d_s = v. The tool solves this with union-find with offsets mod 26 over 7 key nodes and 3 shift nodes.
It is exhaustive over every boundary pair in crib order, so every b1 ≤ b2 in 0..97 is covered. The prefix and middle are
built incrementally and checked with early exits. Leave-one-crib-out (`drop`) gives the one-error test.

**Power** ([`power.txt`](../data/cycle167/power.txt)): at the direct crib positions every three-segment boundary pair keeps
**≥ 15 checks** (24 equations, rank ≤ 9). Union bound 1.5 × 10⁻¹⁹ per alphabet and triple → 1 × 10⁻¹³ chance fits per text over
86,731 alphabets × 8 triples. On 300 random 24-position layers the minimum is also 15 → ~1.6 × 10⁻¹² chance fits per text behind
the whole bank for A–Z/KA. One error leaves ≥ 14 checks. A K4 fit would therefore be strong evidence. Compare model T: 4 checks.

## 4. Runs (4 min 57 s wall, 8 processes, 01:18:22–01:23:19 PDT; [`run_cycle167.sh`](../tools/cycle167/run_cycle167.sh))
Texts: K4, 4 shuffled nulls and 20 profile-matched nulls, the same 24 nulls as cycle 166 ([`texts167.txt`](../tools/cycle167/texts167.txt)).

| cell | scope | S (same form) | SM (mixed forms) | deg | label |
|---|---|---|---|---|---|
| D | direct, 86,731 alphabets, 25 texts | K4 **0**, nulls 0/24 | K4 **0**, nulls 0/24 | 0 | `EXACT-EXCL` |
| D1e | direct, leave-one-crib-out × 24, 86,731 alphabets, 25 texts | K4 **0**, nulls 0/24 | K4 **0**, nulls 0/24 | 0 | `EXACT-EXCL` (one error) |
| BA | full bank (660,260 configs per text), A–Z/KRYPTOS, 25 texts | K4 **0**, nulls 0/24 | K4 **0**, nulls 0/24 | 0 | `EXACT-EXCL` |
| BE | full bank, A–Z/KRYPTOS, leave-one-crib-out × 24, K4 + null1 + mnull01 | K4 **0**, nulls 0/2 | K4 **0**, nulls 0/2 | 0 | `EXACT-EXCL` (one error) |
| BS | q ≡ 0 mod 4000 (42 perms, 168 configs), all 86,731 alphabets, K4 + 4 nulls | K4 **0**, nulls 0/4 | K4 **0**, nulls 0/4 | 0 | `EXACT-EXCL` on the sample |

Counts: [`summary_counts.txt`](../data/cycle167/summary_counts.txt). All 1,029 H lines: [`H_lines_all_runs.txt`](../data/cycle167/H_lines_all_runs.txt).
No slice printed a single fit (S) line. Run-folder audit (I-078): [`run_provenance.txt`](../data/cycle167/run_provenance.txt):
227/227 slices finished, 0 `.tmp`, done marker present.

**False-positive gate (I-079).** Every cell has 0 nulls with any fit (0/24, 0/24, 0/24, 0/2, 0/4), so the gate passes wherever it
applies. Here the gate is not what carries the result: the analytic bound (≥ 15 checks) already puts the chance rate near 10⁻¹³.
The small-null cells (BE, BS) rest on that bound, not on null counts. Voynich's C078 (see journal) warns that a 20-replicate gate
is itself noisy (8.3 % observed against 5 % nominal). That matters for count cells like I-072. It does not matter here.

## 5. Controls
- [`plant167.py`](../tools/cycle167/plant167.py) is an independent textbook encryptor. It made 18 shifted-key plants (direct,
  model Q and carved; A–Z, KRYPTOS and random dictionary alphabets; same-form and mixed triples; boundaries random, some inside
  a crib, every segment holding a crib; d2 ≠ d3, both non-zero). **18/18 recovered** with the true alphabet, triple and layer.
- 4 one-error plants (one carved letter under a crib altered): **4/4 recovered** in drop mode, and 0/4 in strict mode with the
  true alphabet. Strict mode is correctly broken by the error.
- 4 decoys with three independent keys (case 154 model T, A–Z/KA, Vig and Beau): **4/4 rejected** (no shifted-key fit).
  Total **26/26** ([`controls167.txt`](../data/cycle167/controls167.txt)). The solver is exact, so plant strength is binary (power 22/22 ≥ 9/10).
- Independent recount [`recount167.py`](../tools/cycle167/recount167.py) uses numpy over all 26 × 26 shift pairs and every boundary
  pair, with no union-find. It covered the 26 plants × 8 triples, K4, null1 and mnull01 directly on 12 alphabets × 8 triples, and
  K4 at 4 bank configurations on A–Z/KA. **560/560 cells identical** in the number of three-segment boundary pairs
  ([`compare167.txt`](../data/cycle167/compare167.txt)).
- Consistency with case 154: the same-form model S is a subset of model T, so S fits must sit inside T's fits. T had 10 direct /
  66 bank A–Z/KA fits for K4, and S has 0. Consistent. `deg` = 0 everywhere agrees with cases 123 and 150.

## 6. Crib and English checks
No K4 configuration survives in any cell, so there is nothing to decrypt. The plants decrypt to their planted English (all 24 crib
letters reproduced by construction of the recovery check). No coherent 97-letter English, and no candidate.

## 7. I-078 sweep (run-folder audit of past "stopped / unfinished" claims)
[`i078_sweep.txt`](../data/cycle167/i078_sweep.txt): every "stopped / unfinished / not run / budget" statement in cases 139–154
and the journals of cycles 151–166, checked against the run folders on the box:
- Case 147 (cycle 159) null-major stop: the folder holds 122 completed chunks of 192; case 147 lists exactly 70 remaining, and
  those were finished in cycle 161 (192 C lines, case 149). Nothing orphaned.
- Case 149 (cycle 161) "L 9 nulls saved but not run" and case 145 (cycle 157) "L 9 / L 12 not run": no result files exist. Correct.
- Case 152 (cycle 164): the known false "unfinished", already corrected in case 153.
- Cases 141–143, 148 and 150: their "not run" items are scope limits with no runs behind them.
**Result: no further orphan results.** I-078 is closed as a sweep, and the rule stays in force.

## 8. What this excludes and what it doesn't
Excluded (exact, under the model):
- One period-7 keyword shifted by a constant per segment (three segments, any boundaries), same or mixed Vig/Beau per segment,
  one shared Quagmire-III alphabet out of 86,731, directly, strict and under one crib/carved error.
- The same behind all 165,065 bank permutations (both directions and both index orders) for A–Z/KRYPTOS, strict and one-error,
  and for all alphabets on q ≡ 0 mod 4000 (≈ 0.025 % of the bank).

Not excluded:
- All alphabets behind the rest of the bank (I-084; ~1 core-s per configuration now).
- A shift taken in plain A–Z letter space and then read through a keyed alphabet. This differs from the tableau-row shift except
  for A–Z (I-083).
- 4+ segments (I-081), phase restarts at the boundary, periods other than 7, and Quagmire I/II/IV tableaux per segment (I-071).

## 9. Reproduce
`gcc -O3 -march=native -o tools/cycle167/shift3 tools/cycle167/shift3.c`, then `tools/cycle167/controls167.sh`,
`python3 tools/cycle167/checkctl167.py`, `tools/cycle167/run_cycle167.sh`, `python3 tools/cycle167/summarize167.py RUN` and
`python3 tools/cycle167/compare167.py` (inputs `alpha.bin` and `perms97.bin` from the support backup).
