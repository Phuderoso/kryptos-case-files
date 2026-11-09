# Cycle 191 pre-registration — new family: compound key on two DIFFERENT tableaux (IDEAS I-190)

Written and pushed before any K4 or registered-null run. Timing only on the reserved shuffle seed 9191 (`random.Random(9191).shuffle(list(K4))`,
I-116) under **I-180** (81 routes = all.bin[::2048], `timeout 60`, the full registered pair set): `cmp191` with A–Z>KRYPTOS and KRYPTOS>A–Z ≈ 0.11 s;
one 64-pair direct chunk ≈ 0.16 s; one 64-pair themed chunk on 81 routes ≈ 1.0 s. Extrapolation: C1 (all 165,782 routes) ≈ 225 s; whole run ≈ 5–6 min.
**Chance meter checked before K4 (I-193):** 40 uniform random texts (seeds 19140–19179) on the 81 probe routes: solution totals per band
e = round(−log26 E_config) match E in every band (text-level z: −0.12, +0.56, −0.90, −1.90, −0.20 for e = 0–4; 0 fits and E ≤ 0.13 for e ≥ 5).
**Planted controls rehearsed before this push: 11/11** (`plant191.py` seed 19100, `run_controls191.sh`, `checkctl191.py`); the rehearsal is
declared the registered control run. Recount rehearsed on P1 (row 12345: 3,360 fits, identical sets and solution counts).
Binary: `cmp191` built from `tools/cycle191/cmp191.c` with `gcc -O3 -march=native -fopenmp -lm`. Heavy budget ≤ 8 min (≈ 15 s used before this push).

## Question (new family; checked against cases 119, 176, 177)
Case 176 tested two arbitrary periodic keys stacked on **one** tableau (additive, union-find). K1 and K2 were enciphered on the KRYPTOS tableau,
and Sanborn's sculpture shows both the plain A–Z alphabet and the KRYPTOS-keyed one. If the two passes sit on **different** tableaux (pass 1 on
T1 with key a, period m; pass 2 on T2 with key b, period n; the letter handed over as a letter), then with x = T1idx(p), z = T2idx(c) and
σ(y) = T2idx(T1[y]):  **z = s2·σ(s1·x + a[i mod m]) + b[i mod n]** (s1, s2 = ±1: Vig/variant +, Beau −). σ is not affine, so the combined
cipher is not a periodic key of period lcm(m, n) in any index space; case 176's exclusions do not cover it. Case 119 tried only **named**
keyword pairs; here the keys are arbitrary.

## Method (exact; new solver `cmp191.c`)
Each crib t is a bijection between a[u] and b[v] (u = pos mod m, v = pos mod n). On every connected component of the residue graph that
contains a cycle, all 26 values of one root are tried and propagated along a spanning tree, checking each non-tree edge (exact; no
approximation). Components without a cycle are always satisfiable. A config fits iff every cyclic component keeps ≥ 1 root value.
**Chance count (I-193):** with independent uniform carved letters, E_config = Π_cyclic 26^(1 − r_c) is the exact expected number of consistent
assignments (r_c = independent cycles of component c) and bounds the pass probability; printed per cell (H) and per band (B).
Ordered pairs (m, n), 2 ≤ m, n ≤ 26, m ≠ n (600); forms VV, VB, BV, BB; models **P** (key on the plaintext index) and **C** (carved index).

## Registered cells
- **C1** K4, T1>T2 ∈ {A–Z>KRYPTOS, KRYPTOS>A–Z}, **all 165,782 routes** (`all.bin`), P and C, 4 forms, 600 pairs.
- **Grid** K4 + 19 shuffles (seeds 19111–19129, `nulls191.txt`): the C1 tableau pairs on `all_s512.bin` (324 routes).
- **C3** K4, 572 tableau pairs (each of the 144 themed alphabets with A–Z and with KRYPTOS, both orders) on `all_s512.bin`.
- **C2t** K4 direct (identity route), 20,592 ordered pairs of distinct themed alphabets.
- **C2v** K4 direct, 75,292 pairs (each of the 18,824 vocabulary/themed keyed alphabets with A–Z and with KRYPTOS, both orders); lowest priority.
- **Recount** `recount191.py` (independent: literal letter-level two-pass tables, vectorised DFS) vs `cmp191` (all fits) on `slice191.bin`
  (all.bin rows 0, 40000, 80000, 120000, 160000, 12345, 100000), tab4 (C1 pairs + A–Z>A–Z, KRYPTOS>KRYPTOS), texts K4, P1, P2, P7, n19111:
  fit sets and solution counts must be identical.

## Labels
Cell = (model, tableau pair or tableau-pair list, form, m, n) over its routes. Cell E ≤ 0.05 = full power. K4 0 fits in a full-power cell →
**`EXACT-EXCL`** (that cell's scope). Any K4 fit in a full-power cell → decoded with `decode191.py` before any label; a solution needs a full
coherent English decryption with EASTNORTHEAST and BERLINCLOCK at the official positions, reproducible. Cells with E > 0.05 → **`LOW-POWER`**;
their totals are compared with E (meter) and with the shuffles (I-152 rank, p⁺ = (1 + #nulls ≥ K4)/20, floor 0.05, rank flag only; I-182).
Fits are printed only for E_config ≤ 0.002; if a full-power cell's H fit count exceeds its printed M lines, that cell is re-run with full
printing before labelling. A missing `END` = cell not run.

## Controls (`plant191.py`, seed 19100; passes applied literally letter by letter)
Positives: P1 A–Z>KRYPTOS P VV 7/11 (row 12345); P2 KRYPTOS>A–Z C Beau 5 + Vig 13 (row 100000); P3 A–Z>KRYPTOS C variant 8 + Beau 12
(row 18944); P4 KRYPTOS>A–Z P Vig 6 + Beau 19 (row 165781); P5 direct A–Z>KRYPTOS Vig PALIMPSEST then Vig ABSCISSA (10, 8); P6 direct
KRYPTOS>A–Z Beau KRYPTOS then Vig BERLINCLOCK (7, 11); **one-tableau plants (must also be found, I-190):** P7 A–Z>A–Z C variant 3 + Vig 25
(row 51712), P8 KRYPTOS>KRYPTOS P Beau 4 + Beau 9 (row 12345). Each must fit at its row, tableau pair, reduced form, model and (m, n), and the
decoder must reproduce the planted plaintext at every determined position. Fits at equivalent cells (period multiples, one-tableau form
equivalents, coincidences forced by the cribs' 36/42 offsets) are listed, not failures (I-195 handling). Negatives (no fit with
E_config ≤ 1e-4 at the planted row): N1 three passes (5, 7, 11; A–Z, KRYPTOS, A–Z); N2 random 97-letter key; N3 = P1 with one wrong carved
crib letter (slot 2).

## Not covered (stated now)
One error (strict test only); three or more passes; n or m > 26; vocabulary × vocabulary tableau pairs; vocabulary / themed pairs behind the
routes beyond all_s512 (themed) and direct (vocabulary); a transposition between the two passes.
