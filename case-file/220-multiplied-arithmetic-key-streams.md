# Case 220 — Multiplied arithmetic-sequence key streams (decimated keyed alphabets) (cycle 234)

**Slot:** free (233 new family, 235 audit, 236 new family; I-363). Idea **I-362 chunk 1** (tested here); new **I-367–I-369**.
Pre-registered as [PREREG234](../tools/cycle234/PREREG234.md) (local commit, 2026-11-22 03:41 PT, before any plant, null or K4 run). Code and window list: [`tools/cycle234/`](../tools/cycle234/)
(`keys234.py`, `keys234.tsv`, `plant234.py`, `check234.py`, `runA.sh`, `runP.sh`, `HASHES234.txt`); tool `gn217` **unchanged** (source sha 97bae55f…d792); raw results (stamped, rule 5): [`data/cycle234/`](../data/cycle234/).
**Verdict: no solution.** K4 has 0 hits (0 exact, 0 with one wrong crib letter) in all three scopes: `EXACT-EXCL` within the frozen 20,860-window list (gate P 20/20).

## The idea
[Case 219](219-arithmetic-sequence-key-streams.md) tried 22 named integer sequences and the K1–K3 word-length rhythms as keys, k_i = f(n) + c, with multiplier 1 only. Here k_i = a·(f(n) + c) mod 26 for
a ∈ {3, 5, 7, 9, 11}. A unit multiplier is the same cipher as multiplier 1 with **both keyed alphabets decimated by a** (X′[j] = X[a·j], Y′[j] = Y[a·j]), and the repo's alphabet lists are
almost never closed under decimation (`alpha.bin` 114 of 86,731 under ×3; `themed144.bin` 0 of 144), so this is genuinely new coverage: "the case 219 streams on decimated keyed alphabets".
Because −a under Vigenère equals +a under variant, the five multipliers represent all ten units ≠ ±1 for those two forms. `[speculation]`: no source says Sanborn used a sequence key.

## Method
`keys234.py` rebuilds the full case 219 list (4,172 windows; the cross-list dedup of case 219 removed none) and multiplies each window by a; windows equal to any in `keys217/218/221/233.bin` or earlier in the list are dropped (none were).
20,860 windows (4,172 per a), sha 36931345…f365. `gn217` model Q, forms Vig / variant / Beaufort, ≥ 23 / 24 crib seats (EASTNORTHEAST 0-based 21–33, BERLINCLOCK 63–73).

| scope | permutation rows | window-pair-forms | K4 hits (24 / 23) | null 209646 | K4 time |
|---|---|---|---|---|---|
| direct | 1 | 4.71 × 10¹⁴ | 0 / 0 | 0 / 0 (full) | 21 s |
| bank | 165,065 | 8.57 × 10¹⁴ | 0 / 0 | 0 / 0 (rows ÷ 10) | 139 s |
| all.bin | 165,782 | 8.61 × 10¹⁴ | 0 / 0 | 0 / 0 (rows ÷ 10) | 139 s |

(window-pair-forms = T-line `pairforms` × windows for the families; the direct T line already counts windows.)
**Gate P (seed 209645):** 20 / 20 plants recovered with the planted (window, form, X, Y, permutation) (Wilson 0.84–1.00; 10 one-error plants included). **Gate T:** `check234.py` re-derived every plant H line (434 lines), agreement mismatches 0.
Plant 17 (all.bin, a 9, S18 look-and-say, o 23) returned 410 H lines and plant 10 six: many windows share the same key on the crib seats (see I-367); the planted configuration was among them both times.
**Null:** one shuffled K4 (`random.Random(209646)`), 0 hits in every scope — a smoke measure, not a calibration.
**Timing smoke (disclosed in PREREG234):** case 219's published null text at row stride 100 / Y stride 20 before filing, 0 hits; not part of any result.

## Reading
- `EXACT-EXCL` for K4 within the list and the model (one wrong crib letter tolerated; the plants show the filter finds these keys, one-error included).
- With **zero** H lines the I-342 NC bar was again **not exercised** on K4 (second cycle in a row; I-364 is being exercised blind by Voynich on a hit-rich crib subset, not repeated here).
- Compute: K4 ≈ 5 min, null ≈ 50 s, plants ≈ 1 min, inside the 8-minute budget.

## Found while checking the plants (I-367)
`keys233.py` builds S18 (look-and-say lengths) as real values only for n ≤ 42 (the string is cut at 10⁵ characters) and **0 beyond**. Every S18 window (offsets 0–39, n up to 136) is therefore a
partly constant-zero stream; the BERLINCLOCK seats always sit in the zero tail. So **case 219's and this case's S18 rows test "look-and-say then zeros", not look-and-say**. Near-constant keys are a periodic
key of period 1 on most seats (long excluded), so nothing is lost for K4, but the S18 label in case 219 is wrong as written. Fix: look-and-say lengths mod 26 via Conway's 92-element audioactive decomposition (exact, no string) — queued as I-367. Case 219 gets an addendum pointing here.

## Blind spots
Beaufort with −a (a ∈ 15–25); even multipliers and 13 (I-368); constants c > 1 beyond the A=0 / A=1 reading; offsets > 39; other-language names; sequence-rank alphabets; S18 proper (I-367). One-error beyond 23 / 24 not covered.

## Addendum (cycle 237)
The S18 ×a rows (I-367) are re-done with exact look-and-say lengths in [case 223](223-look-and-say-s18-repaired.md) (a ∈ {1, 3, 5, 7, 9, 11}, 960 windows): K4 0 hits in all three scopes → `EXACT-EXCL`.
