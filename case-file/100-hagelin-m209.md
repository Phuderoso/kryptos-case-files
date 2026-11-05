# 100 — Hagelin M-209 / C-38 pin-and-lug machine, directly on the copper (cycle 111)

> *The CIA's own era ran on Hagelin. Crypto AG, Rubicon, the M-209 in every Army field bag. If Ed Scheidt wanted a machine key for Sanborn, this was the one on the shelf.*

## Why this family
The coverage table listed "pin wheels" as open after the single-rotor work (case file 90). The M-209 is the most likely machine for an American cryptographer of Scheidt's generation. It is new to the case files.

## Model
- Six pin wheels of periods 26, 25, 23, 21, 19, 17, all stepping one place per letter. Pins are arbitrary bits; the starting positions are absorbed into the pins.
- A 27-bar lug cage. Each bar carries 0, 1 or 2 lugs, so the cage is 21 counts (6 single-wheel types, 15 two-wheel types) summing to ≤ 27. The key at letter i is the number of bars with at least one lug on a wheel whose active pin is up (overlaps counted once), so k ∈ 0–27.
- Mode 0 is the real M-209: c = (25 + k − p) mod 26 (Beaufort type, straight alphabet). Mode 1 is the additive (Vigenère type) form.
- Cribs: EASTNORTHEAST at 21–33 and BERLINCLOCK at 63–73 (0-indexed).

## Tests and results (`tools/cycle111/`, `analysis/cycle111_m209.txt`)
1. **Exact Z3 model** (integer lug counts, Boolean pins, both modes, fixed or free offset): every check hit the 60 s timeout. **No verdict.** A CP-SAT or a custom DFS over wheel residues is needed.
2. **Crib-only local search** (60 restarts × 600k moves, quadgram weight 0). Planted M-209 controls (three English texts with the cribs inserted, random pins and lugs, both modes): **6/6 reach 0 crib mismatches**. **K4: best 2 (mode 0) and 1 (mode 1) mismatches.** Shuffled K4 nulls: **2 of 8 reach 0**, the rest 1–2. So K4 sits inside the null range. Not finding a fit is not a proof, and random texts sometimes fit, so the cribs alone have little power here.
3. **Whole-text annealing** (quadgram + 0.5 per crib mismatch, 40 restarts × 2M moves): the controls reach 0 mismatches, but **none of the six planted plaintexts is recovered**. Their output is crib-correct nonsense around −5.9 to −6.2. That means 97 letters are too few for this attack. K4 is best at 1 mismatch (−6.19), and the nulls fall between −5.73 and −6.43.

## Verdict
**Inconclusive, leaning negative.** Local search finds no crib-consistent M-209 for K4, while it finds the planted ones every time. But 2 of 8 shuffled texts are consistent, so the cribs barely constrain this machine, and whole-text scoring has no power at 97 letters. Not excluded.

## Still open
- An exact feasibility proof (CP-SAT/DFS) for K4 and 50+ nulls, to make "K4 fits or doesn't" a fact.
- Historical lug rules (M-209 training tables, no empty bars), which would shrink the space and could add power.
- M-209 behind a transposition. With no power directly, this is not worth running before the exact test.
