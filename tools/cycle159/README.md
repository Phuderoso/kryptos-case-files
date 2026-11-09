# Cycle 159 — cycle-rank-matched nulls for Periodic Gromark L 8 one-error survivors (IDEAS I-057)

No new solver: the cycle-155 program `tools/cycle155/gromark1e.c` (model P, unchanged; binary identical to cycle 157's build) is rerun
on new nulls matched to K4 on **both** the crib-letter repetition profile and the **cycle rank r = 6** of the L 8 crib graph.
- `mknulls159.py` — rejection sampling of K4 shuffles (seeds from 15900000): profile 3-2×8-1×5 (14 distinct) and r8 = 6.
  48 accepted of 19,350 shuffles (135 profile-matched, 48 of those also r-matched). Prints r at L 9, 11, 12 for reference.
- `plant159.py` — four quick planted model-P L 8 encryptions (random alphabet, free group offsets): carved error (AZ/Vig, KA/Vig),
  wrong crib letter (KA/Beau), clean (AZ/Beau).
- `run_cycle159.sh` — resumable runner (finished chunks skipped; `ONLY=` restricts). Jobs run **quarter-major** (primers 0–25M of
  every null first, then 25–50M, …) so a budget stop leaves a primer range common to all nulls.
- `summarize159.py` — K4 vs nulls on the chunks listed in `LOS` (default all four): min / median / max, empirical
  p_upper = (1 + #{null ≥ K4}) / (N + 1), optional pooling with the cycle-157 r = 6 nulls, Bonferroni ×4 note.
- `indep159.py` — pure-Python recount on a primer window (loads `ok()` from `tools/cycle155/indep_check.py`; all 24 drops, BFS,
  no code shared with `gromark1e.c`).

## Reproduce
```
W=/tmp/w159 REPO=$PWD bash tools/cycle159/run_cycle159.sh          # full 48 x 10^8 primers ~13 min on 8 cores (resumable)
cd /tmp/w159 && LOS=0,25000000 python3 $REPO/tools/cycle159/summarize159.py results_raw.txt nulls.txt 10        # primary
python3 $REPO/tools/cycle159/summarize159.py results_raw.txt nulls.txt 28 1,2,2,5                                # full range
python3 $REPO/tools/cycle159/indep159.py $(cat ct_rnull02.txt) 8 rnull02 25151354 25171354
```
