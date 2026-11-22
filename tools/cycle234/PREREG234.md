# PREREG234 — Cycle 234 (free slot, I-362 chunk 1): multiplied arithmetic-sequence key streams

Filed 2026-11-22 03:41 PT (America/Vancouver), **before** any plant, null or K4 run with `keys234.bin`. Base: origin/main **a736626** (c233 published). Case file 220.
Slots: 233 new family (case 219), so **234 is free**, 235 audit, 236 must be a new family (I-363). Seeds: plants **209645**, null **209646**; next free after this cycle **209647**.

## Disclosed before filing
- `gn217.c` unchanged (sha 97bae55f…d792), rebuilt `gcc -O3 -fopenmp -march=native`. `keys234.py` run once to build the list (no search).
- **Timing smoke** (no new seed): the already-published case 219 null text (seed 209644, `null233.txt`) through `keys234.bin`, bank at row stride 100 (offset 50) and direct at Y stride 20 (offset 7): 1.6 s and 1.1 s, 0 hits each. Used only to size the run; not part of any result.
- Frozen list: `keys234.bin` sha256 **369313455222b5cd4b1f581575d5757288a6e519cbad482dfbd282bd88f3e365** (20,860 windows; `keys234.tsv` sha 4ca55094…f66f lists a / family / offset / constant / direction).

## Idea (I-362, `[speculation]`)
Case 219 tested key streams k_i = f(n) + c for 22 named integer sequences and the K1–K3 word-length rhythms, but only with **multiplier 1**. A layered-simple variant multiplies the
sequence value: k_i = a·(f(n) + c) mod 26. Algebraically, a unit multiplier a is the same cipher as multiplier 1 with **both keyed alphabets decimated by a** (X'[j] = X[a·j], Y'[j] = Y[a·j]),
so this is "the case 219 streams on decimated keyed alphabets", which neither the keyword list (`alpha.bin`, closed under ×3 for 114 of 86,731 alphabets) nor `themed144.bin` (0 of 144) contains.
**Chunk 1:** a ∈ {3, 5, 7, 9, 11}. Because −a under Vigenère equals +a under variant, these five represent all ten units ≠ ±1 **for forms 0/1**; Beaufort with −a (a ∈ {15…25}) is a stated blind spot,
as are even multipliers and 13 (keys with only 13 or 2 values; I-362 chunk 2).

## Model and commands (as case 219)
`gn217` model Q, forms Vig / variant / Beaufort, hit = ≥ 23 / 24 crib seats (EASTNORTHEAST 0-based 21–33, BERLINCLOCK 63–73). Scopes direct (86,731² `alpha.bin`), bank and all.bin (144² `themed144.bin`).
`runA.sh`: K4 direct / bank / all.bin at full scale; null 209646 direct full, bank and all.bin at row stride 10. `runP.sh`: gate P.

## Gates and labels
- **P:** 20 plants (`plant234.py`, seed 209645; 0–7 direct, 8–13 bank, 14–19 all.bin; odd ids one corrupted crib letter); pass ≥ 19/20 recovered with the planted (w, form, X, Y, perm), Wilson reported.
- **T:** `check234.py` (= `check233.py`, docstring only) re-derives agreement for every H line; mismatches must be 0.
- **I-342 NC bar** for any decrypted H line: bar(nq, N) = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² − 0.0192 nq + 0.879, N = max(10, H lines in scope); candidate only if NC ≥ bar and English.
- **Labels:** K4 0 hits with P passing and null ≪ 1 expected → `EXACT-EXCL` within the list; hits failing the bar and null-like → `NO-SIGNAL`; P failing → `INSUFFICIENT-DISCRIMINATION`.
  One null is a smoke measure, not a calibration. FRONTEIRA / distance-to-bar rule (PREREG232) for any count comparison.

## Honesty clause
Any plain-English decrypt with both cribs at the official positions and NC ≥ bar is reported prominently and reproduced independently before being called a solution. Nothing is submitted anywhere.
