# Case file 177 — One wrong letter: the compound key of case 176 under a single carving or crib error (cycle 190)

**Status:** negative. **Type:** audit (189 was a new family). IDEAS [I-191](../IDEAS.md) (via pointer I-192), part of I-003.
Pre-registered in [`tools/cycle190/PREREG190.md`](../tools/cycle190/PREREG190.md) (commits a1bb21b, c0f8acc, ~15:26 PT) with the plants,
decoder, checker, recount, run script and null seeds, **after** the planted controls had been rehearsed (11/11, two rule fixes disclosed) and
the solver timed under rule I-180 on the reserved shuffle (seed 9190, I-116), before any K4 or registered-null run.
New solver: [`cmp190.c`](../tools/cycle190/cmp190.c).

**Result in one line:** if K4 were enciphered with **two arbitrary periodic keys of lengths m and n stacked on one tableau** (case 176's family,
K[i] = a[i mod m] + b[i mod n], any Vig/Beau/variant stack) **and one of the 24 crib letters were wrong on the copper (or in the crib)**, the
fit would show up in the one-error test. **On all 165,782 K3-law decimations/routes with A–Z or KRYPTOS, every pair that keeps full power under
one error (63 per form on the plaintext index, 46 on the carved index; 47 / 30 of them with lcm > 26, up to 105 / 77; incl. 8 × 10 and 7 × 11)
has 0 one-error fits → `EXACT-EXCL` (one-error scope).** Direct with 18,824 keyed alphabets: 70 full-power pairs, 0 fits. 144 themed alphabets on
every 512th route: one fit in a cell at the threshold (E 0.049), decoded with every consistent deletion: gibberish, rejected. All other cells are
**`LOW-POWER`**, and their fit counts match the exact chance count (C1: 152,530,845 vs 152,531,362). Controls 11/11; 19 shuffles at chance;
recount identical (23,526 fits). **No solution.**

## 1. Why this
Sanborn's own text has slips: K1's IQLUSION, K2's UNDERGRUUND and the S he later said he left off the copper (IDBYROWS → X LAYER TWO), K3's DESPARATLY. Case 176's test needs
all 24 crib equations exact, so a single wrong letter on the copper inside a crib would hide a true compound key. This is the standing one-error
audit (I-003) for case 176.

## 2. Method (exact)
Same model as case 176: alphabet T on both sides, vig K = T(c) − T(p) or beau K = T(c) + T(p); model **P** (key on the plaintext index) or **C**
(key on the carved index); pairs m 2–25 < n ≤ 26, m ∤ n (260). A config fits under one error if the 24 equations a[u] − b′[v] = K_t are consistent
after deleting **at most one** slot t. The strict union-find stops at the first inconsistent edge t_f; only a deletion t ≤ t_f can help, and each
is tried from the shared prefix state. **Exact chance count:** with ex = strict excess and ncls = the number of *series classes* of non-bridge
edges (edges that lie on exactly the same cycles; found by XOR cycle hashing with 64-bit labels), P(one-error fit) = 26^−ex + ncls·(26^(1−ex) −
26^−ex): deleting any member of a series class gives the same consistent system, and the events for different classes are disjoint (the cycle
matroid is regular, so this holds mod 2 and mod 13 alike). Full power: cell E ≤ 0.05. **Meter check before K4** (I-193; the brute-force fixture
the Voynich desk offered in its K059 journal): on 40 uniform random texts the observed fits matched E in every probability band (|z| ≤ 0.71;
[`runlog190.txt`](../data/cycle190/runlog190.txt)).

## 3. Results ([`summary190.txt`](../data/cycle190/summary190.txt), [`c1_k4_full.txt`](../data/cycle190/c1_k4_full.txt), [`runlog190.txt`](../data/cycle190/runlog190.txt))
| cell | routes × alphabets | configs | full-power cells, one error (fits) | low-power cells: fits vs chance E |
|---|---|---|---|---|
| **C1** A–Z, KRYPTOS; P and C; vig/beau | 165,782 × 2 | 3.45 × 10⁸ | P 63 + 63, C 46 + 46 (**0**) | 152,530,845 vs 152,531,362 |
| **C2** direct; 18,824 keyed alphabets | 1 × 18,824 | 1.96 × 10⁷ | 70 per model and form (**0**) | 10,598,838 vs 10,599,896 |
| **C3** 144 themed; P and C | 324 (all_s512) × 144 | 4.85 × 10⁷ | P 70 + 70, C 53 + 53 (**1**, beau P 9 × 10) | 21,428,961 vs 21,429,845 |

- **The C3 fit** (all_s512 row 188, SHADOWFORCES/K, Beau, plaintext index, 9 × 10; cell E 0.049, and C3's full-power cells together expect 0.76
  chance fits) decodes all 97 letters under both consistent deletions: `ITETFBAXXRQOBIJJQNCXX EASTNOCTHEAST XYJSIJMSURK…` (slot 6, R → C) and
  `…EASTNORTHEAST XYJZIJMSURKXMQKDZJVVVBBIHOFBX BERLGNCLOCK…` (slot 17, I → G). No English outside the cribs: rejected.
