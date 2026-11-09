# Cycle 190 pre-registration — audit: one-error version of case 176 (compound key, two periodic keys on one tableau) (IDEAS I-191)

Written and pushed before any K4 or registered-null run. Timing only on the reserved shuffle seed 9190 (`random.Random(9190).shuffle(list(K4))`,
I-116) under **I-180** (81 routes, `timeout 60`; one order only): `cmp190` on `all_s2048.bin` with A–Z/KRYPTOS ≈ 0.16 s, with the 144 themed
alphabets ≈ 5.2 s (before the chunk-size fix), direct with 18,824 alphabets ≈ 9.9 s (single route, one thread). Extrapolation: C1 ≈ 80–100 s.
**Meter check before any K4 (I-193; brute-force fixture as the Voynich desk offered in its K059 journal):** 40 uniform random texts (seeds
19091–19130) on all_s2048, A–Z/KRYPTOS: observed one-error fits vs the analytic chance count per band of per-config probability:
p < 10⁻³ 64 vs 65.3; p < 10⁻² 1,706 vs 1,735.6; p < 0.1 14,744 vs 14,702.1; p < 0.5 231,929 vs 232,086.2; p ≥ 0.5 2,721,179 vs 2,721,192.2
(all |z| < 0.8). **Planted controls rehearsed before this push: 11/11** (declared the registered control run). Recount rehearsed on planted E1
(row 12345, 875 fits, identical sets). Heavy budget ≤ 8 min including probes and controls (≈ 30 s spent before this push).

## Question
Case 176 excluded a compound key K[i] = a[i mod m] + b[i mod n] (two keyword passes on one tableau) on every full-power pair, but only with all 24
crib letters exactly right. One wrong carved letter (Sanborn's known K1–K3 slips) or one wrong crib letter breaks every strict test. Does K4 fit
the same family with **at most one** wrong crib slot?

## Method (exact; `cmp190.c`)
Same model as case 176 (alphabet T both sides; vig K = c − p, beau K = c + p in T's index space; model P key on the plaintext index, model C on the
carved index; pairs m 2–25 < n ≤ 26, m ∤ n, 260 pairs). A config fits if the 24 equations a[u] − b′[v] = K_t are consistent after deleting at
most one slot t (weighted union-find mod 26; only t ≤ the first inconsistent edge can help). **Chance (exact):** P = 26^−ex + ncls·(26^(1−ex) −
26^−ex), ex = strict excess, ncls = number of series classes of non-bridge edges (XOR cycle hashing): the events "G − t consistent" coincide
inside a series class and are disjoint across classes. Summed per cell as E. Full power: E ≤ 0.05.

## Registered cells
- **C1** K4, A–Z and KRYPTOS, all 165,782 routes, P and C, vig/beau.  **C2** K4 direct, 18,824 keyed alphabets.  **C3** K4, 144 themed alphabets,
  all_s512 (324 routes), P and C.
- **Grid** K4 + 19 nulls (seeds 19011–19029, `nulls190.txt`), A–Z/KRYPTOS on all_s512 and direct with 18,824 alphabets; statistics: fits in
  full-power cells, fits with ex_after ≥ 3, all fits. I-152 empirical rank, p⁺ = (1 + #nulls ≥ K4)/20, rank flag only (I-182 second batch).
- **Recount** `recount190.py` (left null spaces mod 2 / mod 13 by numpy, every one-row deletion; no union-find) vs `cmp190` PE 0 on `slice190.bin`
  (all.bin rows 0, 80000, 12345, 100000, 51712), A–Z/KRYPTOS, texts K4, E1, E2, E6, n19011: fit sets must be identical.

## Labels
Per cell (pair × model × form, over its routes and alphabets), one-error scope. K4 0 fits and E ≤ 0.05 → **`EXACT-EXCL`** (one-error). Fits
with E > 0.05 → **`LOW-POWER`**, counted against the nulls. Fits in a cell with E ≤ 0.05 → decoded with `decode190.py … all` (every consistent
deletion); a solution needs a full coherent English decryption with the cribs at the official positions (one of them corrected), reproducible.
Missing `END` = cell not run.

## Controls (`plant190.py` on the cycle-189 literal two-pass plants, seed 18900; rule in `checkctl190.py`)
Positives: E1 = P1 (A–Z, P, Vig 7 + 11, q 12345) + error slot 5; E2 = P2 (KRYPTOS, C, Beau 5 + 13, q 100000) + slot 17; E3 = P5 (direct A–Z,
PALIMPSEST then ABSCISSA) + slot 0; E4 = P6 (direct KRYPTOS, carved, KRYPTOS then BERLINCLOCK) + slot 23; E5 = P4 (KRYPTOS, P, 6 + 19,
q 165781) + slot 12; E6 = P7 (A–Z, C, 3 + 25, q 51712) + slot 9; S1 = P3 with no error. Each must be found at its route, alphabet, reduced form,
model and pair, at the planted slot or a slot in series with it (or −1 if the slot is a bridge). Negatives (no fit at the planted route with
ex_after ≥ 5): D1 = P1 + errors at slots 5 and 10 (+7, +11); D2 = P6 + slots 2 and 15; N1 three periods; N2 random key.
**Rehearsal disclosures (before any K4):** (1) E1 was first reported at slot 4, which is in series with 5 (deleting any member of a series class
gives the same consistent system); the checker now accepts the series class, computed independently by connectivity. (2) D1 first had errors at
slots 5 and 20 with equal shifts: they lie in one series class, so the text is a one-error text by construction (equal shifts on two edges in
series also cancel on every cycle); D1 moved to slots 5 and 10 with shifts +7 and +11.

## Not covered (stated now)
Two different tableaux (I-190); two or more errors; dropped/inserted letters (positions shift); vocabulary alphabets behind the routes; n > 26.
