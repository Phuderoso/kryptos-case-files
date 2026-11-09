# Case file 157 — One wrong letter: running keys behind K3's decimation law and routes (cycle 169)

**Status:** negative. **Type:** variant/audit of cycle 168 (case 156 was a new structure). Two IDEAS items:
- **I-087:** case 156's exact test (named running keys behind 165,782 K3-law decimations and spiral/diagonal routes) was strict, so
  one wrong crib letter or one wrong carved letter at a crib position would have hidden a true key. Rerun with one error allowed
  (≥ 23 of 24 crib letters): **K4 0 fits at ≥ 23/24 (0 at 24/24) → `EXACT-EXCL` under one error.**
- **I-090:** case 156 found that `bookrk`'s depth diagnostic counts up to 63 phantom offsets past the end of each text. The new tool
  masks them. **Every quoted depth checked stands:** case 156 (K4 best 9, 4 configs; null max 12), case 44 (K4 best 9, 6 configs;
  nulls 9/9/10). Over the whole cycle-168 run, about 15,559 of 287,096,544 configs (0.005 %) drop one level (read from the histogram flows), none from above depth 6.

## 1. Why this, and why now
Cycle 168 was a new family, so 169 is an audit/variant slot. The queue offered I-087 + I-090 (cycle 168's own suggestion) or I-072
under I-085 (more nulls for the cycle-163 one-error split-key count). I-072 can only re-rank 12 configurations that are already
decoded and gibberish (case 151), at ~3.5 min per null. I-087 closes the main robustness gap in the newest exact exclusion (I-003's
programme: one-error audits of high-impact exact results). It also turned out cheap: one extra bitset makes the test one-error
tolerant, at ~3.4× the strict cost, not the ~10× the queue estimated. I-090 needs the same masking, so it comes free.

## 2. Model (same as case 156, plus one error)
- Transpositions: the same 165,782 (`dec_perm.bin` 159,712 K3-law decimations M 97–112 + `route_perm.bin` 6,070 routes; perm and inverse).
- Models A (substitute in plaintext order, then transpose) and B (transpose, then substitute in carved order); 29 substitutions
  (24 additive A–Z/KRYPTOS tableaux incl. Sanborn's K1/K2 rule and Quagmire I–III on KRYPTOS, 5 five-bit XOR codes).
- Key texts: cycle 168's `texts.txt`, sha256 `af222890…` (identical file). **36 texts**: 24 carved texts made cyclic, plus Carter vol. I, Smith 1923,
  KJV John, KJV NT, NSA 1947, Reagan 1987, each forward and reversed. 3,305,522 letters, 3,302,066 offsets. (Erratum, §8:
  case 156 says "48 texts". The letter and offset counts there were right.)
- **Error model:** exactly one of the 24 crib constraints may fail. That covers one wrong crib letter (the true plaintext differs from
  EASTNORTHEAST/BERLINCLOCK at one position) and one wrong carved letter at a crib position. A wrong carved letter elsewhere does not
  touch the test. For XOR codes, an undecodable key symbol now counts as the one allowed miss. The strict tool skipped those configs,
  so this run has 290,153,232 configs against case 156's 287,096,544.
- Not covered: a dropped or inserted carved letter (it shifts the alignment), and two or more errors.

## 3. Tool (`tools/cycle169/bookrk1e.c`)
Two bitsets over real offsets: `A` (no miss so far) and `O` (at most one miss so far). Per constraint with shifted letter bitset `v`:
`O ← (O & v) | A`, `A ← A & v`. Every word is masked to offsets `o < len − 96` (I-090). When `O` gets sparse, the surviving offsets
are finished letter by letter. Output: `FULL` (24/24), `FIT23` (with the missed crib index), masked strict depth, one-error
depth (`depth1`), and both histograms. Before the run it reproduced case 156's strict histogram on the strict config set,
up to the expected tail-bit shifts (§6).

## 4. Results (run 02:24:29–02:31:30 PDT, 7 min wall, 8 processes, own process group, CPU shared; [`summary169.txt`](../data/cycle169/summary169.txt))
| item | scope | ≥ 23/24 fits | best one-error depth | label |
|---|---|---|---|---|
| K4 | 165,782 perms × 2 models × 29 subs × 36 texts (290,153,232 configs, ≈ 3.2 × 10¹³ placements) | **0** (FULL 0, FIT23 0) | 12 (1 config: perm 7017 of chunk 04, B, mode 22, KJV NT; strict depth 5) | `EXACT-EXCL` |
| K4 on null slice | 1,000 perms (first 500 decimations + last 500 routes) | 0 | 9 | — |
| 40 shuffled K4s | same slice | **0 in 40** (exact binomial 95 % upper bound on the null fit rate 7.2 %) | 9 / 9 / 10 (min/median/max); 40/40 ≥ K4's 9 | null lineup |
| 18 planted controls | 2,000-perm slices (cycle 168's string-level controls, then corrupted) | **18/18 PASS** | — | see §5 |

**Bound.** Under uniform letters P(≥ 23 of 24) = 24·(1/26)²³·(25/26) + (1/26)²⁴ ≈ 6.6 × 10⁻³². Times 3.2 × 10¹³ placements, that is
≈ 2 × 10⁻¹⁸ expected chance fits. Worst case, every required key letter is as common as English E (p = 0.127): ≈ 1.6 × 10⁻⁶. A one-error fit
would therefore still be decisive, and 0 is what a wrong model gives. The verdict rests on this bound and on the controls. The test is exact,
so plant strength is binary. The null count is reported in the I-085 spirit: 0/40 nulls fit, ≥ 40 as I-085 asks.

## 5. Controls (independent, string level; [`controls169_planted.txt`](../data/cycle169/controls169_planted.txt), [`ctl_verify169.txt`](../data/cycle169/ctl_verify169.txt))
Built by `ctl169.py` from cycle 168's 12 planted controls (Jane Eyre plaintext, cribs at the official positions, 12 key texts, Models A/B, random decimation/route).
- **e0–e11, one error at a crib position:** even i, a wrong carved letter; odd i, a wrong crib letter (plaintext changed, then re-encrypted
  with the planted key). **12/12** found as FIT23 at the planted permutation, model, mode, text and offset, **with the right missed crib
  index**. Strict `bookrk` finds **0/12** (best depth 7–21), so the strict test of case 156 really was blind to them.
- **n0–n1, wrong carved letter at a non-crib position:** 2/2 FULL (the error does not touch the test, as expected).
- **d0–d3, two crib-position errors:** 4/4 absent. Tolerance is exactly one.
- `verify169.py verify` rebuilds every FULL/FIT23 line's 97-letter decryption by string operations. Each is 23/24 (or 24/24) with the stated
  miss, and **each differs from the planted plaintext in exactly the one corrupted letter**. Extra lines are the same key in a containing
  text (KJV John ⊂ NT; K3 ⊂ K1–K3 and K1–K3+K0).
- Independent numpy recount (`verify169.py depth`, no bitsets) on 40 random permutations × 36 texts × 2 models × 24 additive modes
  (69,120 configs): **identical masked strict and one-error histograms** to `bookrk1e`
  ([`recount40_numpy.txt`](../data/cycle169/recount40_numpy.txt), [`recount40_bookrk1e.txt`](../data/cycle169/recount40_bookrk1e.txt)).

## 6. I-090 — masked depths and the cited case files ([`recheck090.txt`](../data/cycle169/recheck090.txt))
Case files that quote `bookrk` depths: 34, 35, 44, 45 (Myszkowski, different tool), 68, 72, 77, 156. `recheck090.py` cuts each
quoted best config (one permutation, one text) out of the original run folders and runs the old tool and the masked tool side by side:
| case | config | unmasked | masked | one-error depth |
|---|---|---|---|---|
| 44 (cycle 45) K4 | 6 configs, KJV John rev, modes 22 / 12 | 9 | **9** | 10 |
| 44 null 1 / null 3 max | Carter rev | 9 / 10 | **9 / 10** | 10 / 11 |
| 156 (cycle 168) K4 | 4 configs, KJV NT rev ×3, NSA 1947 rev | 9 | **9** | 10 |
| 156 null 6 max | KJV NT rev | 12 | **12** | 13 |

Whole-run effect (cycle 168 K4, all 287,096,544 strict configs). Unmasked: 0:18,436,652 1:133,883,107 2:89,715,227 3:34,424,182 4:9,565,945
5:1,015,489 6:53,434 7:2,422 8:82 9:4. Masked: 0:18,436,652 1:133,888,412 2:89,718,871 3:34,416,438 4:9,564,827 5:1,015,415 6:53,421
7:2,422 8:82 9:4. Read as one-level flows (6→5: 13, 5→4: 87, 4→3: 1,205, 3→2: 8,949, 2→1: 5,305), that is ≈ 15,559 configs (0.005 %), none from above depth 6. Case 44's "K4 9 vs nulls 8–10" and case 156's "K4 at
the bottom of the null depth range" stand. Cases 34, 35, 68, 72 and 77 quote maxima of 7–11 from the same tool. Their run folders
were not re-cut this cycle. The shift is downward-only and in this sample never reached the maximum, so their verdicts (all resting on
24/24 fits, not on depth) cannot change. They are noted as "not re-cut".

## 7. Crib and English checks
K4: no configuration reaches 23/24, so there is no candidate to decrypt. The single deepest one-error prefix (12 of 24, strict 5) is
a partial coincidence in a 2.9 × 10⁸-config search and not a fit. No coherent 97-letter English, and no candidate.

## 8. Errata to case 156 (documentary, results unaffected)
- "48 texts" should read **36 texts** (24 carved + 6 books × fwd/rev). The 3,302,066 offsets and 287,096,544 configs were computed on
  the 36. The same slip appears in the README decimation row and the cycle-168 journal. The README is corrected this cycle.
- "chunk_15 = 10,352 decimations + all 6,070 routes" should read **chunk_15 = the last 10,352 perms = 4,282 decimations + all 6,070 routes**.
  So the 24 nulls of case 156 ran on 10,352 perms, not 16,422.

## 9. Run folder (I-078)
[`inputs_provenance.txt`](../data/cycle169/inputs_provenance.txt): 93/93 outputs end in SUMMARY, 0 `.tmp`, sha256 of all inputs.
Raw outputs: [`outputs_k4.txt`](../data/cycle169/outputs_k4.txt), [`outputs_nulls_controls.txt`](../data/cycle169/outputs_nulls_controls.txt).

## 10. What this excludes and what it doesn't
Excluded (exact, ≤ 1 error): K4 = running key from any of the 36 named texts at any offset, under any of the 29 substitutions, in
either layer order, behind any K3-law decimation (M 97–112) or spiral/diagonal route of cycle 61, with up to one wrong crib letter or
one wrong carved letter at a crib position.
Not excluded: a dropped/inserted carved letter (I-093); two errors; one error behind the 165k bank or the 1.87M rail/AMSCO family
(I-091); transpose-first with an unnamed book (I-088); the 98-symbol `?` circle and the 20,946 mixed tableaux (I-089); unlisted books.

## 11. Reproduce
`tools/cycle169/run_cycle169.sh` (needs cycle 168's run folder: `all.bin`, `chunk_00..15`, `texts.txt`, `ctl/`), then
`python3 tools/cycle169/summarize169.py RUN`; `recheck090.py BOOKRK BOOKRK1E data/cycle169/recheck090_list.txt`;
`verify169.py depth K4 all.bin texts.txt 40 1690`.
