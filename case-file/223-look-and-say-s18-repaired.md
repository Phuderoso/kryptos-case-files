# Case 223 — Look-and-say S18 repaired (exact, no truncation) + near-miss profile (cycle 237)

**Slot:** free (236 new family, 238 audit, 239 new family; I-378). Ideas **I-367** (tested here) and **I-376** (first pass); new **I-379–I-382**.
Pre-registered as [PREREG237](../tools/cycle237/PREREG237.md) (local commit 7fd2b86, 2026-11-23 ~03:47 PT, before any plant, null or K4 run with `keys237.bin`). Base: origin/main **9ed3d33** (c236 was already published there). Code and window list: [`tools/cycle237/`](../tools/cycle237/)
(`las_exact.py`, `keys237.py`, `keys237.tsv`, `plant237.py`, `check237.py`, `mknull237.py`, `mknull237nm.py`, `gn237nm.c`, `runA.sh`, `runN.sh`, `runP.sh`, `runNM.sh`, `HASHES237.txt`); tool `gn217` **unchanged** (source sha 97bae55f…d792); raw results (stamped, rule 5): [`data/cycle237/`](../data/cycle237/).
**Verdict: no solution.** K4 has 0 hits (0 exact, 0 with one wrong crib letter) in all three scopes: `EXACT-EXCL` within the frozen 960-window exact-S18 list (gate P 20/20). The near-miss profile (I-376) is `NO-SIGNAL`: K4's best agreement is 13 of 24, below or equal to the nulls'.

