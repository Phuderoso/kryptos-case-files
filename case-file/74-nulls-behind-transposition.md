# 74 — Nulls between the cribs, behind transpositions (cycle 76)

**Type:** audit/extension (diversity rule: cycle 75 was a new structure, so 76 may extend). Extends case file 73
(nulls + periodic key, direct) and the cycle 19/22 transposition engines (case files 18, 21) with the null count
between the cribs as an extra loop. Idea (1) of cycle 75.

## Model (A)
Plaintext P (no nulls) → substitution, key indexed by plaintext position → null letters dropped in anywhere
outside the two crib spans (b of them between the cribs, any number before/after) → transposition → carved.
Undoing the transposition gives X with X\[i\] = carved\[perm\[i\]\]; EASTNORTHEAST sits at X 22–34 and BERLINCLOCK at
X 64–74 (1-based, Sanborn's positions), and their plaintext-stream indices are 21+j₁ and 63+j₂−b (0-based, up to a
common shift that never matters). Only b (0–29) changes anything.

- **F0 periodic key**, p 1–26, b mod p (351 effective (p, b) per text and tableau/mode).
- **F1 plaintext-fed autokey**, lag L 1–96, b 0–29, and **F2 ciphertext-fed autokey**, same. The null positions in
  the gaps are unknown, so the only exact checks are between two crib letters at stream distance L: inside one crib
  (L ≤ 12) or across (j₂ − j₁ = d = L − 42 + b). Deduplicated to 113 effective configurations (L ≤ 12 alone,
  L ≤ 12 with a cross distance d, or d alone). Exact, necessary conditions; no English scoring.
- Tableaux KRYPTOS (KA) and A–Z; Vigenère/Beaufort/variant in tableau index space (K1/K2's own arithmetic); 165,065
  transpositions of the cycle-19 family plus identity (`perms97.bin`). Per text: 3.48 × 10⁸ periodic and
  2 × 1.12 × 10⁸ autokey configurations. Plain per-class consistency; no Bean-style pruning.

Model B (transpose first, then a key that skips nulls) is not testable this way: every crib letter's key index then
depends on how many nulls the transposition put before it. If nulls are enciphered like other letters, nothing
changes from cycles 13/19/22.

## Power (`tools/cycle76/summarize76.py`)
With ≥ 6 exact checks as the decision line (no shuffled text reached 6; see below):
periodic p 1–18 are testable for **every** b; p 19–26 for 50–68 % of b. Autokey: 92 of 113 effective configurations
are testable; blind: L 10–12 without useful cross pairs, and cross distances d −12…−8 and 6…10 (few overlapping
letters).

## Controls (`tools/cycle76/controls76.py`, `analysis/cycle76_controls_planted.json`)
English plaintext (cycle-74 corpus), random family transposition, random null letters at random non-crib slots:

| # | planted | recovered | checks | configs with ≥ as many checks |
|---|---|---|---|---|
| 0 | KA Vigenère p 7 SHADOWS, a 4 b 9 c 6 | yes | 17 | 2 |
| 1 | AZ Beaufort p 11 ABSCISSAPAL, a 2 b 17 c 3 | yes | 13 | 1 |
| 2 | KA Vigenère PT-autokey L 8 primer PALIMPSE, b 24 | yes | 11 | 1 |
| 3 | AZ variant PT-autokey L 37 (random primer), b 10 | yes | 6 | 1 |
| 4 | KA Beaufort CT-autokey L 3 primer KRY, b 29 | yes | 21 | 1 |
| 5 | AZ Vigenère CT-autokey L 40 (random primer), b 0 | yes | 11 | 12 (same X at the crib slots under related transpositions) |

**6/6 recovered**, each at or near the top of its own run.

## Result (`analysis/cycle76_summary.json`, `analysis/cycle76/`)
| family | K4 max checks (all consistent) | 20 shuffled K4: max checks | K4 configs ≥ 4 checks | shuffled ≥ 4 (min–median–max) |
|---|---|---|---|---|
| F0 periodic | 5 (2 configs: AZ, p 19, b ≡ 13) | 4–5 (5 in 6/20) | 12 | 2–27.5–91 |
| F1 PT-autokey | 4 | 4–5 (5 in 10/20) | 6 | 3–6–270 |
| F2 CT-autokey | 4 | 4–5 (5 in 2/20) | 4 | 2–6–54 |

K4 sits inside the shuffled baseline in every family, and **no configuration with ≥ 6 checks is consistent**.
The two 5-check periodic cases are p 19 (partly blind period) and at the shuffled level.

## Verdict
**Negative.** Nulls between the cribs do not rescue a periodic (p ≤ 18 fully, p 19–26 partly), plaintext-autokey or
ciphertext-autokey key behind any of the 165,065 transpositions on the KA or A–Z tableau (model A).
Still open: model B; nulls + running key (idea 2 of cycle 75); arbitrary alphabets with nulls behind transpositions;
transpositions outside the cycle-19 family. No plaintext found; nothing to submit.

Reproduce: `cd tools/cycle76 && sh run76.sh` (about 1 min on 8 cores).
