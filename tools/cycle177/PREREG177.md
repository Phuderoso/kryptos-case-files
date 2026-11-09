# Cycle 177 pre-registration — one-error Gromark behind K3's decimation law (IDEAS I-128) + bases 5–9 (I-129)

Written and pushed before any K4 or registered-null run. Smoke and timing runs used only the reserved shuffle seed 9177 (I-116);
the err-0/base-10 path of `gm177` was regression-checked against cycle 176's stored output for n17611 (identical M lines).

## Question (audit of case 164)
Case 164 called ordinary Gromark (any cipher alphabet, L 2–5 both layer orders, 22,121 named primers) and ACA Periodic Gromark
(17,164 keywords) `EXACT-EXCL` behind the 165,782 K3-law decimations / routes (`all.bin`). Those were strict tests. Does any of
them fit K4 if ONE of the 24 crib slots is wrong (one wrong carved letter or one wrong crib letter)? And does ordinary Gromark with
digit base 5–9 fit strictly? Cribs EASTNORTHEAST at 21–33, BERLINCLOCK at 63–73 (0-indexed).

## Models (exact)
- **G1 (one-error ordinary Gromark), `gm177.c`, err 1, base 10.** Same model as gm176 (arbitrary cipher alphabet, PA A–Z/KRYPTOS,
  Vig/Beau; variant = Beau). A config fits with one error iff some slot t exists such that the equal-letter ⇔ equal-w condition
  holds on the other 23 slots. Wrong carved letter and wrong crib letter are the same event under an arbitrary alphabet (slot t
  becomes free; a consistent true letter always exists). The run reports the drop mask (all slots t that repair the fit); a full
  mask = strict fit. Counted statistic: **one-error-only fits** (mask ≠ full), per L.
  - ix 0 (Gromark on the plaintext index, then transpose): every primer, **L 2–6**, full perm set (hash join, 24 keys per perm).
  - ix 1 (transpose first, carved index): every primer, **L 2–5**; K4 on the full set AND on `all_s8.bin` (every 8th perm);
    nulls on `all_s8.bin`.
  - Named primers (cycle 176's 22,121, `primers176.txt`): ix 0 full (K4 and nulls), ix 1 K4 full + s8, nulls s8.
- **PG1 (one-error ACA Periodic Gromark), `pg177.c`.** cycle 176's 137,312 configs (`cfg176.txt`), fixed alphabets, ≥ 23/24
  exact predictions; both ix, full perm set, K4 and nulls.
- **GB (strict ordinary Gromark, base b = 5…9), `gm177.c` err 0.** Digits mod b, primers b^L. ix 0 **L 2–7** full; ix 1
  **L 2–4** (K4 full + s8; nulls s8). Not run: base < 10 one-error, ix 1 L 5 for bases, L 8.

## Texts
K4 (`data/k4.txt`, md5 dc4df49d…). 19 nulls = K4 shuffled with `random.Random(s)`, s = 17711…17729 (`nulls177.txt`).

## Labels (per model × ix × L cell, one-error-only counts for G1/PG1, strict for GB)
- K4 0 → `EXACT-EXCL` (under the stated model, one error allowed), null mean quoted as the power statement; a cell whose null
  mean is < 1 gives a weak exclusion and is labelled `EXACT-EXCL (weak power)`.
- K4 > 0 inside the null range → `LOW-POWER`; decodes (below) → `NO-SIGNAL` if K4's best is inside the null decodes' range and far
  below the plants.
- K4 above every null in a cell → flagged and decoded, not called a signal without a readable decode.
- Solution criterion: a full 97-letter coherent English decryption with both cribs (up to the one error) in place, reproducible.

## Decodes
Every K4 one-error/GB fit in: G1 ix 0 L ≤ 5, G1 ix 1 (all, full set), named primers (all), PG1 (all), GB ix 0 L ≤ 6 and GB ix 1
(all) is replayed at string level (independent of the C code) and decoded with cycle 176's procedure (free cipher-alphabet
letters by a seeded quadgram hill-climb, 3 × 2,500 swaps; for G1 each slot in the drop mask is tried as the wrong one and the
best kept). The same cells are decoded for the first 5 nulls (n17711–n17715) and for the plants. Score printed against the number
of fixed alphabet letters (I-131).

## Grid (I-120 rule, unchanged)
Cells: C1 G1 ix0 L 2–5 (sum), C2 G1 ix0 L 6, C3 G1 ix1 L 2–5 (s8), C4 named primers G1 ix0 (full) + ix1 (s8), C5 PG1 both ix,
C6 GB ix0 L 2–7 + ix1 L 2–4 (s8). Per cell, exact Poisson tails of each text's count against the mean of the other 19
(leave-one-out); all-zero cells reported, not scored. G± = min over scored cells; grid p = fraction of the 20 texts with
G ≤ G(K4). Best attainable 0.05. Reported both tails.

## Controls
`plant177.py` (independent string-level encryptor; one-error plants made by overwriting a carved letter with the carved letter of a
slot with a different w, or by encrypting a plaintext with one crib letter changed so that the strict test fails at the planted
config — both checked in Python): G1 ix0 L4 wrong carved letter; G1 ix1 L4 wrong crib letter; G1 ix0 L5 random CA wrong carved
letter in BERLINCLOCK; G1 ix1 named primer (KRYPTOS ranks) wrong carved letter; G1 ix1 L5 variant wrong crib letter; PG1 ix1 miss
at crib slot 0 (second-bucket path); PG1 ix0 wrong crib letter; PG1 ix1 miss at slot 17; GB base 7 ix0 L6; GB base 5 ix1 L4
Beaufort; strict G plant must appear with a full mask in the err-1 run. Negatives: G two wrong letters in disjoint violated pairs
and PG two misses must be missed at their planted configs. Every planted case also checks that the strict run misses it (the
error is visible). All plants sit behind a transposition (perm q of all.bin).
Independent recount: numpy brute force of G1 (both ix, L 2–4) and GB (base 7, L 2–4) on a 46-perm slice (all.bin[::4000] +
planted perms) for K4 and 2 nulls; numpy PG1 (both ix) on the same slice; line-by-line comparison with gm177/pg177.

## Budget
~8 min heavy, one 6-thread job at a time, own process group under `setsid timeout`. Resumable (jobs ending in END are skipped).
