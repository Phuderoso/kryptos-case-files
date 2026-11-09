# Case file 176 — Two keywords, one tableau: the compound key of periods m and n behind K3's decimation law (cycle 189)

**Status:** negative. **Type:** new family (188 was an audit). IDEAS [I-189](../IDEAS.md), with add-on I-184 (finished).
Pre-registered in [`tools/cycle189/PREREG189.md`](../tools/cycle189/PREREG189.md) (commits 5ef5558, 9d1d4a0, f4a6810, ~14:50 PT) with the
plants, decoder, checker, recount, run script and null seeds, **after** the planted controls had been rehearsed (10/10) and the solver timed under
rule I-180 on the reserved shuffle (seed 9189, I-116), before any K4 or registered-null run. New solver: [`cmp189.c`](../tools/cycle189/cmp189.c).
Checked new against cases 12, 14, 52, 119, 134, 154 and 155 (case 119 tested only **named** word pairs; case 14's long periods are LOW-POWER).

**Result in one line:** if K4 were enciphered with **two arbitrary periodic keys of lengths m and n stacked on one tableau** (A–Z or KRYPTOS;
any mix of Vigenère, Beaufort and variant passes), the combined key K[i] = a[i mod m] + b[i mod n] has period lcm(m, n) — up to 168 here — but
only m + n − 1 free values. **On all 165,782 K3-law decimations/routes, with the key on the plaintext index or on the carved index, every
full-power pair (90 per form for the plaintext index, 59 for the carved index; 74 / 43 of them with lcm > 26) has 0 fits except one carved-index
cell (7 × 13, Vig, A–Z), whose single fit decodes in full to gibberish → `EXACT-EXCL` (one chance fit decoded and rejected).** The same holds
direct for 18,824 keyed alphabets (Quagmire III, 97 full-power pairs per form, 0 fits) and for the 144 themed alphabets on every 512th route
(0 fits). The other pairs are **`LOW-POWER`**: the cribs cannot pin them, and their fit counts equal the analytic chance rate to 0.01 %.
19 shuffles at chance; controls 10/10; recount identical (161,948 fits). Add-on: case 174's strict direction r now covers **8/8** of the routes
(I-184 done, with per-offset alignment controls 4/4). **No solution.**

## 1. Why this
K1 used one keyword (PALIMPSEST) on the KRYPTOS tableau, K2 another (ABSCISSA). The obvious "two systems, layers of something simple" move is to
run the text through the tableau **twice**, with two keywords. On one tableau every such stack collapses to a single additive key in the
tableau's index space: Vig∘Vig → c = p + (a + b); Beau∘Beau → c = p + (b − a); Vig∘Beau and Beau∘Vig → c = K − p; variant just flips a sign.
So the whole family is c = p + K or c = K − p with **K[i] = a[i mod m] + b[i mod n]**. The period is lcm(m, n): 7 and 11 give 77, 8 and 10
(the lengths of ABSCISSA and PALIMPSEST) give 40, well past every periodic exclusion in this repo (p ≤ 26 direct, ≤ 20 behind transpositions).
But the structure is thin: m + n − 1 unknowns against 24 crib equations, so many pairs can still be tested **exactly**, for every keyword pair
of those lengths at once. kryptosbot's public FAQ lists "keys longer than our checks cover (for example, repeating keys of 27 to 29 letters, or 53 or
more)" among its open gaps `[sourced: kryptosbot.com/faq, read 2026-11-09]`; a compound key is the simplest way a hand cipherer gets such a key.

