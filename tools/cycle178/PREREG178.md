# Cycle 178 pre-registration — linear-recurrence key mod 26 behind K3's decimation law (IDEAS I-137) + replication of case 165's C2 flag (I-133)

Written and pushed before any K4 or registered-null run. Smoke and timing runs used only the reserved shuffle seed 9178
(`random.Random(9178).shuffle(list(K4))`, I-116): all cells 0 fits on it; cost ≈ 10 s per text (M0 L 9 on 1/8 is 4.5 s of it).

## Question (new family behind the decimations)
Is K4 = transposition (one of the 165,782 K3-law decimations / routes, `all.bin`, md5 946402ca…) ∘ periodic-tableau substitution
whose key is an **affine linear recurrence over Z₂₆**, k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26), arbitrary weights c and
constant d (Fibonacci / tetranacci / LFSR-like keys, progressive keys and every period ≤ L are special cases)? Tableau A–Z or
KRYPTOS (key value = index difference in that alphabet), Vigenère (k = c − p) or Beaufort (k = c + p); variant = −Vigenère, which
maps the family onto itself (d → −d). Both layer orders. Cribs EASTNORTHEAST 21–33, BERLINCLOCK 63–73 (0-indexed). Strict
(no carving error). Cycles 80–81 ran this family direct and behind the 165,065 columnar bank only.

## Models (exact, `lr178.c`)
- **M0 — ix 0 (key on the plaintext index, then transpose), algebraic, L 1–9.** For each perm the 24 crib key values are known.
  The recurrence equations inside the crib blocks (i = 21+L…33, 63+L…73) are linear in x = (c₁…c_L, d): solved over GF(2) and
  GF(13) separately (Z₂₆ ≅ Z₂ × Z₁₃), every solution enumerated, k[34…73] propagated from the 13 block-1 values mod p and all 11
  BERLINCLOCK values required. Fit ⇔ a mod-2 and a mod-13 solution both survive; #solutions mod 26 = n₂·n₁₃. The seed upstream of
  position 21 is not required to exist (superset of every seed, including vocabulary seeds). L 1–8 full perm set for every text;
  **L 9: K4 on the full set AND on `all_s8.bin` (every 8th perm), nulls on `all_s8.bin`** (cost).
  Expected false fits per (perm, alphabet, form) ≈ 26^(2L+1−24): L 8 ≈ 2·10⁻¹⁰, L 9 ≈ 8·10⁻⁸ × 663k ≈ 0.06 on the full set.
- **M1 — ix 1 (transpose first, key on the carved index, arbitrary seed at carved 0…L−1, which covers any start offset), L 1–5,
  CRT.** Mod 2: all 2^(2L+1) streams as 97-bit words; a (perm, alphabet, form) passes iff some stream matches the 24 key bits.
  Survivors: for every c mod 13 the stream is linear in (seed, d) (precomputed basis table); 24 equations by incremental
  elimination over GF(13). Fit ⇔ both moduli consistent. Full perm set for every text.
- **W0 / W1 — small weights, vocabulary seeds, L 6–10.** c ∈ {0,1}^L \ {0} (LFSR / lagged-Fibonacci style), d ∈ Z₂₆, seed = the
  first L letters of one of 74 vocabulary words (`seeds178.txt`, md5 10c14f09…), numbered A–Z or KRYPTOS; W0 seed at plaintext
  0…L−1 (exact 24-letter hash join), W1 seed at carved 0…L−1 (decrypt + triple-position index). Full perm set, every text.
  (W0 at L ≤ 9 is a subset of M0 and serves as an internal cross-check: every W0 fit with L ≤ 9 must appear in M0.)
- Not tested (blind spots, declared now): M0 L ≥ 10 with arbitrary weights; M1 L ≥ 6 with arbitrary weights; non-zero seeds
  offsets for W (seed at another position); keyed (Quagmire) alphabets other than A–Z / KRYPTOS; non-linear generators; one error.

## Texts
K4 (`data/k4.txt`, md5 dc4df49d…). 19 nulls = `random.Random(s).shuffle(list(K4))`, s = **17811…17829** (`nulls178.txt`).

## Labels (per model × ix × L cell)
- K4 0 fits → `EXACT-EXCL` (under the stated model), the analytic false-fit rate and the null counts quoted as the power statement.
- K4 > 0 inside the null range → `LOW-POWER`; decodes → `NO-SIGNAL` if K4's best is inside the null range and far below the plants.
- K4 above every null → flagged and decoded, never called a signal without a readable decode.
- Solution criterion: a full coherent English decryption of the 97 letters with both cribs, reproducible.

