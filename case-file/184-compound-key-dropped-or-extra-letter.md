# Case file 184 — The letter that fell off the copper: a compound key with one dropped or extra carved letter (cycle 197)

**Status:** negative. **Type:** new family (196 was an audit). IDEAS [I-196](../IDEAS.md) via pointer I-215.
Pre-registered in [`tools/cycle197/PREREG197.md`](../tools/cycle197/PREREG197.md) (commits a616108, 3e735fb, 15b4011, 7f7894e, e7f604e,
84c8186, 848dfc6, ~23:55–23:57 PT, 2026-11-09; the file's "~23:59" header time is a typo for ~23:55) with the solver, the Python reference, the
registered run script, the text-free pair lists, plants, checker, recount and meter output, **after** the timing probe and the structure pass
(reserved shuffle 19790 only), the chance meter on 50 uniform random texts and the control rehearsal (11/11, checker fixes disclosed), and
**before** any K4 or shuffled-K4 run.

**Result in one line:** if K4 were made by **two periodic keys stacked K1/K2-style** — on one tableau (A–Z or KRYPTOS; Vig/Beau; K[i] = a[i mod m]
+ b[i mod n], case 176) or on two tableaux (A–Z>KRYPTOS or KRYPTOS>A–Z, Vig/Beau/variant per pass, case 178) — **and one ciphertext letter was
left off the copper or one extra letter was carved** (K2's missing S), applied directly or behind a K3-law decimation of the 98/96-letter true
ciphertext, then: **direct** (101 distinct crib records, both crib readings): solver A on 18,824 alphabets 530 full-power cells, **0 fits vs
E 0.87**; solver B 1,552 full-power cells, **0 fits vs E 1.16**; **behind decimations**: solver A on all 170,258 (drop) + 168,858 (extra)
decimations (11.6 M records), 932 full-power cells, **0 fits vs E 1.92**; solver B on the pure decimations M = N (4,116 + 3,072 perms), 4,496
full-power cells, **4 fits vs E 7.21**, all decoded under every equivalent drop/insert position, gibberish → **`EXACT-EXCL`** on those cells.
The rest is **`LOW-POWER`** (totals at the chance line) or **not run** (solver B behind the non-M = N decimations; I-220). **No solution.**

## 1. Why this
- Queue: I-215 named I-196 for this new-family slot. K1–K3 each carry a slip, and K2's is exactly this kind: a letter missing from the copper,
  which shifts every later position. Cases 176–183 put two arbitrary keys on K4 but assumed every carved letter is where the cribs say.
- Prior coverage (grep of case files 23, 24, 161, 163, 176–183): indels were tested only with **one** periodic key (case 23 direct and behind
  the cycle-19 family; case 161 behind these same 96/98-letter decimation families; case 24 two slips; case 163 two slips + Hill). Two-key
  compound keys with an indel are not in the files. kryptosbot's public findings (status 29 Sep 2026) list single-error tests with one optional
  periodic key, not two.
- Style fit (case 10): two meaningful keywords on the KRYPTOS tableau (PALIMPSEST/ABSCISSA), a K3-law transposition, one-letter slip. The
  test is exact and keyword-agnostic: any key of periods m, n (keywords included) is covered.

## 2. Method ([`cmp197.c`](../tools/cycle197/cmp197.c), reference [`lib197.py`](../tools/cycle197/lib197.py))
- **Slip model (case 23 conventions):** `del` — true ciphertext C′ of 98 letters, C′[d] not carved (d 0–97); `ins` — C′ of 96 letters, an
  extra letter carved at carved index d (0–96). A crib whose ciphertext letter was the dropped one (or whose carved position is the extra
  letter, reading R2) is unusable and is skipped.
- **Records:** per (transposition, d), each crib's key index (plaintext index, model P; C′ index, model C) and carved index. d values that
  give the same record are run once — they are the same test on the cribs — but **the off-crib decryption depends on d**, so every decode is
  repeated for every d of the run (I-223).
- **Direct:** reading R1 (cribs at the official positions of the 98/96-letter plaintext) and R2 (cribs at the official carved positions);
  [`recs197.py`](../tools/cycle197/recs197.py) → 101 distinct records (includes the indel-free record: a drop after the last letter).
- **Behind decimations:** case 161's 96/98-letter K3-law families ([`decgen173.py`](../tools/cycle173/decgen173.py), 168,858 / 170,258 perms),
  cribs at plaintext 21–33 / 63–73 (0-based), models P and C.
- **Solver A** (one tableau): case 176's weighted union-find over Z26, pairs 2 ≤ m < n ≤ 26, n mod m ≠ 0; E_config = 26^−excess, exact.
- **Solver B** (two tableaux): case 178's bijection graph (26 roots per cyclic component, propagate), forms VV/VB/BV/BB, ordered pairs m ≠ n;
  E_config = Π 26^(1−r_c), the exact expected solution count.
- **Pairs behind decimations fixed text-free** ([`select197.py`](../tools/cycle197/select197.py)): the structure pass (E is structure-only) on
  every 32nd perm (A) or every 8th M = N perm (B), scaled; run if the estimate ≤ 0.10. Run: A drop P 63 / C 50, extra P 70 / C 54; B drop P 138
  / C 126, extra P 166 / C 144 (lcm up to 105). Labels use the **exact** cell E printed by the run (full power ≤ 0.05).
- **Scope cut, registered:** solver B on the whole decimation families was probed at ≈ 700 s for the selected pairs (I-180 probe on 200 perms),
  over budget, so B ran on the pure decimations M = N only (no skipped slots: the K3 law at the true length).

## 3. Results ([`summary197.txt`](../data/cycle197/summary197.txt), [`k4_cells197.txt`](../data/cycle197/k4_cells197.txt), [`k4_decodes197.txt`](../data/cycle197/k4_decodes197.txt))
| stage | solver | configs | full-power cells | fits there | E there | low-power fits vs E | label |
|---|---|---|---|---|---|---|---|
| direct, 101 records | A, 18,824 alphabets × vig/beau | 101 × 520 pairs × 37,648 | 530 | **0** | 0.87 | 478,101,794 vs 478,106,000 (−0.001 %) | `EXACT-EXCL` / `LOW-POWER` |
| direct, 101 records | B, AZ>KA, KA>AZ × 4 forms | 101 × 600 × 8 | 1,552 | **0** | 1.16 | solutions 248,408 vs 264,083 (heavy-tailed, as in the meter) | `EXACT-EXCL` / `LOW-POWER` |
| dec98 drop, 170,258 perms, 7,365,696 records | A, A–Z/KRYPTOS | P + C, 113 pairs | 436 | **0** | 1.20 | 0 vs 1.34 (16 cells) | `EXACT-EXCL` |
| dec96 extra, 168,858 perms, 4,221,450 records | A | P + C, 124 pairs | 496 | **0** | 0.72 | — | `EXACT-EXCL` |
| decM98 drop, 4,116 perms, 175,806 records | B | P + C, 264 pairs | 2,064 | **2** | 3.43 | 4 vs 3.99 (48 cells) | `EXACT-EXCL` (fits decoded) |
| decM96 extra, 3,072 perms, 76,800 records | B | P + C, 310 pairs | 2,432 | **2** | 3.78 | 4 vs 2.95 (48 cells) | `EXACT-EXCL` (fits decoded) |

- **Full-power fits, all decoded under every equivalent d** (I-223): decM98 #90 d 25 model C AZ>KA BB 17 × 2 (E_config 2.2 × 10⁻⁶) →
  `QIRHHRFEYMPUHKATDZBQIEASTNORTHEAST QPNPZBKV…`; decM98 #1671 d 5 C KA>AZ BB 15 × 4 → `GGFBWSZTJNZIIBPVSXVSM…`; decM96 #2861 d 50 P AZ>KA BV 6 × 20
  (8.4 × 10⁻⁸) → `?BVDHHXDQJITYQ???…`; decM96 #2568 d 24–27 P KA>AZ VV 4 × 19 → `??JZBJWNVNNHKLOHE…`. Off-crib quadgram −7.69 to −8.31 (the plants'
  plaintexts score −4.13 to −4.16 with the same scorer, `decode197.py`). Gibberish, rejected. 4 fits vs E 7.21 is chance.
- **Strongest low-power fits** (the 20 smallest E_config, plus all 8 low-power B fits on the decimations and all 11 direct B prints): best
  direct A PERFORMANCES/KRYPTOS-keyed vig 8 × 11, record 85 (d 66), excess 6, E_config 3.2 × 10⁻⁹ → `MHAIYPCUGCEXPWEFGFOIZ EASTNORTHEAST YAQDOBFV…`,
  quadgram −8.21. Best score of all 43 decodes −7.49. Nothing English. With 18,824 alphabets the direct cells are low power by construction
  (E 4.8 × 10⁸ total), so these are the expected coincidences.
- **Grid** ([`grid197.txt`](../data/cycle197/grid197.txt); K4 and 19 shuffles, seeds 19751–19769, on the direct records with A–Z/KRYPTOS and
  the sample banks): cluster-aware count of fits at E_config ≤ 26⁻³ (I-217): K4 2, nulls 0–4, **p⁺ 0.50**; raw 2 vs 0–7 (0.55); full-power fits
  on the sample banks 2 vs 0–9 (0.70). At chance. Disclosure: the first pass of `grid197.py` read the solution-count column of solver B lines
  as E_config, so every text scored 0 (a degenerate statistic, not a result); fixed (one column index) before reading the ranks (→ I-224).

## 4. Controls, meter, recount
- **Controls 11/11** ([`controls197.txt`](../data/cycle197/controls197.txt), rerun after the K4 run, identical to the rehearsal): P1 direct R1
  drop d 50, KRYPTOS vig ABSCISSA + PALIMPSEST; P2 direct R2 extra letter inside EASTNORTHEAST (d 30), A–Z beau BERLIN + KRYPTOS; P3 direct
  R1 extra d 5, AZ>KA VV CLOCK + NORTHEAST; P4 direct R2 drop d 70, KA>AZ BV ABSCISSA + PALIMPSEST; P9 indel-free plant, found at the trailing-drop
  record; P5 dec98 drop d 40 model P KRYPTOS vig ABSCISSA + PALIMPSEST; P6 dec96 extra d 80 model C A–Z vig CLOCK + BERLIN; P7 decM98 drop d 60
  model C AZ>KA VB TIME + KRYPTOS; P8 decM96 extra d 10 model P KA>AZ VV SHADOW + LIGHT — each found in its cell at a record the checker
  rebuilt independently, and decoded by `lib197` to the planted plaintext at every determined position (48–97 of 96–98; gcd(8, 10) = 2 leaves
  half the positions undetermined for PALIMPSEST + ABSCISSA). N1, N2 (three keys CLOCK + KRYPTOS + BERLINCLOCK, drop) gave no fit at the planted
  record. Rehearsal fixes (checker only): decode under every d of an equivalent run; a stale loop variable for the direct map; the indel-free
  plant's 98-letter frame.
- **Meter** ([`meter197.txt`](../data/cycle197/meter197.txt), 50 uniform texts, before K4): full-power bands direct A 68 vs E 32.0 (44 from one
  text: one coincidence repeated over overlapping records and nested pairs 2 × 25 ⊂ 10 × 25; z −1.29 without it), direct B solutions 36 vs 46.4,
  sample banks A 1 vs 1.03, B 25 vs 17.6 (z +1.78). Low-power bands are heavy-tailed (products of component counts, overlapping records), so
  Poisson z is no test there; K4's low-power totals sit on the chance line (A −0.001 %).
- **Recount** ([`recount197.txt`](../data/cycle197/recount197.txt)): an independent Python solver (BFS propagation, exhaustive roots, its own
  tables; no union-find) on 4,604 K4 cells (direct, both solvers; decimation subsets incl. low-power pairs to have fits to count):
  **1,016,222 fits, identical, 0 mismatches.**

## 5. Scope, blind spots, budget
- Exact under: the slip is one dropped or one extra letter (not both, not two); the crib letters are otherwise right; two periodic keys with
  2 ≤ m, n ≤ 26; the listed tableaux; direct or behind K3-law decimations of the true length.
- **Not covered:** solver B behind the non-M = N decimations (≈ 98 % of the families; I-220); themed/keyed alphabets behind the decimations
  (solver A ran 18,824 alphabets only directly; I-225); an indel plus a wrong crib letter (I-222); two indels; three keys; m or n > 26;
  transpositions other than K3-law decimations (columnars with an indel and two keys: I-213 family).
- Heavy compute ≈ 10.5 min in total (probe 19 s, structure pass 34 s, rehearsal 12 s, meter 87 s, registered run 23:57:18–00:03:19 PT = 6.0 min,
  recount 102 s, control rerun 12 s), **over the 8-minute budget by ≈ 2.5 min**; the recount was the extra. Every step ran under `timeout`.

## 6. What it means
Putting K2's kind of slip into the K1/K2 two-keyword model does not open K4: wherever the 24 cribs can judge (small and middle period pairs,
lcm up to 105), nothing fits beyond chance, and what fits reads as static. The slip moves the shift, but no shift makes a two-key stack
agree with EASTNORTHEAST and BERLINCLOCK. Next: an audit slot (I-221).
