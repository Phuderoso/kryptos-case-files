# PREREG238 — Cycle 238 (audit slot): I-382 silent-truncation audit of all frozen key lists + closing the case 223 stride-10 null deviation

Filed 2026-11-24 19:46 MST (UTC-7), **before** any run of `audit238.py` on the published lists, and before any `gn217` run with the nulls below. Base: origin/main **20f9948** (c237 already published there, tree 8fb12327). Case file 224.
Slots (I-381): 238 audit, **239 must be a new family**, 240 free. Seeds: tool plants **209706**, Part B nulls **209707, 209708**, Part A null windows **209709**; next free after this cycle **209710**.

## Why these two items
1. **I-382.** Cases 219 / 220 carried a silent bug (S18 look-and-say stopped at 10⁵ chars and returned 0; 94 of 136 positions zero) that was found by chance, in cycle 234, 15 cycles after the family was frozen. `EXACT-EXCL` labels are only as good as the window lists behind them. A generic, frozen detector run on *every* published list (keys217 … keys237, 85,818 windows incl. ×a copies) is the highest-value audit available: it checks the premise of ~20 exclusion labels at once.
2. **Case 223 deviation.** Case 223's six nulls were run at row stride 10 in bank / all.bin (full scale ≈ 17 min). The null role there is a machinery check, but a disclosed deviation should be closed when budget allows: two fresh nulls at **full** scale (all rows) on `keys237.bin`.

## Part A — list audit (`audit238.py`, thresholds frozen in its docstring, sha in HASHES238.txt)
Lists (all `gn217` `.bin`, 97 bytes per window): `keys217`, `keys218`, `keys221a` (case 221 chunk A) + `keys222b` (chunk B; their concatenation = `keys221.bin`), `keys233`, `keys234`, `keys236`, `keys237`. Flags: CONST60, DISTINCT3, TAILRUN (last ≥ 10 identical), ZEROTAIL, HEADRUN, RUN20, SEATCONST (24 crib seats equal), BLOCKCONST, PERIOD12; plus within-list and cross-list duplicate windows.
- **Gate P (tool plants, seed 209706, `plant238.py`):** 20 clean random windows + 40 defective windows (8 kinds × 5: zero tail, clamp / size-cap, constant, 3-valued, head run, seat-constant, block-constant, periodic). Pass: each defective window carries its **expected** flag (40/40) and 0 / 20 clean windows are flagged. (The plant list was generated and the tool smoke-tested on it, 40 flagged windows, **before** this filing; no real list had been audited.)
- **Gate N (calibration of false flags):** 100,000 uniformly random 97-value windows over Z₂₆ (seed 209709): expected flags per window ≈ 0 (a random window cannot reach CONST60 / RUN20 / TAILRUN ≥ 10 at 26 symbols: TAILRUN P ≈ 26^-9). Pass: ≤ 1 flagged window. This is the null: any flag on a real list that random windows do not produce is structural.
- **Known positive:** `keys233` S18 rows (the case 219 truncation) **must** be flagged ZEROTAIL (those with o ≥ 5, 55 + o zeros) — if not, the detector fails to find the bug it was designed for → `INSUFFICIENT-DISCRIMINATION`.
- **Reading rule (declared):** a flagged window in a list is *not* an error by itself (Catalan C_n ≡ 0 mod 26, constant sequences by design). Each flagged **family tag** is reported with count, cause (by reading the generator) and class: **BUG** (the sequence stops or saturates by implementation), **ARITHMETIC** (true property of the sequence), **DESIGN** (e.g. intended constant key). Only BUG families change a label: they get a note "within the list the effective family is X" and a repair idea; no old label is silently edited. Unflagged ≠ correct (the detector sees degeneracy, not wrong-but-varied values).
- **A2:** `srcscan238.sh` textual scan of all key generators for caps / `break` / `return 0` / large literals, results read by hand and listed.

## Part B — full-scale nulls (closing the case 223 deviation)
`mknull238.py`: two shuffled K4 texts (209707, 209708). `runB.sh`: `gn217` (source sha 97bae55f…d792, **unchanged**) on `keys237.bin`, direct / bank (165,065 rows) / all.bin (165,782 rows), stride **1**, hit = ≥ 23 / 24 crib seats. Expectation: 0 hits per scope (24-seat filter ≪ 1 chance hit); the result is a machinery check, not a power calibration. Time budget ≈ 6 min wall in its own process group (`setsid timeout 660`). If it overruns, stop **my own** process group only and report the partial result as such.

## Labels
- Part A: per list, `CLEAN` (no flag beyond the DESIGN / ARITHMETIC classes) or `FLAGGED` with family tags and class; gates P, N, known-positive must pass, else `INSUFFICIENT-DISCRIMINATION` for the audit. A clean list leaves its earlier `EXACT-EXCL` label unchanged (that label's scope is the list, model Q and the stated assumptions); it does not enlarge it.
- Part B: 0 / 0 hits at full scale → the case 223 deviation is closed (`machinery check`, no tail claim from 2 nulls); any hit on a null → report and investigate before anything else.
- No tail claims from small nulls; no K4 re-run is needed in this cycle (K4 results on these lists are published, tool unchanged).

## Honesty clause
Nothing here can produce a solution except a regression in the tool; if a K4-like decrypt appeared anywhere it would be reported prominently and reproduced independently. Nothing is submitted anywhere.
