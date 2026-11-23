# PREREG237 — Cycle 237 (free slot): I-367 look-and-say S18 repaired + I-376 near-miss profile

Filed 2026-11-23 03:47 PT (America/Vancouver), **before** any plant, null or K4 run with `keys237.bin`. Base: origin/main **9ed3d33** (c236 is already published there: tree ab7d48ea = local 2b10629). Case file 223.
Slots (I-378): **237 free**, 238 audit, 239 new family, 240 free. Seeds: plants **209679**, main nulls **209680–209685**, I-376 nulls **209686–209705**; next free after this cycle **209706**.

## Disclosed before filing
- `gn217.c` unchanged (sha 97bae55f…d792), rebuilt `gcc -O3 -fopenmp -march=native`. No timing smoke with new seeds; no search was run before filing.
- S18 repair code written and validated this cycle before filing (`las_exact.py`): the 92 audioactive atoms are **derived in code** (split a term-16 string at cut points whose 9-step evolutions never interact, close under decay), not copied from a table. Validation: direct strings n ≤ 45 equal, **OEIS A005341 b-file n ≤ 3000: 0 mismatches** (`data/cycle237/b005341.txt`, fetched from oeis.org, sha 8000706b…d417). The lengths used (n ≤ 136) are therefore exact.
- Frozen list: `keys237.bin` sha256 **b43e35db…e414f**, 960 windows (`keys237.tsv` sha 030a8766…6316). No duplicates among the lists keys217 / 218 / 221 / 233 / 234 / 236 or inside it; 0 windows constant on the 24 crib seats.
- `plants237.tsv` (seed 209679) was generated before filing (sha cef6cbab…2e) and not run.

## What S18 was (I-367)
`keys233.py` S18 = length of look-and-say term n (term 1 = `1`), but `las()` stopped generating at 10⁵ characters (term 42) and `S18(n)` returned **0** for larger n. Case 219 windows (offsets 0–39, n up to 136) and case 220's ×a copies therefore were partly "look-and-say then zeros", the BERLINCLOCK seats always in the zero tail.
**Repair:** exact S18(n) mod 26 for all n ≤ 136 (values grow to ~10¹⁶; bigints in Python).
Windows exactly as keys233 defines for sequences: fwd k_i = S18(1+o+i)+c, rev k_i = S18(1+o+96−i)+c, o = 0..39, c ∈ {0,1}; then k → a·k mod 26 for a ∈ {1,3,5,7,9,11} (as keys234; case 219 had a = 1, case 220 a ≠ 1). 160 × 6 = **960 windows**.

## Model and commands (as cases 219 / 220 / 222)
`gn217` model Q, forms Vig / variant / Beaufort, hit = ≥ 23 / 24 crib seats (EASTNORTHEAST 1-based 22–34, BERLINCLOCK 64–74); scopes direct (86,731² `alpha.bin`), bank (165,065 rows), all.bin (165,782 rows), 144² `themed144.bin`.
`runA.sh`: K4 full scale in the three scopes; 6 fresh nulls (`mknull237.py`, 209680–209685) at **full** scale in all three scopes (cheap list). `runP.sh`: gate P (`plant237.py`, seed 209679; ids 0–7 direct, 8–13 bank, 14–19 all.bin; odd ids carry one corrupted crib letter, so 10 one-error plants; Y stride 1000 / row stride 2000 slices).

## I-376 near-miss profile (secondary, `[method]`)
`gn237nm.c` = gn217 with one addition: a histogram of crib agreement over every candidate that matches a 4-seat block (the same index join); search and hit logic untouched.
`runNM.sh`: window list = **case 222 `keys236.bin`** (8,792 windows). K4 vs **20 fresh shuffled nulls (209686–209705)**, scopes: direct (full) and all.bin (row stride 20, offset 0). Statistic: per text, the **maximum agreement** found (one-sided rank p of K4 among 21 = (1 + #nulls ≥ K4) / 21), plus the number of candidates at agreement ≥ 15.
Caveat registered in advance: this is the best agreement among *index-matched* candidates (those equal to the key on seats 0–3 or 13–16), not a global best; it is a near-miss profile for this search, not a distribution over all keys. No label beyond `NO-SIGNAL` (rank p > 0.05) or "K4 unusually close" (rank p ≤ 0.05, descriptive; a single exploratory statistic, not a discovery).

## Gates and labels
- **P:** 20 plants, pass ≥ 19 / 20 recovered with planted (w, form, X, Y, perm), Wilson reported. **T:** `check237.py` re-derives agreement for every H line and decrypts all 97 letters; mismatches 0.
- **I-342 NC bar** for any decrypted H line: bar(nq, N) = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² − 0.0192 nq + 0.879, N = max(10, H lines in scope); candidate only if NC ≥ bar **and** the 97 letters read as English.
- **Labels:** K4 0 hits with P passing → `EXACT-EXCL` within the frozen list and model (one wrong crib letter tolerated); hits failing the bar and null-like → `NO-SIGNAL`; P failing → `INSUFFICIENT-DISCRIMINATION`. Plants validate recovery within this scope only; the I-376 profile is `NO-SIGNAL`-type heuristics.
- Nulls: six shuffled texts, calibration of false hits (not power).

## Honesty clause
Any plain-English decrypt with both cribs at the official positions and NC ≥ bar is reported prominently and reproduced independently before being called a solution. Nothing is submitted anywhere.
