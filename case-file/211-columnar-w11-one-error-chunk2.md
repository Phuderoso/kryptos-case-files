# Case file 211: every width-11 column order with π[0] ∈ {2, 3}, four alphabet pairs, under one wrong crib letter (I-312 chunk 2)

**Cycle 225, 2026-11-20 (free slot). Verdict: negative within the chunk. Pre-registered as `tools/cycle225/PREREG225.md`
(local commit filed 11:43 PT, before any run on K4, plants or nulls).**

## Why
Case 114 Part B (cycle 126) excluded every width-11 column order with a periodic key p ≤ 18 on four alphabet pairs, but only
strictly (all 24 crib letters). Case 206 (chunk 1, π[0] ∈ {0, 1}) showed the exclusion survives one wrong crib letter there. This is
**chunk 2: π[0] ∈ {2, 3}** = 7,257,600 orders, the K3-style keyed-columnar layer under a KRYPTOS / Quagmire periodic layer. After
this, 4/11 of the w 11 orders are done.

## Method (exact within its scope)
- Tool `tools/cycle220/col1e4.c` **verbatim** (sha256 de865865…e573f); `tools/cycle225/run225.sh`; `analyze225.py` =
  `analyze220.py` with the chunk changed, gate S replaced by gate T, and D2 rank / null-occupancy columns.
- Family exactly as case 206: ragged grid of width 11, COL / ROW read, σ and σ⁻¹, Vigenère (= variant) or Beaufort, key before (A)
  or after (B) the transposition, p 1–18, A–Z, KRYPTOS (Quagmire III), Quagmire I, Quagmire II. One error = excess ≤ 1.

## Gates
- **T (tool identity):** K4, w 11, π[0] = 0, π[1] = 1 rerun now is byte-identical to cycle 220's `.raw` (sha256 12a6ae3d…33922). **PASS.**
- **R (weak):** K4 strict count 0 at every p ≤ 18 in the chunk (case 114 Part B). **PASS.**
- **P (plants, seed 209537, `plant225.py`):** 20 plants, five per alphabet pair, odd ids with one corrupted carved crib letter, π[0]
  forced into {2, 3}, each on its true sub-slice. **20/20** found at the true configuration and period, decrypt matching outside the
  corrupted key class. **PASS.**

## Result (K4 vs eight shuffled K4, seeds 209538–209545, same chunk; all 9 texts complete, 7,257,600 orders each)
| p | K4 (strict + one-error) | nulls | null occupancy | label (chunk scope) |
|---|---|---|---|---|
| 1–17 | 0 | all 0 | 0/8 | `EXACT-EXCL (one-error scope, discriminating)` |
| 18 | 6 (D2 6) | 6, 10, 6, 2, 0, 4, 8, 6 | 7/8 | `INSUFFICIENT-DISCRIMINATION` (D2 rank p_up 6/9 ≈ 0.67) |

K4 has **no** configuration with excess ≤ 1 at p ≤ 17 in this chunk, and here every null is also 0 through p 17 (chunk 1 had
nulls at p 15–17), so the exclusion is discriminating up to p 17. At p 18 K4's six one-error cells sit at the null median.
Every K4 p 18 cell (91 key-determined letters) scores below the −6.0 bar (best −6.78:
`KU?HYACMONAQVYRISOFU?EASTNORTHEASTAMFU?…BERLANCLOCK…`, a Quagmire I, Vigenère, model A fit whose dissenting seat is the I of BERLIN);
gibberish, no candidate.

## Scope and blind spots
Only π[0] ∈ {2, 3}; chunks {4,5}, {6,7}, {8,9}, {10} remain. One error only (no dropped / inserted letters, no two errors); p ≤ 18;
rotation 0 and short last row = leftmost columns; tableau alphabets only (no Quagmire IV). Eight nulls give a scale, not a tail.
Quagmire I / II one-error at w 9–10 (the other half of I-312) is still not done.

## Files
[`data/cycle225/`](../data/cycle225/): `results_k4.txt`, `results_null2095xx.txt` (stamped: scope, input sha256, tool sha256, per-p
counts, hit lines), `summary225.json`, `analyze225.log`, `plants/` (raw plant outputs), `gateT/`, `plants225.tsv`, `nulls225.tsv`,
`texts.tsv`, `time.txt`, `SHA256SUMS`. Tools: [`tools/cycle225/`](../tools/cycle225/). Heavy wall 11:43:39–11:51:42 PT (~483 s).

## Also this cycle
Case 210 addendum: the Voynich desk's recount of the V all.bin p 19 cell (voynich-case-files b0793db / 0128be8): 2 distinct tests,
not 1 (Z is involved), `NO-SIGNAL` unchanged.

## Verdict
No solution. Within π[0] ∈ {2, 3}, a width-11 keyword columnar with a periodic key on any of the four tableau pairs is excluded up to
p 17 even with one wrong crib letter (p 18 not discriminating). **K4 still standing.**
