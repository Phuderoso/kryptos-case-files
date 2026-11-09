# Cycle 174 pre-registration (IDEAS I-108, with the I-110 grid rule)

Written and pushed **before** any K4 or null run of the families below (one disclosed exception at the end).
Date: 2026-11-09, ~05:21 PT.

## Families (new behind K3's law; case 57's last three names)
Behind each of the 165,782 K3-law decimations / spiral-diagonal routes of `all.bin` (cycle 168; perm and inverse both entries).
Convention as `tools/cycle172/q4d172.c`: plaintext index i ↔ carved index S[i]; ix 0 = substitute on plaintext order, then transpose;
ix 1 = transpose first, substitute on carved order.

1. **Hill n = 2 and n = 3** (`hill174.c`), decryption form P = D·Z (linear) and P = D·Z + e (affine; covers A=1 and any cyclic
   numbering shift), numbering A–Z and KRYPTOS (KA), block offset 0..n−1, both orders. Exact: each crib letter is one linear equation
   on one row of D, solvable mod 2 and mod 13. Consistent configs are then checked for an invertible D and decoded.
2. **Ragbaby, classic** (`rag174.c`), step d = 1, both directions, any word division (word in progress at a crib start ≤ 20 letters),
   ix 0 only (Ragbaby on the plaintext, whose word structure it needs), on the 18,776 alphabets of `alpha172.txt`
   (vocabulary words keyed on A–Z and on the KRYPTOS order, plus A–Z and KA). Exact on the 24 crib letters (case 53 test).
3. **Portax** (`portax174.c`, core from `tools/portax.c`), any key of period p = 1..48, numbering A–Z and KA, both orders. Exact.

## Texts
- K4 (97 letters, as `data/k4.txt`) on the full 165,782 perms (the exact verdict).
- 19 shuffled nulls (Python `random.Random(seed).shuffle` of K4's letters, seeds 174000–174018) on every 4th perm (`all_s4.bin`,
  41,446 perms); K4 is also run on `all_s4.bin` so that the grid compares like with like.

## Grid (I-110: few cells, a standardised score that cannot sit at a floor for most texts)
Four cells, fixed now (≤ N/4 with N = 19 nulls):

| cell | statistic per text (on `all_s4.bin`) |
|---|---|
| C1 Hill n 2 | number of crib-consistent configs, summed over linear/affine × A–Z/KA × ix × offset |
| C2 Hill n 3 | same for n = 3 |
| C3 Ragbaby | number of (perm, alphabet, direction) with both cribs fitting |
| C4 Portax | number of crib-consistent (perm, numbering, ix, p) configs, p 1–48 |

Per cell, a text's score is a leave-one-out z: z = (x − mean of the other 19 texts) / sd of the other 19 (sd = 0: z = 0 if x equals
the mean, +∞ if above). Grid statistic G = max over the 4 cells of z. **Grid p = (1 + #{nulls with G ≥ G_K4}) / 20.** Best attainable
p = 0.05. With all-zero cells every z is 0 and G ties at 0; then the grid p is 1.00 and carries no information (stated as such).
No single cell's rank is quoted as evidence.

## Verdict rules
- Per family/sub-cell, K4 count 0 on the full family with planted controls recovered → `EXACT-EXCL` (under the stated alphabets,
  numberings, periods and perms). For Hill, the analytic chance expectation is printed beside each sub-cell.
- K4 count > 0: decode (Hill, Portax), mean log10 quadgram per letter on all non-crib letters vs the nulls' decodes and the plants
  (a real English plant reads about −4); counts at null level and gibberish → `NO-SIGNAL` (exact count indistinguishable from
  chance → `LOW-POWER` for that sub-cell). No claim from fewer than the 19 nulls.
- A solution claim needs a readable decode outside the cribs AND a count/score beyond every null.

## Controls
Independent Python encryptor (`plant174.py`, string tables, no code shared with the C tools): Hill (n 2/3, linear/affine,
both numberings, both orders, offsets), Ragbaby (explicit words, both directions), Portax (table built from row strings),
each hidden in a 200-perm slice; one Hill and one Portax negative plant (one carved crib letter altered: strict test must miss).
Independent recount (`recount174.py`): brute force in Python (Hill n 2: all 676 row vectors / 17,576 affine rows; Portax: all 13
slides per column; Ragbaby: explicit enumeration of word divisions) on sampled configs and on all hits, compared per config.

## Disclosure
While writing `hill174.c` a 2,000-perm smoke run was made on K4 (perms 0–1,999) before this file was written; it printed only
per-cell totals (0 consistent configs in every sub-cell). Ragbaby and Portax smoke runs used a shuffled text with seed 9174, not
K4 and not a registered null. Nothing about the grid above was changed after that run.

## Budget
≈ 8 min of heavy computation; chunks with an `END` line are skipped on rerun (resumable).
