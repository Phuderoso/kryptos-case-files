# Case file 214: width-11 column orders with π[0] ∈ {4, 5} under one wrong crib letter (I-312 chunk 3), and the old w 9–11 cells re-read with the NC bar (I-331)

**Cycle 228, 2026-11-20/21 (free slot). Verdict: negative within the chunk; no published crib-consistent cell of cases 205 / 206 /
211 clears the house bar. Pre-registered as `tools/cycle228/PREREG228.md` (local commit 3261429, 23:47:24 PT, before any run of
chunk 3 on K4, plants or nulls).**

## Why
Case 114 Part B excluded every width-11 column order with a periodic key p ≤ 18 on four alphabet pairs, but only strictly (all 24
crib letters). Cases 206 and 211 showed the exclusion survives one wrong crib letter for π[0] ∈ {0, 1} and {2, 3}. This is **chunk 3:
π[0] ∈ {4, 5}** = 7,257,600 orders. After it, 6/11 of the w 11 orders are done. It is also the first w 11 chunk read with the I-330
NC bar and the tie = '?' rule. Cases 205 / 206 / 211 were read with the retired all-letter bar, so Part B re-reads their published
cells with the new one (I-331).

## Method (exact within its scope)
- Tool `tools/cycle220/col1e4.c` **verbatim** (sha256 de865865…e573f); `tools/cycle228/run228.sh` (= run225.sh, chunk {4,5});
  `analyze228.py` = `analyze225.py` with decrypts read by `nc228.py` (tie = '?', NC), null NC passes counted per distinct decrypt
  text, Wilson 95 % intervals, D2 and top-3 D2-family share beside raw counts.
- Family exactly as cases 206 / 211: ragged grid of width 11, COL / ROW read, σ and σ⁻¹, Vigenère (= variant) or Beaufort, key before
  (A) or after (B) the transposition, p 1–18, A–Z, KRYPTOS (Quagmire III), Quagmire I, Quagmire II. One error = excess ≤ 1.
- Formats and dedup order as declared in PREREG228 (`.raw` H / C lines, `qg.bin` 26⁴ float32 LE, D2 = first hit per crib-test
  signature in file order).

## Gates
- **T (tool identity):** K4, π[0] = 0, π[1] = 1 rerun now is byte-identical to `data/cycle225/gateT/w11_f0_s1.raw` (sha256
  12a6ae3d…33922). **PASS.**
- **R (weak):** K4 strict count 0 at every p ≤ 18 in the chunk (case 114 Part B). **PASS.**
- **P (plants, seed 209549, `plant228.py`):** 20 plants, five per alphabet pair, odd ids with one corrupted carved crib letter, π[0]
  in {4, 5}, p 1–18, each on its true sub-slice. **20/20** found at the true configuration and period, decrypt matching outside the
  corrupted key class (Wilson 95 % 0.84–1.00). **PASS.** NC under tie = '?': **20/20** barred plants clear −6.0 (Wilson 0.84–1.00;
  range −5.25 … −3.90; known 83–97). Scope of that check: mostly p ≤ 16 (one plant at p 18), so it validates recovery and the bar at
  the periods where plants sat, not a tail.
- **Invariance pre-check** (before filing, on the published case 211 plants): NC moves from −3.9…−4.7 to unscorable / −8.05 when the
  ciphertext is shuffled under the same hit, and tie = '?' moves `known` 91 → 86 on one plant. The statistics move.

## Part A result (K4 vs eight shuffled K4, seeds 209550–209557, same chunk; all 9 texts complete, 7,257,600 orders each)
| p | K4 raw (D2) | nulls raw (= D2) | null occupancy (Wilson 95 %) | NC passes: K4 / nulls (distinct texts) | NC max: K4 / nulls | label (chunk scope) |
|---|---|---|---|---|---|---|
| 1–17 | 0 | all 0 | 0/8 (0.00–0.32) | — | — | `EXACT-EXCL (one-error scope, discriminating)` |
| 18 | 6 (6) | 3, 19, 0, 0, 24, 0, 11, 36 | 5/8 (0.31–0.86) | 0 / 0 | −7.94 / −7.25 | `INSUFFICIENT-DISCRIMINATION` (D2 rank p_up 5/9 ≈ 0.56) |

