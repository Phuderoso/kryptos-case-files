# Case file 134 — periodic key with a Vigenère-or-Beaufort choice per phase

**Cycle 146, 2026-11-08. New structure.**

## Idea
K1–K3 used plain Vigenère; K2's tableau and the Beaufort/variant forms have each been tested only as one global
choice. A deliberately mischievous layer would flip direction on some key letters (a "one-letter anomaly" in the key
rather than the text). With period P, phase j gets its own key letter *and* its own direction, 2^P·26^P settings, yet
each phase is checked independently and exactly from the cribs (L−p constant for Vigenère, L+p constant for Beaufort).

## Test
P 1–28, A–Z and KRYPTOS numbering, direct and behind all 165,065 bank permutations (both directions, model Q and
carved): 3.70 × 10⁷ configurations per text in 7 s. Texts: K4 and two shuffled K4s. Controls: six planted mixed keys
(P 5–19, direct, bank, inverse bank) all recovered as full English (meanQ about −4.1).

## Result
Direct: nothing consistent for P ≤ 26 (K4 or nulls). Behind the bank about 1.38 million configurations are consistent
for every text, nearly all with 0–3 checks (underdetermined). At ≥ 4 independent checks: K4 2 (one bank pair, P 27,
best meanQ −7.20), null 1 2, null 2 2; at ≥ 5: none for anyone. **Negative**: K4 is indistinguishable from shuffled text.
Larger P (29+) is crib-underdetermined: P 29 alone passes with 10 "checks" and unreadable text for K4 and nulls alike,
so it was excluded from the claim.

## Limits
Key period ≥ 27 behind transpositions; mixed direction on a mixed (non-tableau) alphabet; autokey with per-step direction;
double transposition outside the bank.
