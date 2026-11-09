# Cycle 157 — structure-matched nulls for the strict / one-error Gromark tests (IDEAS I-052)

No new solver: the cycle-155 program `tools/cycle155/gromark1e.c` (model P, unchanged) is rerun on new **nulls**.
- `mknulls157.py` — shuffles of K4 accepted only if the 24 cipher letters under the cribs have K4's exact repetition profile
  (14 distinct; multiplicities 3, 2×8, 1×5). 20 accepted of 2,915 shuffles (seeds from 15700000).
- `run_cycle157.sh` — resumable runner (finished chunks skipped; `ONLY="mnull01 …"` restricts a resume). Jobs: every matched null for
  model P digit primers L 2–8 and rank primers L 8–11 (full sets); K4 L 8 digits and L 11 ranks rerun as a regression.
- `summarize157.py` — K4 vs the matched nulls per (L, primer set): min / median / max, number of zero nulls, empirical upper tail
  p = (1 + #{null ≥ K4}) / (N + 1).
- `structure157.py` — cycle rank r = edges − nodes + components of the crib graph (cipher-letter nodes ↔ group-offset nodes) at each L;
  each independent cycle is one mod-26 filter on the digit stream, so r governs the chance survivor count.
- `indep157.sh` — independent checks: profile of every null recomputed; pure-Python `tools/cycle155/indep_check.py` full L 4 recount for
  every null; Python confirmation of 2 sampled L 8 survivors per null; K4 survivor lines compared with cycle 155.

## Reproduce
```
W=/tmp/w157 REPO=$PWD bash tools/cycle157/run_cycle157.sh        # ~7 min on 8 cores (resumable)
cd /tmp/w157 && python3 $REPO/tools/cycle157/summarize157.py results_raw.txt
python3 $REPO/tools/cycle157/structure157.py results_raw.txt nulls.txt ct_K4.txt $REPO/data/cycle155/controls.txt
REPO=$REPO bash $REPO/tools/cycle157/indep157.sh
```
