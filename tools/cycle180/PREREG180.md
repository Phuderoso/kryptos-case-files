# Cycle 180 pre-registration — linear-recurrence key mod 26 over keyed (Quagmire) alphabets behind K3's decimation law (IDEAS I-142)

Written and pushed before any K4 or registered-null run. Smoke / timing only on the reserved shuffle seed 9180
(`random.Random(9180).shuffle(list(K4))`, I-116), on `all_s8.bin`: every cell 0 fits. Cost (6 threads): M0 L 1–7 vocabulary 1.1 s
on 1/8 (≈ 9 s full); M1 L 1–2 0.9 s, L 3 1.6 s on 1/8; M1 L 4 themed 0.4 s on 1/8; M0 L 8 vocabulary 14 s on 1/8 (→ not run);
M1 L 4 vocabulary 6.3 s on 1/64 (≈ 400 s full → not run).
**Planted controls rehearsed before this push (I-119):** 14/14 on the first rehearsal (table below), no rule changed by it.
The numpy recount was rehearsed on the plant texts only (4/4 lines identical, counts included; it also caught a duplicated alphabet in the subset, now deduplicated, and a slow loop order, now c-outer).

## Question (new family behind the decimations; cycle 179 was an audit)
Cases 166–167 excluded the affine linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) behind the 165,782 K3-law
decimations / routes (`all.bin`, md5 946402ca…) only with the **A–Z or KRYPTOS** tableau. Kryptos K1–K2 use a keyed tableau
(Quagmire III, KRYPTOS alphabet); the natural next layer is the same tableau construction with **another English keyword**. Does any
linear-recurrence key over a **keyed alphabet** fit K4's 24 crib letters behind any decimation / route?

## Alphabets
`alpha172.txt` (cycle 172, `tools/cycle172/mkalpha172.py` on `data/cycle158/vocabulary_all.txt`, 10,056 words): every word keyed on
A–Z (K1/K2 construction, `/Z`) and on the KRYPTOS order (`/K`), plus A–Z and KA; **18,776 distinct alphabets** (md5 92793b74…).
Themed subset `alpha_themed180.txt`: the same construction on the 74 seed words of cycle 178 (`tools/cycle178/seeds178.txt`), 144
alphabets (used only for M1 L 4).
Tableau types (A = plaintext-side alphabet, B = ciphertext-side): **q1** A keyed / B = A–Z; **q2** A = A–Z / B keyed; **q3** A = B = keyed
(K1/K2 style). A–Z itself counted once. Vigenère c = B[(A(p) + k) mod 26], Beaufort c = B[(k − A(p)) mod 26]. Variant (= −Vig) and
any rotation of either alphabet (k → k + e, absorbed by d) map the affine family onto itself, so they are covered.
**56,326 (alphabet, type) pairs × 2 forms per perm.** Quagmire IV (two different keyed alphabets) is not tested.

## Models (exact, `lrk180.c`)
- **M0, ix 0 (key on the plaintext index, then transpose), L 1–7.** Same algebra as case 166 (`lr178` solve0): Z₂₆ = Z₂ × Z₁₃.
  New: the mod-2 test depends only on the 24 crib key bits, so it is precomputed as a 2²⁴ table (per L: some (c, d) mod 2 satisfies
  the in-block equations and propagates block 1 across the gap onto block 2); per perm the bits come from 24-bit letter masks and the
  alphabet's parity mask. Survivors go to the GF(13) solve0 per form. Seed upstream of 21 free (superset of every seed / offset).
- **M1, ix 1 (transpose first, key on the carved index, seed at carved 0…L−1), L 1–3 (vocabulary) and L 4 (themed).** Mod 2: the
  2^(2L+1) streams projected onto the 24 crib carved positions (pext) in a per-thread 2²⁴ bitset; one lookup per (alphabet, type).
  Survivors: lr178's GF(13) loop over c mod 13 (seed, d linear).
- **Analytic chance rate** per (perm, pair, form) ≈ 26^(2L+1−24); configs per full set 1.87 × 10¹⁰: M0 L 6 ≈ 5 × 10⁻⁶, **L 7 ≈ 0.003**
  fits per text; M1 L ≤ 4 < 10⁻⁷. So every registered cell has full power. **Not run (declared now):** M0 L 8 (≈ 2.3 chance fits per
  full set → `LOW-POWER` by construction, and 14 s per 1/8 pass), M1 L 4 with all 18,776 alphabets (≈ 400 s per text), M1 L ≥ 5,
  Quagmire IV, one-error versions, alphabets outside the list (N4 below shows the test is alphabet-specific).