## Decodes
Every K4 fit (any cell) and every fit of the first 5 nulls is replayed at string level (Python, independent of the C code;
representative solution = CRT of each listed mod-2 / mod-13 solution, up to 32 × 32 combinations) and decoded: M0 positions
21–96 forward (and 0–20 backward when c_L is a unit), M1 / W all 97. Score = mean log10 quadgram (support/quadgrams.json) over
off-crib windows.

## Grid (I-120 rule, unchanged)
Scored cells: R1 M0 L 1–8 fits; R2 M0 L 9 fits (s8); R3 M1 L 1–5 fits; R4 W0 fits; R5 W1 fits; D1 M0 **mod-2 pass count**
L 7–8 (full) + L 9 (s8); D2 M1 mod-2 pass count L 1–5 (full). D1 / D2 are diagnostics of the mod-2 layer (not exclusion
statistics). Leave-one-out exact Poisson tails per cell, all-zero cells reported and not scored; G± = min over scored cells;
grid p = fraction of the 20 texts with G ≤ G(K4); best attainable 0.05; both tails reported.

## Controls (`plant178.py`, seed 17800, independent string-level encryptor; each plant behind a perm q of all.bin; run on
q ± 1,500 of all.bin with the model/L it belongs to)
P1 M0 L3 A–Z Vig; P2 M0 L6 KA Beau; P3 M0 L8 A–Z Beau; P4 M0 L9 KA Vig; P5 M0 Fibonacci c = (1,1), d 0, seed KR (KA numbering),
KA Vig; P6 M1 L2 A–Z Beau; P7 M1 L4 KA Vig with a non-unit last weight; P8 M1 L5 A–Z Vig; P11 M1 L3 KA Beau; P9 W1 L7 seed
PALIMPS… (KA numbering) KA Beau; P10 W0 L10 seed BERLINCLOC (A–Z numbering) A–Z Vig; P12 W0 L6 seed KRYPTO (KA numbering) A–Z Beau.
Pass = found at its planted q with the planted (c mod 2, c mod 13, d) among the listed solutions (M0/M1) or the exact planted
word / weights / d (W), and the replayed decode equals the planted plaintext on every position it determines.
Negatives (must be missed at the planted q, every L in the run): N1 = P1 with one wrong carved crib letter; N2 = random key behind
M1 L 1–5; N3 = P9's stream shifted by one position (seed not at 0) behind W1.
**Independent recount** (`recount178.py`, numpy brute force, no algebra): M0 L 1–3 over all 26^(L+1) (c, d) and M1 L 1–2 over
all 26^(2L+1) streams on a slice (all.bin[::4000] + the planted perms of P1, P5, P6, P11, P12), K4 + 2 nulls + those plants; and W0/W1
L 6 by direct string replay on the same slice. Fit sets and solution counts compared line by line with lr178.

## Add-on I-133 (pre-registered replication of case 165's C2 flag; single cell, one-sided)
Statistic: `gm177` (tools/cycle177, unchanged) err 1, ix 0, L 6, base 10, full all.bin, **sum of the one-error-only column over
the 4 (alphabet, form) rows**. K4 is rerun and must reproduce 230. Fresh set F: 40 shuffles, seeds **17841–17880**
(`fresh133.txt`). Matched set M: candidate seeds 17901, 17902, … in order, a shuffle accepted iff its mean crib-slot equal-pair
count over the perm set (eqpairs177 definition) is within ±0.02 of K4's 9.8983, until 20 are accepted (cap 600 candidates).
p_F = (1 + #{F ≥ K4}) / 41, p_M = (1 + #{M ≥ K4}) / 21, pooled p = (1 + #{F∪M ≥ K4}) / 61.
**Decision:** replicated ⇔ p_F ≤ 0.05 AND p_M ≤ 0.05; not replicated ⇔ pooled p > 0.05; otherwise "weak / inconclusive".
Not replicated closes the flag (case 165's p⁺ 0.05 was the floor of a 19-null grid with the crib-repeat covariate). Even if
replicated, it is a count anomaly of a family whose 256 decodes were gibberish, not a solution.

## Budget
~8 min heavy in total, one 6-thread job at a time, own process group under `setsid timeout`; resumable (jobs ending in END skipped).
