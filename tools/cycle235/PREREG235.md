# PREREG235 — cycle 235 (audit slot): I-364 / I-356, the case 218 NC bar on a hit-rich surrogate of the gn217 family

Filed 2026-11-22 ~11:55 PT, before any plant, fresh-null or K4 run with this tool. Base: origin/main a0bb734 (c234 published by Firefly;
local e1e4acc has the identical tree d181adc).

## Why (and whose idea)
Case 218 adopted the NC bar bar(nq, N) = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² − 0.0192 nq + 0.879 for families that print Y lines,
fitted in the case 213 (keyboard, kb229) family only. I-356 asks whether it holds in another family; I-364 asks to exercise it on
gn217. **Voynich's blind run on c233 (freeze f58e6e1, result 779f465, voynich-case-files) came back NOT TESTABLE**: the 23/24-seat filter
gives 0 H lines on K4 and on the null, so no decrypt exists to score. Her note (kryptos-notes/2026-11-22-I364-note.md) proposes the design
used here: a fixed crib subset (the 8 index seats, 0–3 and 13–16, hit = 8/8), ≥ 21 fresh nulls in two disjoint sets, decrypts printed
with NC / nq and N per scope. `[external audit]` design credit: Pimpolha Voynich. Parameters below are mine.

## Tool
`gn235.c` = gn217 (sha 97bae55f…) with the hit rule changed to 8/8 on the index seats (EAST at 21–24, BERL at 63–66); every hit is
decrypted in full (97 letters) and scored with NC over quadgrams touching no crib position (nq = 64 always), table `qg.bin`
(sha 4a02ba4e…, = quadgrams.json to 2.8 × 10⁻⁷). agree24 printed. Windows **keys233.bin** (case 219, 4,172 windows, sha 4d03ca5b…);
scopes direct (alpha.bin, full), bank.bin r10, all.bin r10 (themed144.bin). One timing smoke on the already-published null 209646
(case 220's null; not a fresh seed): direct 430 / bank r10 73 decrypts, max NC −7.49 / −7.61, ~10 s. Not part of any result.

## Seeds
Fresh nulls set A **209647–209658**, set B **209659–209670** (`random.Random(seed).shuffle(list(K4))`, `mknull235.py`);
plants **209671** (`plant235.py`). **Next free seed 209672.**

## Hypotheses and decision rules (as in `analyze235.py`)
- **Unit** (text, nq 64) pooled over the 3 files: N = decrypts, max = best NC. Per-text pass ⇔ N ≥ 10 and max ≥ bar(64, N).
- **H1 (primary):** per-text passes among the 24 fresh nulls. **HOLDS** if ≤ 3/24 (P(≥ 4 | 1/21) = 0.025), **FAILS (too permissive)**
  if ≥ 4/24; robust only if sets A and B fall on the same side (≤ 2/12 each), else FRONTEIRA. Wilson 95 % printed.
- **H2 (secondary):** null R_t = max − fit(64, N) vs the 20 case 218 calibration R_t (summary232.json): two-sided Mann–Whitney,
  Hodges–Lehmann shift with bootstrap CI. p < 0.05 with negative shift ⇒ "bar conservative in this family by |shift|" (a power note).
- **Gate P:** 20 plants (8 direct, 6 bank, 6 all.bin; odd ids one carved letter wrong at a random **non-crib** position, since the 8/8
  surrogate needs the index seats intact and NC ignores crib positions): recovered with the planted configuration and NC ≥ bar(64, N_K4)
  for ≥ 18/20; one-error count reported.
- **Gate T:** `check235.py` (independent Python decrypt + NC from quadgrams.json) mismatches 0 on every K4 file, the first null of each
  set and every plant file.
- **K4 arm (descriptive):** K4 unit N, max, R, rank p among the 24 nulls. A surrogate hit can only agree on 8 seats; case 219 already
  has K4 at 0 hits ≥ 23/24 for these windows, so no K4 surrogate decrypt can be a solution. Any K4 pass is printed as a lead and checked.
- No verdict on K4's key family changes in this cycle. Budget ≤ 8 min wall, own process group.

## Publication
Y / T lines and all H lines for K4 and the 24 nulls (`data/cycle235/R`), plant files, summary235.json, SHA256SUMS. The 32 MB
permutation / alphabet files stay unpublished (sha256 listed; same files as cases 217–220).
