# Cycle 189 pre-registration — new family: a compound key (two arbitrary periodic keys of periods m and n stacked on one tableau) behind K3's decimation law (IDEAS I-189), with the I-184 add-on

Written and pushed before any K4 or registered-null run. Timing only on the reserved shuffle seed 9189 (`random.Random(9189).shuffle(list(K4))`,
I-116) under **I-180** (81 routes, `timeout 60`, the only order there is): `cmp189` on `all_s2048.bin` with A–Z/KRYPTOS ≈ 0.04 s, with the 144
themed alphabets ≈ 2.5 s; direct with 18,824 alphabets ≈ 0.3 s (2.9 s for the three probes). Extrapolation: C1 (full set, A–Z/KRYPTOS) ≈ 80 s.
**Planted controls rehearsed before this push: 10/10** (`plant189.py` seed 18900, `run_controls189.sh`, `checkctl189.py`); the rehearsal is declared
the registered control run. **I-184 alignment controls rehearsed: 4/4** (`i184plant189.py`, seed 18950). Recount rehearsed on planted P1 (1 row:
717 fits, identical sets). Binaries: `cmp189` built from `tools/cycle189/cmp189.c` with `gcc -O3 -march=native -fopenmp`; `lrk186` = cycle-187 binary
(md5 4f41a243…). **Heavy budget:** ≤ 8 min including controls and probes (≈ 20 s spent before this push).

## Question (new family; checked against cases 12, 14, 52, 119, 134, 154, 155)
K1 and K2 each used one keyword on one tableau. If Sanborn ran K4 through **two** keyword passes on the **same** tableau (any mix of Vigenère,
Beaufort and variant steps), the combined key is K[i] = a[i mod m] + b[i mod n] (mod 26, in the tableau's index space; signs are absorbed by
a and b) and the cipher is c = p + K or c = K − p. That key has period lcm(m, n) (e.g. 77 for 7 and 11), far beyond the periodic exclusions
(p ≤ 26 direct, ≤ 20 behind transpositions), but it has only m + n − 1 free values, so the cribs can still test it. Case 119 tested only
**named** word pairs; case 14's long periods are LOW-POWER. Here the two keys are **arbitrary** (every keyword pair of those lengths at once).

## Method (exact; new solver `cmp189.c`)
For each route, alphabet T (same keyed alphabet on both sides: A–Z, KRYPTOS, or a Quagmire III keyed alphabet), form (vig: K = c − p,
beau: K = c + p in T's index space) and model (**P**: key on the plaintext index, i.e. substitute then transpose; **C**: key on the carved index,
transpose then substitute), the 24 crib equations a[u] − b′[v] = K_t (u = pos mod m, v = pos mod n, b′ = −b) are checked with a weighted
union-find over Z26 (exact, no division). excess = 24 − merging edges = number of independent checks; chance pass ≈ 26^−excess, summed per cell
as the expected chance count E (printed in every `H` line). Pairs: m 2–25, n m+1–26, m ∤ n (260 pairs).

## Registered cells
- **C1** K4, A–Z and KRYPTOS, **all 165,782 routes** (`all.bin`), models P and C, vig/beau, 260 pairs.
- **C2** K4, direct (identity), **18,824 keyed alphabets** (vocabulary 18,776 + 48 themed not in it; `alpha_direct189.txt`), vig/beau (P = C here).
- **C3** K4, 144 themed alphabets, `all_s512.bin` (324 routes), models P and C, vig/beau.
- **Grid** K4 + 19 nulls (seeds 18911–18929, `nulls189.txt`): A–Z/KRYPTOS on all_s512 and C2's direct cell, printing fits with excess ≥ 3.
- **Recount** `recount189.py` (independent: left null spaces of the design matrix mod 2 and mod 13 by numpy elimination) vs `cmp189` (PE 0) on
  `slice189.bin` (all.bin[::4000] + rows 12345, 100000, 51712; 45 rows), A–Z/KRYPTOS, texts K4, P1, P2, P7, n18911: fit sets must be identical.
- **Add-on (I-184)** case 174 direction r, strict, L 1–3, `lrk186` on classes all.bin[6::8] and all.bin[7::8], each under `timeout 60`.

## Labels
Per cell (pair × model × form, over its routes and alphabets): K4 0 fits → **`EXACT-EXCL`** (that pair, model, form, alphabet list, route set).
K4 fits in a cell with E > 0.05 → **`LOW-POWER`** (fits expected by chance; the cell cannot tell K4 from shuffled text); fits are counted against the
nulls (I-152 empirical rank, p⁺ = (1 + #nulls ≥ K4)/20, floor 0.05, rank flag only, second batch under I-182). K4 fits in a cell with E ≤ 0.05
→ every fit decoded with `decode189.py`; a solution needs a full coherent English decryption with the cribs at the official positions,
reproducible. A missing `END` = cell not run.

## Controls (`plant189.py`, seed 18900; layers applied literally letter by letter)
Positives: P1 A–Z, P, Vig 7 + Vig 11 at q 12345; P2 KRYPTOS, C, Beau 5 + Beau 13 at q 100000; P3 PALIMPSEST/Z, C, Vig 8 + variant 12 at q 18944;
P4 KRYPTOS, P, Vig 6 + Beau 19 at q 165781; P5 direct A–Z, P, Vig PALIMPSEST then Vig ABSCISSA (8, 10); P6 direct KRYPTOS, C, Beau KRYPTOS then Vig
BERLINCLOCK (7, 11); P7 A–Z, C, variant 3 + Vig 25 at q 51712. Each must be reported at its route with its alphabet, reduced form (odd number of
Beaufort steps → beau) and model. Negatives (no fit with excess ≥ 5 at the planted route): N1 three stacked periods 5, 7, 11; N2 random key;
N3 = P1 with one wrong carved crib letter.
I-184 alignment: plants A6 (class 6, local row 1000) and A7 (class 7, local row 15000) must be found at their local rows in their own class file
and not in the other class file.

## Not covered (stated now)
Two different tableaux for the two layers (not additive; open); three or more layers; one-error audit (next audit slot); vocabulary alphabets
behind the routes; pairs with n > 26.