- **The case-176 chance fit** (route 46579, 7 × 13, carved, Vig) sits in a cell that is LOW-POWER under one error; it is not a new finding.
- **Full-power pairs under one error** (exact lists in `summary190.txt`): plaintext index, m ≤ 9 with most n up to 15–23 plus 12 × 18 and 14 × 21
  (lcm up to 105, e.g. 5 × 21); carved index, m ≤ 8 with n up to 10–17 (lcm up to 77, 7 × 11). Both lists contain **8 × 10** (ABSCISSA,
  PALIMPSEST lengths) and **7 × 11** (KRYPTOS, BERLINCLOCK lengths). One error costs case 176 27 plaintext-index and 13 carved-index pairs.
- **Scope:** `EXACT-EXCL` (one error in any one crib slot, or none) for the full-power cells above, with the stated alphabets, both forms, both
  key indexings and the stated route sets. `LOW-POWER` elsewhere. Not covered: two or more wrong letters, dropped or inserted letters (they shift
  positions), two different tableaux.

## 4. Grid ([`grid190.txt`](../data/cycle190/grid190.txt); I-152 empirical rank, 19 nulls, seeds 19011–19029)
| statistic | K4 | nulls (min–max, mean ± SD) | p⁺ / p⁻ |
|---|---|---|---|
| all_s512, A–Z/KRYPTOS: fits in full-power cells | 2 | 0–4, 0.9 ± 0.9 | 0.15 / 0.95 |
| all_s512: fits with ex_after ≥ 3 | 14 | 8–25, 13.8 ± 4.3 | 0.50 / 0.60 |
| all_s512: all fits | 297,653 | 297,483–297,811, 297,651.3 ± 74.2 | 0.40 / 0.65 |
| direct, 18,824 alphabets: fits in full-power cells | 0 | 0–4, 0.5 ± 1.1 | 1.00 / 0.80 |
| direct: fits with ex_after ≥ 3 | 282 | 210–366, 279.1 ± 39.1 | 0.50 / 0.55 |
| direct: all fits | 10,598,838 | 10,598,360–10,601,716, 10,600,012.6 ± 935.8 | 0.90 / 0.15 |

K4 sits inside the shuffles everywhere; no rank flag. The two all_s512 full-power fits (KRYPTOS, Vig, plaintext index, 4 × 23, rows 43 and 94)
are in a cell that has full power only on 324 routes; on all routes it is LOW-POWER (C1: 9 fits vs E 4.91). Their decodes fill 34 letters
(`MOZZ EASTNORTHEAST`, `FOUL EASTNORTHEAST … BERLINCLOCK ZWIUGG`): noise around the cribs.

## 5. Controls ([`runlog190.txt`](../data/cycle190/runlog190.txt), [`texts190.txt`](../data/cycle190/texts190.txt))
Plants: case 176's literal two-pass texts (`plant189.py`, seed 18900, regenerated byte for byte) with errors injected by `plant190.py`.
E1 P1 + slot 5; E2 P2 + slot 17; E3 P5 (PALIMPSEST then ABSCISSA, direct) + slot 0; E4 P6 (KRYPTOS then BERLINCLOCK, direct, carved) + slot 23;
E5 P4 + slot 12; E6 P7 + slot 9; S1 P3 with no error: **all 7 found** at their route, alphabet, reduced form, model and pair, at the planted slot
or a slot in its series class (E3 and E6: the planted slot is a bridge, so the strict pass already fits). Negatives with no fit at ex_after ≥ 5
at the planted route: D1 P1 + two errors in different series classes, D2 P6 + two errors, N1 three periods, N2 random key. **11/11.**
`decode190.py` on E1 with every consistent deletion returns the planted plaintext at slot 5 (`…EASTNVRTHEAST…`, the injected error) and noise at
the other members of its series class.
**Rehearsal disclosures (before any K4):** E1 was first reported at slot 4, in series with 5; the checker now accepts the series class. D1 first
put two equal-shift errors in one series class, which is a one-error text by construction; it was moved to two classes with unequal shifts.
Recount: `recount190.py` (left null spaces mod 2 and mod 13 by numpy, every one-row deletion, no union-find) on 5 rows × 2 alphabets × 260 pairs ×
2 models × 2 forms for K4, E1, E2, E6 and n19011: **23,526 fits, identical sets**, planted fits present.

## 6. Limits
- Two or more wrong crib letters; dropped or extra letters (positions shift; the slip machinery of case 175 would be needed).
- **Two different tableaux** (I-190), three or more passes, n > 26, vocabulary alphabets behind the routes.
- Pairs that lose power under one error (27 plaintext-index and 13 carved-index pairs that case 176 could exclude strictly) are only strict-excluded.
- Budget: probes ≈ 40 s, meter check 2 s, controls ≈ 5 s, recount rehearsal 7 s, registered run 150 s (C1 59 s): **≈ 3.5 min heavy**.