## 2. Method (exact)
For a route (perm P: plaintext i carved at P[i]), an alphabet T used on both sides, a form (vig: K = T(c) − T(p); beau: K = T(c) + T(p)) and a
model — **P** = key on the plaintext index (substitute, then transpose) or **C** = key on the carved index (transpose, then substitute) — each crib
slot t gives one equation a[u] − b′[v] = K_t with u = pos mod m, v = pos mod n, b′ = −b. `cmp189` runs a weighted union-find over Z26 on the
bipartite residue graph: an edge inside a component must close its cycle with sum 0 mod 26, otherwise it merges two components. No division is
needed, so the test is exact mod 26 with no CRT split. **excess** = 24 − merging edges = number of independent checks, so the chance of a random
pass is 26^−excess; `cmp189` sums it per cell as the **expected chance count E**. A cell (pair × model × form, over its routes and alphabets) with
E ≤ 0.05 has full power; above that it is LOW-POWER by construction. Pairs: m 2–25, n m+1–26, m ∤ n (260 pairs). Every fit can be decoded by
`decode189.py` (breadth-first propagation, separate code): it fills every plaintext position whose two residues lie in one crib component.

## 3. Results ([`summary189.txt`](../data/cycle189/summary189.txt), [`c1_k4_full.txt`](../data/cycle189/c1_k4_full.txt), [`runlog189.txt`](../data/cycle189/runlog189.txt))
| cell | routes × alphabets | configs | full-power cells (fits) | low-power cells: fits vs chance E |
|---|---|---|---|---|
| **C1** A–Z, KRYPTOS; P and C; vig/beau | 165,782 × 2 | 3.45 × 10⁸ | P 90 + 90 (0); C 59 + 59 (**1**, vig 7 × 13) | 118,159,366 vs 118,159,096 |
| **C2** direct; 18,824 keyed alphabets | 1 × 18,824 | 9.79 × 10⁶ | 97 + 97 (0) | 4,474,069 vs 4,474,691 |
| **C3** 144 themed; P and C | 324 (all_s512) × 144 | 4.85 × 10⁷ | P 90 + 90, C 66 + 66 (0) | 16,784,262 vs 16,784,515 |

- **The one full-power fit** (C1, route 46579, A–Z, Vig, carved index, m 7, n 13, excess 5; cell E 0.0086, but the 298 full-power cells of C1
  together expect 1.43 chance fits) pins the whole key and decodes all 97 letters:
  `FZGYDUKYPGGAXYHEHTJAIEASTNORTHEASTHPOWTMMTFMGHLQRJCCFICIYHSQDTFBERLINCLOCKZFXEEPXFDXPRIYLYBIVVBQZ` — no English outside the cribs.
  Rejected; the cell is excluded by the decode. One more excess-5 fit (route 164674, Beau 10 × 25) lies in a low-power cell (E ≈ 26,000) and
  decodes 55 letters of noise.
- **Full-power pairs** (the exact list per model and form is in `summary189.txt`): for the plaintext index, every m ≤ 9 with most n up to
  19–23, plus 12 × 14/16/18/21, 14 × 21 and 16 × 24 (lcm up to 168); for the carved index, m ≤ 9 with n up to 12–19 and 10 × 15 (lcm up to 99).
  This includes **8 × 10** (ABSCISSA and PALIMPSEST lengths) and **7 × 11** (KRYPTOS and BERLINCLOCK lengths) in both models.
- **Low-power pairs:** 118 pairs have excess 0 on the plaintext index (the residues of positions 21–33 and 63–73 never close a cycle), so any keys
  fit; most pairs with m ≥ 10 or n ≥ 20 are in this group. The fit totals match the analytic chance rate in every run (C1: +270 on 1.18 × 10⁸),
  which doubles as a calibration of the excess count.
- **Scope:** `EXACT-EXCL` for the full-power cells above, with the stated alphabets, both forms (so every Vig/Beau/variant stack on one tableau),
  both key indexings and the stated route sets. `LOW-POWER` elsewhere.

