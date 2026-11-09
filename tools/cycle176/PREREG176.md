# Cycle 176 pre-registration — Gromark behind K3's decimation law (IDEAS I-125)

Written and pushed before any K4 or registered-null run. Smoke runs used only the reserved shuffle seed 9176 (I-116).

## Question
Does an ordinary Gromark (chain-added digit key, any cipher alphabet) or an ACA Periodic Gromark built from a vocabulary keyword
fit the 24 crib letters behind one of the 165,782 K3-law decimations / spiral-diagonal routes (`all.bin`, cycle 168), in either
layer order? Cribs: EASTNORTHEAST at plaintext index 21–33, BERLINCLOCK at 63–73 (0-indexed). Strict (no letter errors).

## Models (exact)
- **G (ordinary Gromark), `gm176.c`.** d[i] = d[i−L] + d[i−L+1] mod 10 from a primer of length L. Plaintext alphabet A–Z or
  KRYPTOS; **cipher alphabet arbitrary** (any bijection, so every keyword-mixed or KRYPTOS-keyed alphabet is included).
  Vigenère w = PA(p) + d, Beaufort w = d − PA(p) (variant = Beaufort after reflecting the arbitrary alphabet). A config fits iff
  equal carved letters ⇔ equal w over the 24 crib slots.
  - ix 0 (Gromark on the plaintext index, then transpose): all 10^L primers, **L 2–8**, hash join over the perms.
  - ix 1 (transpose, then Gromark on the carved index): all 10^L primers, **L 2–5**, brute force.
  - Named primers (`mkcfg176.py primers`, 22,121): ACA numerical keys (ranks, 10→0) of the cycle-129 vocabulary (themed list,
    10,056 words, themed pairs), raw and with repeats removed, L 3–16, plus 17 dates/coordinates (K2 coordinates, 1990, 11/3/1990,
    11/9/1989, 26/11/1922 …), both ix.
- **PG (ACA Periodic Gromark), `pg176.c`.** Cycle 129's key-stream construction (reproduces the ACA ENIGMA example) for every
  vocabulary keyword (dedup length 3–12, 17,164 keywords), cipher alphabets aca / mix / ka and the new **kmix** (keyword + KRYPTOS
  order), plaintext A–Z or KRYPTOS, Vigenère (ACA) and Beaufort, both ix. All alphabets fixed, so each crib letter is an exact
  prediction. 137,312 configs × 2 forms × 165,782 perms × 2 ix.

## Texts
K4 (`data/k4.txt`) on the full perm set for every model. 19 nulls = K4 shuffled with `random.Random(s)`, s = 17611…17629:
ix 0 on the full perm set (G L 2–7 for all 19, G L 8 for the first 9; named primers; PG); ix 1 on every 8th perm (`all_s8.bin`):
G L 2–5 and named primers. K4 is also run on `all_s8.bin` for ix 1. PG both ix on the full set for all 19.

## Labels (per model × ix × L cell)
- K4 0 fits → `EXACT-EXCL` (under the stated model), with the null mean quoted as the power statement.
- K4 > 0 inside the null range → `LOW-POWER`; every K4 fit at L ≤ 7 (ix 0), all ix 1, named-primer and PG fits are decoded:
  the crib-fixed part of the cipher alphabet is kept, the free part is filled by hill-climbing English quadgrams (same budget for
  K4, nulls and plants); `NO-SIGNAL` if K4's best decode is inside the null decodes' range and far below the plants.
- K4 above every null in a cell → reported as a flag, decoded, not called a signal without a readable decode.
- Solution criterion: a full 97-letter coherent English decryption with both cribs in place, reproducible.

## Grid (I-110/I-115/I-117/I-120)
Five cells: C1 G ix0 L 2–6 (summed), C2 G ix0 L 7, C3 G ix1 L 2–5 (1/8 perms), C4 named primers ix0 (full) + ix1 (1/8),
C5 PG (both ix). Per cell, exact Poisson tails of each text's count against the mean of the other 19 texts (leave-one-out):
p⁺ = P(X ≥ x), p⁻ = P(X ≤ x). Cells where all 20 texts are 0 are reported, not scored (I-115). Grid statistic
G⁺ = min p⁺ over scored cells (G⁻ likewise); grid p = fraction of the 20 texts with G ≤ G(K4). Best attainable 0.05.

## Controls
`plant176.py` (independent string encryptor): 8 positive plants (G ix0 L5 KRYPTOS-keyed CA; G ix1 L4 KA Beaufort ACA-columnar
CA; G ix0 L8 random CA; G ix1 word primer KRYPTOS; G ix1 variant form, must appear as Beaufort; PG ix1 PALIMPSEST/aca; PG ix0
SHADOW/kmix Beaufort; G ix0 L5 primer 55555) and 1 negative (a forced collision under a crib, must be missed at its perm).
Independent recount: numpy brute force of G on a perm slice for K4 and 2 nulls, and replay of every reported fit.

## Budget
~6–7 min heavy compute, one 6-thread job at a time, own process group under `setsid timeout`.
