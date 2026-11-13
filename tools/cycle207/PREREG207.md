# PREREG207 — stratified L 16 plant gate for case 193 (I-272, Voynich desk design)

Written 2026-11-12 19:48 PT (America/Vancouver), before any plant is generated or run. Base commit c9edc38.

## Why
Voynich's desk audit of case 193 (`/workspace/voynich/kryptos-audits/c206-r1-bank/plan_followup.md` + `results.md`, box-local, not yet in
this repo) found that 87.2 % of (bank entry, crib segmentation) pairs put a word boundary in the middle of a transposition block (a written
row of the family grid of width w; boundary b is mid-block iff b % w != 0), 0.30 % are grid-aligned with an internal boundary, and the
cycle-206 plants covered only L 8 / L 10, both mid-block (2 / 2), none aligned, none at L 16 / 17. So case 193's L <= 16 zero is an exact
full-bank count but was **not** plant-validated at L 16 and never planted on the aligned case. This cycle runs the gate she proposed.

## Tool and bank
Unchanged `tools/cycle206/wrbank.c` (recompiled, gcc -O3 -fopenmp), bank `perms97.bin` sha256 prefix 004ffc248d17e1a3 (165,065 entries,
cycle-19 family in `k4_autokey_trans.family(97)` order plus identity at 0). No edits to the solver.

## Plants (seed 206207, as reserved by the desk; next free seed recorded in the results)
Invented example plaintexts (not K4 guesses), cribs at 0-indexed 21-33 / 63-73, first crib word and BERLIN... word start a word (o1 = o2 = 0):
- **Stratum M (mid-block), n = 20, L = 16:** C1 template (... TURNED EAST NORTHEAST OVER ... THAT BERLIN CLOCK WAITING ...), true
  segmentation EAST|NORTHEAST + BERLIN|CLOCK (boundaries 25, 69, mid-block for every non-identity entry). Entry drawn uniformly from the
  165,064 non-identity entries.
- **Stratum A (grid-aligned), n = 20, L = 16:** same template with EASTNORTH EAST and BERLINCLOCK as words, true segmentation
  EASTNORTH|EAST + BERLINCLOCK (boundary 30). Entry drawn uniformly from non-identity entries whose every component width divides 30
  (widths read from the family tag exactly as in the desk's `followup_blocks.py`).
- In each stratum, tableau/form cycles AZ Vig, AZ Beau, KA Vig, KA Beau (5 each; superset of the desk's "one KA Vig and one AZ Beau"),
  direction dir 0 / 1 drawn uniformly, key = 16 uniform random letters.
- **Optional L 17:** 5 mid-block plants (same rules), threshold 5 / 5, descriptive; does not replace the L 16 gate.

## Detection rule (fixed)
Run `wrbank CT perms97.bin L L 1000000` on the full bank. A plant is **recovered** iff a survivor line exists with the true perm index,
dir, tm, L, segE, segB, o1 = o2 = 0, and its key agrees with the planted key at every determined index ('?' = undetermined).
## Gate
Each L 16 stratum passes iff >= 19 / 20 recovered; **both** must pass (exact power P(X >= 19 | Bin(20, p)) = 1 / 0.983 / 0.736 at
p = 1 / 0.99 / 0.95). Failure of either stratum means case 193's L <= 16 exclusion may not be cited as tool-validated on that stratum and
the tool is debugged before any further use behind the bank. Pass or fail, the K4 count is not reopened here.
Also recorded per plant: total survivors at that L (false-cell load), descriptive.

## Budget
45 full-bank single-L runs, est. < 2 min on 6 threads; cap 6 min wall; process group owned by the harness.
