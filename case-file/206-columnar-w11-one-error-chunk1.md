# Case file 206: every width-11 column order with π[0] ∈ {0, 1}, four alphabet pairs, under one wrong crib letter (I-312 chunk 1)

**Cycle 220, 2026-11-19 (free slot). Verdict: negative within the chunk. Pre-registered as `tools/cycle220/PREREG220.md`
(local commit filed 15:44 PT, before any run on K4, plants or nulls).**

## Why
Case 114 Part B (cycle 126) excluded every width-11 column order with a periodic key p ≤ 18 on four alphabet pairs (A–Z,
KRYPTOS = Quagmire III, Quagmire I, Quagmire II) — but only **strictly** (all 24 crib letters). Case 205 showed that the w 9–10
version survives one wrong crib letter up to p 17. I-312 asks the same of w 11. 11! orders × 4 pairs is ~20× case 205, so the work
is split by the read rank of column 0 (π[0]) into resumable chunks. This is **chunk 1: π[0] ∈ {0, 1}** = 7,257,600 orders (2/11).

## Method (exact within its scope)
- Tool `tools/cycle220/col1e4.c`: cycle 219's `col1e.c` with a minimal diff. NAL = 4 adds Quagmire I (keyed PT alphabet,
  straight CT) and Quagmire II (straight PT, keyed CT) to A–Z / A–Z and KRYPTOS / KRYPTOS; an optional SECOND argument fixes π[1]
  so each slice runs as ten resumable sub-slices of 9! orders.
- Family: ragged 97-letter grid of width 11, COL or ROW read, σ and σ⁻¹, Vigenère (= variant for consistency) or Beaufort, key
  indexed before (model A) or after (model B) the transposition, period 1–18. One error = excess ≤ 1: exactly one crib seat dissents
  (a wrong crib letter, or a wrong carved letter at a crib seat).

## Gates
- **T (tool identity):** `col1e4` with NAL = 2 on K4, w 10, π[0] = 3 is byte-identical to cycle 219's output for that slice
  (`data/cycle220/gateS/full_w10_f3_nal2.raw`). Run as a smoke test while writing the tool, before PREREG220 was filed; disclosed there.
- **S (sub-slicing):** the nine π[1] sub-slices of that slice add up to 362,880 orders and to the same strict / one-error counts at
  every p 1–22. **PASS.**
- **R (consistency, weak):** K4 strict count 0 at every p ≤ 18 in the chunk, as case 114 Part B says. **PASS.**
- **P (plants, seed 209242, `plant220.py`, independent textbook encryptor):** 20 width-11 plants, five per alphabet pair, odd ids with
  one corrupted carved crib letter, each on its true (π[0], π[1]) sub-slice. **20/20** recovered at the true configuration and period
  with the crib-key decrypt matching the plant outside the corrupted key class.

## Result (K4 vs eight shuffled K4, seeds 209243–209250, same chunk)
| p | K4 (strict + one-error) | nulls | label (chunk scope) |
|---|---|---|---|
| 1–14 | 0 | all 0 | `EXACT-EXCL (one-error scope, discriminating)` |
| 15 | 0 | 0,0,0,0,0,0,1,0 | `EXACT-EXCL (one-error scope, discriminating)` |
| 16 | 0 | 0,0,0,0,1,0,0,0 | `EXACT-EXCL (one-error scope, discriminating)` |
| 17 | 0 | 0,0,24,2,2,0,0,0 | `EXACT-EXCL (one-error scope, exact but saturated-null)` |
| 18 | 0 | 0,15,0,0,12,4,69,2 | `EXACT-EXCL (one-error scope, exact but saturated-null)` |

K4 has **zero** configurations with excess ≤ 1 at any p ≤ 18 in this chunk. At p 17–18 the exclusion is still exact, but 3/8 and
5/8 shuffles also fit somewhere, so a zero there says less than a zero at p ≤ 16.

## Scope and blind spots
Only π[0] ∈ {0, 1}: no claim about the other 9/11 of the width-11 orders (chunks 2–5 in later free slots). One error only (no
dropped / inserted letters, no two errors); p ≤ 18; rotation 0 and short last row = leftmost columns; tableau alphabets only (no
Quagmire IV). Eight nulls give a scale, not a tail. Quagmire I / II one-error at w 9–10 (the other half of I-312) is not done yet.

## Files
[`data/cycle220/`](../data/cycle220/): `results_k4.txt`, `results_null2092xx.txt` (stamped: scope, input sha256, tool sha256,
per-p counts, hit lines), `summary220.json`, `analyze220.log`, `plants/` (raw plant outputs), `gateS/`, `plants220.tsv`,
`nulls220.tsv`, `texts.tsv`, `time.txt`, `SHA256SUMS`. Tools: [`tools/cycle220/`](../tools/cycle220/) (`run220.sh` reproduces
the run in ~7.6 min on 8 cores). Heavy wall 15:44:50–15:52:25 PT.

## Verdict
No solution. Within π[0] ∈ {0, 1}, a width-11 keyword columnar with a periodic key on any of the four tableau pairs is excluded up to
p 18 even with one wrong crib letter. **K4 still standing.**

## Addendum (cycle 222, 2026-11-19): the Voynich desk's open recount of the p 18 null cells
The Voynich desk published an open recount at voynich-case-files `386e342` (`audits/kryptos/c206-p18-recount/`, 2026-11-19 19:59 PT,
after cycle 221 was filed; no seed used). `data/cycle220/SHA256SUMS`: 45/45 OK. Counting only from the stamped `results_null*.txt`
(H lines with p = 18, cross-checked against each file's per-p header), her counts match ours 8/8: **0, 15, 0, 0, 12, 4, 69, 2**. Not
blind on values (we sent them first); she froze and hashed her counts before comparing. Her breakdown of null 209249's 69 cells: file
lines 7–76 except line 65 (the lone p 15 hit), all one-error, in about eight near-duplicate column-order families. Descriptive only;
it supports reading p 17–18 as saturated-null and counting families rather than cells (cf. I-318). **No label changes.**
