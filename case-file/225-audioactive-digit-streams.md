# Case 225 — Audioactive digit streams: the look-and-say strings as keys (cycle 239)

**Slot:** new family (I-385). Idea **I-379** (tested here); owed items from I-377 (a) and (c) done; new **I-386–I-388**.
Pre-registered as [PREREG239](../tools/cycle239/PREREG239.md) (local commit ee95bd6, 2026-11-25 03:40 MST, before any plant, null or K4 run with `keys239.bin`). Base: origin/main **6cd742e** (c238 published). Code and window list: [`tools/cycle239/`](../tools/cycle239/) (`keys239.py`, `conway_table.py`, `las_exact.py` (= case 223), `plant239.py`, `mknull239.py`, `runA.sh`, `runP.sh`, `runAll.sh`, `mw221.py`, `HASHES239.txt`); tool `gn217` **unchanged** (source sha 97bae55f…d793), checker `check237.py` unchanged; raw results (stamped): [`data/cycle239/`](../data/cycle239/) (`SHA256SUMS`).
**Verdict: no solution.** K4 has 0 hits (0 exact, 0 with one wrong crib letter) in direct, bank and all.bin: `EXACT-EXCL` within the frozen 6,810-window list and model Q (gate P 20/20).

## Why this family
Case 223 tested only the *length* of look-and-say terms (S18). The strings themselves are a different stream: a "say what you see" rule a person can run by hand, digits 1–3 only (shifts B–D or A–C), and Conway's decomposition into 92 "elements" gives a second, full-range stream (atomic numbers). Chosen over I-375 / I-313 / I-336 because its data are exact and already validated in the repo (no transcription risk) and the run is cheap. K1–K3 fit is weak: `[speculation]`, no source says Sanborn used it.

## Source checks (all in `keys239.py`, all pass)
- Conway's element table parsed from the Wikipedia article "Look-and-say sequence" (raw wikitext, 2026-11-25, `data/cycle239/las_wiki.txt`, `[secondary]`): 92 rows, Z = 1…92.
- The 92 atoms **derived in code** in case 223 equal the 92 table strings as a set, and every derived decay list equals the table's "decays into" column (92 / 92).
- Element sequences (term 8 split, then ordered decay) concatenate back to the exact term strings for terms 8–21; term 8 = Hf.Sn, as Conway states.

## Window list (frozen, sha 4bcec305…00ae, 6,810 windows, all fwd, mod 26)
| family | stream | windows |
|---|---|---|
| LSCAT | digits of T1 T2 T3 … concatenated, k = d + c, o 0–499, c ∈ {0, 1} | 1,000 |
| LSTERM16–21 | term n (102–408 digits) cyclic from every offset, k = d + c | 2,602 |
| PAIRCAT / PAIRT21 | the same digits in two-digit groups (10a + b) mod 26 | 400 / 408 |
| ELEMZ | element stream (terms 8, 9, … concatenated), k = Z + c | 1,000 |
| ELEMD1 | same stream, first digit of each element + c | 1,000 |
| S18PAIR | decimal digits of S18(1) S18(2) … in two-digit groups | 400 |

94 candidates dropped as duplicates of earlier lists or of earlier windows here. Degeneracy audit (`audit238.py`, pasted in the PREREG): DISTINCT3 on every single-digit window and CONST60 on 732 ELEMD1 windows are **DESIGN** (strings of 1–3; most elements start with `1`); no TAILRUN / ZEROTAIL in the long streams, no SEATCONST, no BUG flag; 0 duplicates across lists.

## Results
`gn217` model Q, forms Vig / variant / Beaufort, hit = ≥ 23 / 24 crib seats (EASTNORTHEAST 0-based 21–33, BERLINCLOCK 63–73); direct 86,731² `alpha.bin`, bank (165,065 rows) and all.bin (165,782 rows) 144² `themed144.bin`.

