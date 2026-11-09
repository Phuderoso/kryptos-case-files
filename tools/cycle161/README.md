# Cycle 161 — finishing the rank-matched Gromark L 8 lineup (IDEAS I-062)

No new solver. The cycle-155 program `tools/cycle155/gromark1e.c` (model P, byte-identical source, binary sha256
`c63bb070…99b1b6` identical to the cycle-159 build) and the cycle-159 resumable runner finish the 70 chunks cycle 159 left
(primer quarter q2 for 29 nulls, q3 for 41) on the same 48 profile- and r8 = 6-matched nulls.
- `run_cycle161.sh` — resume + summary + controls (reproduction recipe).
- `summarize161.py` — duplicate/gap check over all 192 (null, quarter) chunks; K4 vs nulls on the full range (primary,
  pre-specified), per quarter, and the post-hoc q3 comparison with Bonferroni ×4 / ×16.
- `plant161.py` — three planted model-P L 8 encryptions with primers forced into 50–100 M (reuses `plant159.py`'s generator).
- Independent recount: `tools/cycle159/indep159.py` (pure Python, shares no code with `gromark1e.c`) on 7 windows.
