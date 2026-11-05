# 100 — The feedback key (cycle 108)

**Question.** Every key-stream family in the case files so far is either autonomous (periodic, progressive, linear recurrence, cycle 80) or a pure copy of the text (autokey, cycles 19–23). A hand cipher can also mix them: each new key letter is the last key letter, scaled, plus the previous plaintext or ciphertext letter, plus a constant. The classic member is the *cumulative autokey* (key = running sum of all earlier plaintext), which none of the earlier cycles tested.

**Model.** k[j] = a·k[j−1] + b·p[j−L] + e·x[j−L] + d (mod 26), with x the cipher stream before the transposition, L = 1–8, all 26⁴ choices of (a, b, e, d). This contains: constant key (a = 0, b = e = 0), progressive key (a = 1), plaintext and ciphertext autokey at lag L (a = 0), cumulative plaintext / ciphertext autokey (a = 1, b or e = 1), and every affine mix. Tableaux: Vigenère and Beaufort on A–Z and on the KRYPTOS alphabet, with letters numbered in that alphabet (variant Beaufort is Vigenère with the signs flipped). Layers: substitution, then any of the 165,065 transpositions of `tools/export_perms.py` (identity included, so the direct case is covered).

**Method (exact).** Inside the two cribs the equations are linear in (a, b, e, d). They are solvable mod 26 exactly when they are solvable mod 2 and mod 13 (Gaussian elimination). Every survivor is then expanded to all of its (a, b, e, d) solutions, the key is run forward from EASTNORTHEAST through the 29-letter gap, and all 11 letters of BERLINCLOCK must come out.

**Results** (`tools/cycle108/fbkey.c`, raw output `data/cycle108/results108.txt`):

| | L 1–3 | L 1–8 |
|---|---|---|
| K4 crib-consistent / full (BERLINCLOCK reproduced) | 0 / **0** | 1 (4 checks) / **0** |
| 20 shuffled K4 (L 1–3), 8 (L 1–8) | 0 / 0 in all | 0–14 / 0 in all |
| 8 planted controls (random transposition, tableau, L 1–7, a, b, e, d) | true setting found, 14–19 checks | same, 4–8 checks for L 6–7 |

**Verdict: negative.** No feedback key of this form, with lag ≤ 8, on these four tableaux, direct or behind 165,065 transpositions, turns EASTNORTHEAST into BERLINCLOCK. This closes the cumulative autokey and its affine relatives in this family of layers. Open: arbitrary alphabets (both sides free), lags > 8, and the transposition-first order (where the key would run along the carved order and the cribs scatter).