| scope | permutation rows | window-pair-forms | K4 hits (24 / 23) | 6 fresh nulls 209711–209716 | K4 time |
|---|---|---|---|---|---|
| direct | 1 | 1.54 × 10¹⁴ | 0 / 0 | 0 / 0 each (full) | 5 s |
| bank | 165,065 | 2.80 × 10¹⁴ | 0 / 0 | 0 / 0 each (rows ÷ 10, declared) | 101 s |
| all.bin | 165,782 | 2.81 × 10¹⁴ | 0 / 0 | 0 / 0 each (rows ÷ 10, declared) | 101 s |

(Window-pair-forms for the families = rows × 144² × 3 forms × 6,810 windows × 2 directions × 2 key indexings, as in case 223; `gn217`'s own T-line counter prints 4.1 × 10¹⁰ there, a counter of its join, not this product.)
**Gate P (seed 209710):** 20 / 20 plants recovered with the planted (window, form, X, Y, permutation) (Wilson 0.84–1.00; 10 one-error plants included; plant windows: ELEMD1 5, LSTERM 9, ELEMZ 2, LSCAT 2, PAIRCAT 1, S18PAIR 1). **Gate T:** `check237.py` re-derived all 23 plant H lines, agreement mismatches 0. Planted decrypts NC −4.95 … −3.86, every one above the I-342 bar (−7.01 at nq 64, N = 10; margin ≥ +2.05).
**Neighbour windows (new observation, I-386):** 3 of 20 plant ciphertexts produced a second H line from a *different* window of the same low-entropy stream (keys equal on most seats): those decrypts are partly the plant's English (NC −5.24, −6.05 and −4.50), and the −6.05 line clears the bar. On a real hit this would be a true lead read through the wrong window; it is why the honesty clause asks for the 97 letters and a reproduction, not just a bar pass. K4 has no H line, so nothing to trace here.
**Nulls:** six shuffled K4 texts, 0 hits in every scope (machinery check, not power).
**Compute:** 365 s wall for K4 + nulls, gate P 5 s, one process group (`setsid timeout 600`), no other process touched.

## Reading (I-379)
- `EXACT-EXCL` for K4 within the 6,810 audioactive windows and model Q (one wrong crib letter tolerated). No H line, so the I-342 bar was not exercised on K4 (fourth cycle in a row).
- Honest scope: forward reading only; seeds `1` only; offsets as listed; digit keys k = d or d + 1 (no multipliers, no other moduli); element stream from term 8 on.
- Not covered: reversed strings, other seeds (Conway's seed `3`, `22` fixed point), element **symbols** as a letter running key (HFSNLUIN…, I-387), multipliers a ≠ 1, the 3-valued digits as a ternary / Polybius index.

## Owed items (I-377)
- **(a) Case 221 exact Mann–Whitney.** `tools/cycle239/mw221.py` reads only published files (data/cycle235/R, nulls235.tsv, data/cycle232/summary232.json): n 24 vs 20, no ties, U 33.0; **exact two-sided p 6.01 × 10⁻⁸** (Voynich's 6.0e-8 confirmed); normal approximation with continuity 1.13 × 10⁻⁶ (the published figure), without 1.07 × 10⁻⁶. Output in `data/cycle239/mw221.txt`; addendum in case 221.
- **(c) Quadgram tables published:** [`data/support/`](../data/support/) `quadgrams.json` (sha 70c628cf…ee1c) and `qg.bin` (26⁴ float32, sha 4a02ba4e…9f69), the same shas as HASHES232 / HASHES235; max |json − bin| 2.8 × 10⁻⁷. Voynich can now run `check235.py` independently.
- (b) the bar reading check stays for cycle 241.

## News check (2026-11-25)
No solution. K4 plaintext private (Paradigm's $1 hash verifier, June 2026); method unpublished. Seen, nothing new for the repo: a waggle.social "Cracking K4" brief (Nov 2026), rayborg/kryptos-k4-dashboard research notes (cutoff 2026-07-27), cipher.ink overview (23 Oct 2026), akaalias/k4 (198 experiments, criteria revised 17 Nov), Andrew Chan's ChatGPT record, kryptosbot.com FAQ. `[secondary / community, unverified]`.

## Blind spots
See "Not covered" above; plus the neighbour-window effect (I-386) for low-entropy lists generally; I-376 near-miss profile not run on this list (I-380).
