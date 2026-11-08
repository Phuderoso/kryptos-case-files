# Case file 132 — Hill + additive key of an independent period

**Cycle 144, 2026-11-08. Variant of cycle 143** (case file 131 tested only a shift whose period equals the block size).

## Model
Hill decryption on n-letter blocks followed by a Vigenère-style additive key of period k, with k free of n
(in encryption order: Vigenère first, then Hill — the kind of two-step layering K1–K3 used, a keyed substitution
and a second, structural step). Decoder: `out[t] = D·c_block + e[t mod k]`.

All n² + k unknowns are solved **jointly and exactly** from the 24 crib letters (21–33 EASTNORTHEAST, 63–73 BERLINCLOCK)
by Gaussian elimination mod 2 and mod 13, then CRT. No search, no hill-climbing: a configuration either admits a key or it does not.

Tested: n = 2 with k = 1–14, n = 3 with k = 1–10, n = 4 with k = 1–4; every alignment; A–Z and KRYPTOS numbering;
direct and behind all 330,130 bank permutations in both index orders (model Q and carved). About 98 million configurations per text.

## Controls (`data/cycle144/controls_check.txt`)
Six planted encryptions of the English control text — n2 k7 direct, n3 k5 model Q, n2 k11 carved, n3 k8 carved (inverse entry),
n4 k3 model Q, n2 k13 direct KRYPTOS — **all six recovered word-perfect (−4.04 to −4.13)**.

## Results (`data/cycle144/results.txt`; 170 s on 8 processes)
- **n = 2, all k 1–14: every K4 configuration inconsistent** (37 M), same for both nulls.
- n = 3: inconsistent for k 1–8; k 9–10 leave 4 and 22 survivors, best −7.63 (nulls: 4 and 62 / 14 survivors, best −7.77 to −8.13).
- n = 4: k 1–2 nothing; k 3 134 survivors best −7.61 (nulls 118 / 86, −7.36 / −7.56); k 4 reproduces cycle 143 exactly (224, −7.19).
- No configuration of any text came within 2.5 points of English (≈ −4.1). Nothing above the print threshold (−4.6).
- No configuration was left underdetermined at these sizes, so the search is exhaustive over its space.

## Verdict
**Negative.** K4 is not a Hill 2×2 (+ key period ≤ 14), 3×3 (+ period ≤ 10) or 4×4 (+ period ≤ 4) cipher, direct or behind the
165k transposition bank, under A–Z or KRYPTOS numbering. Survivor counts and scores match the shuffled nulls.

## Limits
- Longer key periods (each extra period letter removes a crib check; n = 2 k ≥ 15 is close to underdetermined).
- Key applied before the Hill step on the ciphertext side (`p = D·(c − f)` with f of period ≠ n) — that system is not linear in (D, f) and is not covered.
- Keys from a mixed alphabet (Quagmire-style), other numberings, transpositions outside the bank.