## What S18 was, and the bug (I-367)
`keys233.py` S18 is the **length of look-and-say term n** (term 1 = `1`, lengths 1, 2, 2, 4, 6, 6, 8, 10, 14, 20, …; OEIS A005341), used as key values mod 26 in windows k_i = S18(1+o+i)+c (fwd) or S18(1+o+96−i)+c (rev), o = 0..39, c ∈ {0, 1}.
Its generator stopped building strings at 10⁵ characters (term 42) and `S18(n)` returned **0** beyond. A window reaches n = 136, so **94 of 136 positions were 0** and the BERLINCLOCK seats (0-based 63–73 → n ≥ 64) always sat in the zero tail.
Cases 219 (a = 1) and 220 (a ≠ 1) S18 rows therefore tested "look-and-say, then zeros". Found in cycle 234; repaired here. (Audit of the rest of the cycle-233 sequences: only S12 Catalan is also near-constant, and that one is arithmetic, not a bug: C_n ≡ 0 mod 26 for 79 of the 136 values n = 1..136 by Kummer's theorem; the other 20 sequences and the word-length streams have no window with ≥ 60 equal values.)

## The fix: exact lengths without strings
`las_exact.py` computes S18(n) for any n with Conway's audioactive structure: the look-and-say string decomposes into **92 independent "atoms"** that each decay into a fixed list of atoms, so term lengths follow from a 92-state count vector (Python bigints; S18(136) ≈ 10¹⁶).
The atoms are **derived in code**, not copied from a table: split a term-16 string at every cut whose 9-step evolutions never interact, close the set under decay (result: exactly 92 atoms, as Conway's theorem says), start the count vector at term 16.
**Independent vectors:** (a) direct string iteration agrees for n ≤ 45; (b) the OEIS A005341 b-file (n = 1..3000, [`data/cycle237/b005341.txt`](../data/cycle237/b005341.txt)) agrees at **all 3,000 terms, 0 mismatches** (checked incrementally to n = 3000). Example values: S18(10) = 20, S18(42) = 107,312, S18(43) = 139,984, S18(100) = 511,247,092,564.

## Method and window list
Windows exactly as in keys233 (fwd / rev, o 0–39, c 0 / 1) then × a for a ∈ {1, 3, 5, 7, 9, 11} as in keys234 (k → a·((S18 + c) mod 26) mod 26): 160 × 6 = **960 windows** (sha b43e35db…e414f), none duplicating earlier lists (keys217 / 218 / 221 / 233 / 234 / 236) or each other; none constant on the 24 crib seats (all 960 differ on the seats).
`gn217` model Q, forms Vig / variant / Beaufort, hit = ≥ 23 / 24 crib seats (EASTNORTHEAST 1-based 22–34, BERLINCLOCK 64–74); direct 86,731² `alpha.bin`, bank (165,065 rows) and all.bin (165,782 rows) 144² `themed144.bin`.

| scope | permutation rows | window-pair-forms | K4 hits (24 / 23) | 6 fresh nulls 209680–209685 | K4 time |
|---|---|---|---|---|---|
| direct | 1 | 2.17 × 10¹³ | 0 / 0 | 0 / 0 each (full) | 1 s |
| bank | 165,065 | 3.94 × 10¹³ | 0 / 0 | 0 / 0 each (rows ÷ 10) | 85 s |
| all.bin | 165,782 | 3.96 × 10¹³ | 0 / 0 | 0 / 0 each (rows ÷ 10) | 86 s |

**Deviation from PREREG237 (disclosed):** `runA.sh` filed the nulls at full scale in all three scopes. After K4's three scopes finished (171 s) a full-scale null showed ≈ 85 s per scope (≈ 17 min for six), over the ~8-minute budget, so I stopped my own `runA.sh` (killing its process group, nothing else) and ran the nulls with `runN.sh` at row stride 10 in bank / all.bin (direct full), as in cases 220 / 222. The K4 runs are as filed; the one partial null (209680 bank, direct) was discarded and re-run.
**Gate P (seed 209679):** 20 / 20 plants recovered with the planted (window, form, X, Y, permutation) (Wilson 0.84–1.00; 10 one-error plants included; multipliers drawn: a = 1 ×6, 3 ×3, 5 ×1, 7 ×1, 9 ×5, 11 ×4). **Gate T:** `check237.py` re-derived all 21 plant H lines (agreement mismatches 0); plant decrypts NC −5.26 … −3.96, every one above the I-342 bar (−7.01 at nq 64, N = 10; margin ≥ +1.75).
**Nulls:** six shuffled K4 texts, 0 hits in every scope — a machinery check, not a power calibration (the 24-seat filter predicts ≪ 1 chance hit per text).

## Reading (I-367)
- `EXACT-EXCL` for K4 within the 960 exact-S18 windows and model Q (one wrong crib letter tolerated; plants show the search finds such keys). The corrected S18 label replaces the "look-and-say" rows of cases 219 (a = 1) and 220 (a ≠ 1): those rows were "look-and-say then zeros" (near-constant keys, a period-1 key on most seats, long excluded), and this case is the real look-and-say test. The other 21 sequences and the four word-length streams of cases 219 / 220 are unaffected.
- No H line exists, so the I-342 NC bar was not exercised on K4 (third cycle in a row with 0 hits).
- Honest scope: S18 mod 26 for n ≤ 136 offsets 0–39, multipliers a ∈ {1, 3, 5, 7, 9, 11}, c ∈ {0, 1}. Not covered: even a, 13, Beaufort −a (I-368), the look-and-say *digit string* itself as a key (I-379), S18 in other moduli or on other alphabets.

## I-376 first pass: near-miss profile on the case 222 list
`gn237nm.c` = `gn217` plus a histogram of crib agreement over every candidate that shares a 4-seat block with the key (the index join); search and hit logic untouched. List: case 222's `keys236.bin` (8,792 windows); K4 vs **20 fresh shuffled nulls (209686–209705)**; direct (full) and all.bin (row stride 20). Statistic: per-text maximum agreement and the number of candidates at agreement ≥ 13.

| scope | K4 best agreement | null best (20 texts) | nulls ≥ K4 | rank p (1 + #≥)/21 | K4 candidates at ≥ 13 | null median [range] |
|---|---|---|---|---|---|---|
| direct | 13 (5 candidates) | 13 ×14, 14 ×6 | 20 / 20 | 1.00 | 5 | 8.5 [1–235] |
| all.bin (r20) | 13 (2 candidates) | 12 ×3, 13 ×16, 14 ×1 | 17 / 20 | 0.86 | 2 | 2 [0–5] |

Reading: K4 is **not** unusually close; its best partial fit (13 / 24, 54 %) is what shuffled texts reach (14 / 24 in 6 of 20 nulls in direct). The gap to a hit (23 / 24) is ten seats. `NO-SIGNAL` (descriptive, exploratory). Caveats (PREREG237): the maximum is over *index-matched* candidates (key equal on seats 0–3 or 13–16), not a global best; all.bin is sampled at row stride 20; only the case 222 list was profiled (other lists: I-380); the null count is 20 so rank p ≥ 1/21.

## Compute
K4 three scopes 171 s, six nulls 107 s, gate P 3 s, I-376 398 s: ≈ 12 min total wall of which ≈ 7 min heavy search (separate process group, `setsid timeout`), no other processes touched.

## News check (2026-11-23)
No new solution. State per public pages: plaintext found in Sanborn's papers (Sept 2025), archive sold (RR Auction, 20 Nov 2025), Paradigm verifier ($1 / try, announced June 2026), no method published `[secondary, mysteriesdept.com / paradigm.xyz]`. Community items seen, all unverified and already known to the repo: Andrew Chan's ChatGPT research record (kryptos.tiki.vc, 14 Sep 2026, bounded negatives), the akaalias/k4 Claude Code autoresearch loop (198 experiments / 12 families as of 2026-10-18, success criteria revised 2026-11-17, not solved), glthr's W-rectangle piece (updated 15 Nov 2026), r/KryptosK4_AI pipelines (Logica Omnium, solvekryptos.com dossier). None claims a verified K4 solution.

## Blind spots
Even multipliers and 13; Beaufort with −a; S18 digit string; other audioactive streams (the string, not the length; Conway element indices); window offsets > 39; other-moduli reads; I-376 on lists other than case 222 and a global (not index-matched) best.