## 4. Grid ([`grid189.txt`](../data/cycle189/grid189.txt); I-152 empirical rank, 19 nulls, seeds 18911–18929)
| statistic | K4 | nulls (min–max, mean ± SD) | p⁺ / p⁻ |
|---|---|---|---|
| all_s512, A–Z/KRYPTOS: fits in full-power cells | 1 | 0–6, 1.8 ± 1.8 | 0.80 / 0.65 |
| all_s512: fits with excess ≥ 3 | 2 | 1–9, 3.8 ± 2.0 | 0.80 / 0.25 |
| all_s512: all fits | 233,059 | 233,028–233,189, 233,115.6 ± 42.0 | 0.90 / 0.15 |
| direct, 18,824 alphabets: fits in full-power cells | 0 | 0–3, 0.8 ± 1.0 | 1.00 / 0.50 |
| direct: fits with excess ≥ 3 | 36 | 26–48, 34.6 ± 6.4 | 0.45 / 0.60 |
| direct: all fits | 4,474,069 | 4,473,165–4,475,621, 4,474,734.6 ± 574.1 | 0.85 / 0.20 |

K4 sits inside the shuffles everywhere. No rank flag. (The all_s512 full-power fit is a lower-excess fit in a cell that is full power only on
324 routes; it is not in C1's excess ≥ 5 list and the shuffles average 1.8 such fits.)

## 5. Add-on: I-184 finished, with per-offset alignment controls ([`runlog189.txt`](../data/cycle189/runlog189.txt))
Case 174's strict direction r (Quagmire IV, A vocabulary × B themed, carved-index linear-recurrence key L 1–3), `lrk186` cycle-187 binary, on
classes all.bin[6::8] and all.bin[7::8] (20,722 routes each): **0 fits**, END on both (27 s each). Case 174 direction r now covers **8/8** of the
routes → `EXACT-EXCL` (strict) on the full set; I-184 closed. Answering the Voynich desk's C096 offer (a per-offset alignment check), each class
file was first checked byte for byte against all.bin[r::8] (identical), and two case-174 plants were placed at global rows 8k + r:
A6 (class 6, k 1000, Vig L 2) was found at local row 1000 in the class-6 file and not in the class-7 file, and A7 (class 7, k 15000, Beau L 3)
the other way round: **4/4**.

## 6. Controls ([`runlog189.txt`](../data/cycle189/runlog189.txt), [`texts189.txt`](../data/cycle189/texts189.txt))
Plants by `plant189.py` (seed 18900), which applies the two passes literally, letter by letter, with its own code: P1 A–Z, P, Vig 7 + Vig 11
(q 12345); P2 KRYPTOS, C, Beau 5 + Beau 13 (q 100000; reduces to Vig); P3 PALIMPSEST/Z, C, Vig 8 + variant 12 (q 18944); P4 KRYPTOS, P, Vig 6 +
Beau 19 (q 165781); P5 direct, A–Z, Vig PALIMPSEST then Vig ABSCISSA; P6 direct, KRYPTOS, carved, Beau KRYPTOS then Vig BERLINCLOCK; P7 A–Z, C,
variant 3 + Vig 25 (q 51712). **All 7 were found** at their route, alphabet, reduced form, model and pair. Negatives with no full-power fit at the
planted route: N1 three stacked periods (5, 7, 11), N2 a random 97-letter key, N3 = P1 with one wrong carved crib letter. **10/10.**
Recount: `recount189.py` (left null spaces mod 2 and mod 13 by numpy elimination, no union-find) on 45 rows × 2 alphabets × 260 pairs × 2 models × 2
forms for K4, P1, P2, P7 and n18911: **161,948 fits, identical sets**, planted fits present.

## 7. Limits
- **Two different tableaux** (e.g. one pass on A–Z and one on KRYPTOS, as K1 and K2 used different settings): not additive, not tested (I-190).
- **Three or more passes**; pairs with n > 26; **one carving error** (the audit is due next, I-191).
- Vocabulary alphabets were run direct only; behind the routes only A–Z, KRYPTOS (all routes) and the 144 themed alphabets (1/512).
- Low-power pairs (excess ≤ 4 on the plaintext index, more on the carved index) stay open by construction; a longer crib would be needed.
- Budget: probes ≈ 3 s, controls ≈ 3 s, recount rehearsal < 1 s, registered run 124 s (C1 11 s), alignment controls < 1 s: **≈ 2.2 min heavy**.