## Texts and runs (`run_cycle180.sh`)
K4 (`data/k4.txt`, md5 dc4df49d…): M0 L 1–7 and M1 L 1–3 on the **full** set, M1 L 4 themed full, plus both on `all_s8.bin`.
19 nulls = `random.Random(s).shuffle(list(K4))`, s = **18011…18029** (`nulls180.txt`): M0 L 1–7 and M1 L 1–3 on `all_s8.bin`
(md5 3dd34d3c…, = all.bin[::8]); M1 L 4 themed on the full set.

## Labels (per cell)
K4 0 fits → `EXACT-EXCL` (scope: these alphabets, types, forms, orders, L); K4 > 0 inside the null range → `LOW-POWER`, every fit
decoded; above every null → flagged and decoded, never a signal without a readable decode. Solution criterion: a full coherent
English decryption of the 97 letters with both cribs at the official positions, reproducible.
Any `X` line (table vs solve0 mod-2 disagreement) or overflow is reported and invalidates the affected cell.

## Decodes
Every K4 fit and every fit of the first 5 nulls replayed at string level (`decode180.py`, independent of the C code: rebuilds the
tableau from the alphabet string). Score = mean log10 quadgram (support/quadgrams.json, floor) over off-crib windows.

## Grid (I-120 rule)
Scored cells: R1 M0 L 1–7 fits (1/8); R2 M1 L 1–3 fits (1/8); R3 M1 L 4 themed fits (full). Diagnostics: D1 M0 mod-2 passes L 6–7
(1/8); D2 M1 mod-2 passes L 1–3 (1/8) + L 4 themed. Leave-one-out exact Poisson tails, all-zero cells reported and not scored;
G± = min over scored cells; grid p = fraction of the 20 texts with G ≤ G(K4); both tails.

## Controls (`plant180.py`, seed 18000, independent string-level encryptor; plaintext THEIRONDOORFACEDDUEXX·EASTNORTHEAST·…·
BERLINCLOCK·STRUCKTHEHOURATMIDNIGHT; each plant behind a perm q of all.bin, run on q ± 1,500; `run_controls180.sh`, `checkctl180.py`)
Positives (found at q with the planted alphabet/type/form/L, planted (c, d) mod 2 / mod 13 listed, replay = planted plaintext):
P1 M0 L3 q3 Vig SHADOW/Z; P2 M0 L5 q1 Beau BERLIN/K; P3 M0 L7 q2 Vig ABSCISSA/Z; P4 M0 L2 q3 Beau SHADOW/K; P5 M0 L6 q3 Vig
PALIMPSEST/K with even last weight; P6 M1 L1 q3 Vig COMPASS/Z; P7 M1 L2 q1 Beau LODESTONE/K; P8 M1 L3 q2 Vig MAGNETIC/Z; P9 M1 L4
q3 Beau ABSCISSA/K (themed run); P10 M0 progressive key (c = 1, d = 3) q3 Vig KA.
Negatives (no fit at q, any alphabet / type / form / L): N1 = P1 with one wrong carved letter at slot 30 (inside every block-1
equation window for L ≤ 9, the cycle-178 N1 lesson); N2 random key M0; N3 random key M1; N4 M0 L3 q3 plant with a random alphabet
**not** in the list.
Rehearsal (before this push): **14/14** (10 positives with full or crib-anchored replay, 4 negatives missed).
**Independent recount** (`recount180.py`, numpy brute force, no CRT / table / pext / elimination): slice = all.bin[::4000] + the planted
perms of P1, P4, P6, P7 (46 rows, `mkslice180.py`); alphabets = first 30 of alpha172 + SHADOW/K, COMPASS/Z, LODESTONE/K (`alpha_recount180.txt`, 33; SHADOW/Z is already among the 30);
texts K4, n18011, n18012, P1, P4, P6, P7; M0 L 1–2 (L 3 for P1), M1 L 1 (L 2 for P7 at its planted row) over every (c, d) / stream
mod 26; one process per text, niced. Compared line by line with lrk180 on the same slice and alphabets, including the mod-26 solution counts (`cmprecount180.py`).

## Budget
≈ 3–4 min heavy, one 6-thread job at a time under `setsid timeout 900`; resumable. Recount single core, niced, outside the budget.