The shuffled-ciphertext comparison of an exact crib filter is **non-informative by construction**: it scales the count but cannot
weaken the exclusion, which holds for K4 exactly under the stated assumptions. K4 has no configuration with excess ≤ 1 at p ≤ 17 in
this chunk, and every null is also 0 there, so the exclusion is discriminating up to p 17, as in chunk 2. At p 18 K4's six cells
(top-3 D2 family share 0.50) sit inside the null range. All six decrypts are below the bar (best −7.94, known 91:
`VTHYL?PDCPBIBJK?PCBCIEAJTNORTHEASTOU?ZICKPW…BERLINCLOCK?OJVP…`, a Quagmire I, Vigenère, ROW / σ⁻¹, model B fit whose dissenting seat is the S of the first EAST (seat 2, plaintext position 24 counted from 1; it reads J));
gibberish, no candidate. No null text reached the bar either (max −7.25).

## Part B: the I-331 re-read (published hit lines only, no rerun)
**Input delta.** For every text the H lines read equal the stamped one-error + strict counts at every printed p (cases 206 and 211:
all p ≤ 18; case 205: p ≤ 18 one-error, strict at p 21–22). Out of reach from published lines: case 205 one-error cells at p 19–22
(K4 14 + 3 + 1,928 + 15,768; these were never printed, and case 209 already read p 20 / 21 from fresh col21 runs). No cell that was
printed is unreachable by the bar: every one has known ≥ 49 and ≥ 10 NC quadgrams.

| case | K4 cells (D2) | K4 NC max (tie '?' / first vote) | K4 passes | null D2 cells | null NC max | null passes (distinct texts) | reading |
|---|---|---|---|---|---|---|---|
| 205 (w 9–10) | p 18: 2; p 22 strict: 242 | −7.97 / −8.10; −7.30 / −7.30 | 0 | 664 (9 nulls) | −7.14 | 0 | decrypt-level `NO-SIGNAL (NC)` |
| 206 (w 11, π[0] {0,1}) | none | — | 0 | 132 (8 nulls) | −7.49 | 0 | (K4 0: count-level EXACT-EXCL stands) |
| 211 (w 11, π[0] {2,3}) | p 18: 6 | −7.79 / −7.84 | 0 | 42 (8 nulls) | −7.64 | 0 | decrypt-level `NO-SIGNAL (NC)` |

Count-level labels are unchanged. Case 211 printed "best −6.78" under the old all-letter bar; with crib quadgrams removed the same
fit reads −7.79 (the old score was lifted by the crib letters themselves). The case 205 p 22 strict cells all have known 97 but
read as gibberish (best −7.30, `…EASTNORTHEASTMASOYOUTHJMWX…BERLINCLOCKIFUSORVEV…`).

## Scope and blind spots
Only π[0] ∈ {4, 5}; chunks {6,7}, {8,9}, {10} remain. One error only (no dropped / inserted letters, no two errors); p ≤ 18;
rotation 0 and short last row = leftmost columns; tableau alphabets only (no Quagmire IV). Eight nulls give a scale, not a tail.
Quagmire I / II one-error at w 9–10 is still not done. Part B reads only printed lines; the NC bar is the I-330 bar with its
known caveats (chosen post hoc in case 212; quadgram floor under audit, I-333 / I-335).

## Files
[`data/cycle228/`](../data/cycle228/): `results_k4.txt`, `results_null2095xx.txt` (stamped: scope, input sha256, tool sha256,
per-p counts, hit lines), `summary228.json`, `analyze228.log`, `reread228.json`, `reread228.log`, `plants/`, `gateT/`,
`plants228.tsv`, `nulls228.tsv`, `texts.tsv`, `time.txt`, `SHA256SUMS`. Tools: [`tools/cycle228/`](../tools/cycle228/). Heavy wall
23:47:28–23:55:12 PT (~464 s). Note: the PREREG header says "Filed 23:50 PT"; the commit time is 23:47:24 PT, four seconds before
the run started. The header time was an estimate typed before committing; the commit is the record.

## Verdict
No solution. Within π[0] ∈ {4, 5}, a width-11 keyword columnar with a periodic key on any of the four tableau pairs is excluded up to
p 17 even with one wrong crib letter (p 18 not discriminating). None of the 250 published K4 cells of cases 205 / 206 / 211 or the 838
null cells clears NC ≥ −6.0. **K4 still standing.**
