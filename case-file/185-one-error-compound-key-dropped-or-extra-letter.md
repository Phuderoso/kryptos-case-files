# Case file 185 — One letter off the copper and one letter wrong: case 184 under one wrong crib letter (cycle 198)

**Status:** negative (audit). **Type:** audit (197 was a new family). IDEAS [I-222](../IDEAS.md) via pointer I-221; part of I-003.
Pre-registered in [`tools/cycle198/PREREG198.md`](../tools/cycle198/PREREG198.md) (commits 4bf882a, f97de16, 50968a1, 1443e83, ~03:57–03:58 PT,
2026-11-10) with the solver, Python references, plants, checker, decoder, recount, grid and summary scripts, the meter output and the control
rehearsal (13/13), **after** the timing probe and a strict cross-check on the reserved shuffle (seed 19890), the meter on 40 uniform random
texts and the control rehearsal, and **before** any K4 or shuffled-K4 run.

**Result in one line:** if K4 were case 184's model — **two periodic keys stacked K1/K2-style** (one tableau A–Z or KRYPTOS, Vig/Beau,
K[i] = a[i mod m] + b[i mod n]; or two tableaux A–Z>KRYPTOS / KRYPTOS>A–Z, Vig/Beau/variant per pass), **one dropped or one extra carved letter**,
direct or behind a pure K3-law decimation of the true length — **and one of the 24 crib letters were also wrong**, then: **direct** (101 records):
solver A 360 full-power cells **0 fits vs U 1.29**, solver B 1,328 cells **2 fits vs U 5.14**; **behind the M = N decimations** (decM98 4,116 perms,
decM96 3,072): A 844 cells **0 vs U 2.06**, B 3,248 cells **2 vs U 4.20**. All 4 fits decoded under every equivalent slip position and every
equivalent wrong slot: gibberish (quadgram −7.76 to −8.10; plants ≈ −4.1) → **`EXACT-EXCL`** on those cells (one-error scope). The rest is
**`LOW-POWER`** or **not run** (one error behind the non-M = N decimation families; themed alphabets). **No solution.**

## 1. Why this
- Queue: I-221 named I-222 for this audit slot. Case 184 assumed every crib letter is right. K1–K3 carry both kinds of slip (K2's missing S,
  K1's misspelling, K3's extra/changed letters, case 10 with the case 12 corrections), so an indel *and* a wrong letter is the K1–K3-style
  combination that case 184 left open. A wrong letter in a 2-core can kill a true fit, so case 184's exclusion needed this check.
- Prior coverage: one-error audits of the compound keys without an indel exist (cases 177, 179, 181, 183); none with an indel.

## 2. Method ([`cmp198.c`](../tools/cycle198/cmp198.c), references [`lib198.py`](../tools/cycle198/lib198.py) + case 184's `lib197.py`)
- Records exactly as `cmp197` (case 184 §2): 101 direct records (readings R1/R2, both slips, incl. the indel-free record); perm mode on the
  pure 98/96-letter K3-law decimations (M = N), models P (plaintext index) and C (true-ciphertext index), d values identical on the cribs run once.
- **One-error fit:** the usable crib constraints are consistent outright, or after deleting one crib slot t. Consistency depends only on the
  2-core, so per (record, model, pair) the cyclic components K of the core are found; a config with exactly one failing component fits iff some
  distinct core of K − t is consistent (two failing components cannot be repaired by one deletion). Solver A = case 176's weighted union-find;
  solver B = cycle 192's bijection-graph programs (26 roots).
- **Chance bound per config:** U = Σ_K Σ_distinct d (E_G / E_K) · E(d) (+ E_G when G has pendant edges), E = 26^−excess (A) or Π 26^(1−r) (B),
  capped at 1. U is a union bound (≥ P(fit)); the meter below shows how loose it is. Cell = (stage, solver, model, alphabet/tableau, form, m, n);
  **full power = cell U ≤ 0.05.** The deletion search runs for every config with U ≤ 0.05 (so every config of a full-power cell); others strict only.
- **Additive caveat (new, I-228):** in solver A a bridge of the 2-core never constrains, so a wrong letter there is invisible — the model
  still fits strictly and decodes one letter wrong. Solver B bridges do constrain and are searched like any slot.
- Pair lists: case 184's text-free lists unchanged (direct `pairsA_all` 260 / `pairsB_all` 600 pairs; decimations A del 113, ins 124,
  B del 264, ins 310 lines over both models). Alphabets A–Z and KRYPTOS only (case 184's 18,824 direct alphabets were low power already).
- Probe checks before registration: strict counts identical to `cmp197` on all 5,840 direct cells; the component-wise search gives output
  identical to a first global-core version (direct and decM96 every 8th).

## 3. Results ([`summary198.txt`](../data/cycle198/summary198.txt), [`k4_cells198.txt`](../data/cycle198/k4_cells198.txt), [`k4_fits198.txt`](../data/cycle198/k4_fits198.txt), [`k4_decodes198.txt`](../data/cycle198/k4_decodes198.txt))
| stage | solver | full-power cells | fits there (strict) | U there | low-power: searched fits vs U | label |
|---|---|---|---|---|---|---|
| direct, 101 records | A, A–Z/KRYPTOS × vig/beau | 360 | **0** (0) | 1.29 | 38 vs 33.9 | `EXACT-EXCL` / `LOW-POWER` |
| direct, 101 records | B, AZ>KA, KA>AZ × 4 forms | 1,328 | **2** (0) | 5.14 | 146 vs 249.4 | `EXACT-EXCL` (fits decoded) / `LOW-POWER` |
| decM98 drop, 4,116 perms (175,806 records) | A | 384 | **0** (0) | 0.98 | 10 vs 9.7 | `EXACT-EXCL` |
| decM98 drop | B | 1,488 | **1** (0) | 2.35 | 1,581 vs 1,868 | `EXACT-EXCL` (fit decoded) / `LOW-POWER` |
| decM96 extra, 3,072 perms (76,800 records) | A | 460 | **0** (0) | 1.08 | 1 vs 2.7 | `EXACT-EXCL` |
| decM96 extra | B | 1,760 | **1** (0) | 1.86 | 1,195 vs 1,590 | `EXACT-EXCL` (fit decoded) / `LOW-POWER` |

- **Full-power fits, decoded** under every equivalent d (I-223) and every slot giving the same one-error event (same 2-core):
  direct record 5 (d 23) KA>AZ BV 8 × 11, wrong slot 4 → `YYSXXWXPHWHJRPMWMFRFOEA?TDORTHEASTZNETITGHT…` (−8.07);
  direct record 29 (d 63) KA>AZ VB 6 × 13, slot 10/20 → `NGHURVWPDBYJWGCGZMUQW EASTNORTHEAST SKABRUHFDYQ…` (−7.76);
  decM98 #3671 d 63 P AZ>KA BV 3 × 20 (U 3.3 × 10⁻⁸) → `?RUQIAARDFTPQS???…` (−7.94); decM96 #1415 d 10 C AZ>KA BV 11 × 6 (5.5 × 10⁻⁸) →
  quad −8.10. Gibberish, rejected. 4 fits against a summed bound of 12.7 (and 0 strict) is chance.
- **Case 184's strict fits reappear** (decM98 #90 C AZ>KA BB 17 × 2 and #1671 C KA>AZ BB 15 × 4, now in low-power cells because one error
  widens U), a free consistency check between the two solvers.
- **Strongest low-power fits** (20 smallest U, one per perm and cell, U 3.6 × 10⁻⁸ to 1.2 × 10⁻⁶): best quad −7.24 on 5 quadgrams, −7.53 on 63;
  nothing English (e.g. `…EASTNORTHEASTTSENTHEWWLETFLLOULL…`). With one error the low-power cells are crib-starved by construction.
- **Grid** ([`grid198.txt`](../data/cycle198/grid198.txt); direct records + every 128th M = N perm; K4 and 19 shuffles, seeds 19851–19869):
  distinct clusters with a one-error fit at U_config ≤ 26⁻²: **K4 16, nulls 12–26, p⁺ 0.90**, non-degenerate (I-224). At chance. On the direct
  records alone K4 has 2 full-power fits against 1–11 for the shuffles (mean 5.1).

## 4. Controls, meter, recount
- **Controls 13/13** ([`controls198.txt`](../data/cycle198/controls198.txt), rerun after the K4 run, identical to the rehearsal): case 184's plants
  with one carved crib letter replaced on a 2-core slot — P1e direct R1 drop d 50 KA vig ABSCISSA + PALIMPSEST (slot 3); P2e direct R2 extra d 30
  AZ beau BERLIN + KRYPTOS; P3e direct R1 extra d 5 AZ>KA VV CLOCK + NORTHEAST; P4e direct R2 drop d 70 KA>AZ BV ABSCISSA + PALIMPSEST; P7e decM98
  drop d 60 C AZ>KA VB TIME + KRYPTOS; P8e decM96 extra d 10 P KA>AZ VV SHADOW + LIGHT; P10e decM98 drop d 30 P KA vig ABSCISSA + PALIMPSEST
  (reported slot 6 = the same event as the planted slot 17); P11e decM96 extra d 20 C AZ beau CLOCK + BERLIN — each found in its cell at the
  planted record with the planted (or an equivalent) slot and decoded by `lib197` to the plaintext at every determined position except the
  altered letter; P1s (no error) found strictly; P1b (wrong letter on a bridge) found strictly, as documented. Negatives N3 / N4 (two wrong
  letters) and N1 (three keys) gave no fit in the planted cell; at the planted record other cells gave chance fits (N3 8, N1 1), reported.
  Rehearsal changes (before registration, disclosed): P1e first drew a bridge slot → kept as P1b and redrawn; N1 criterion narrowed to the
  planted cell; control decimation runs restricted to the planted perm.
- **Meter** ([`meter198.txt`](../data/cycle198/meter198.txt), 40 uniform texts, direct records): full-power cells 162 fits vs U 257.4 (the union
  bound holds and is ≈ 1.6× loose); low-power searched configs 6,927 vs 11,331. The 19 shuffles on the direct records: 96 vs 122.3.
- **Recount** ([`recount198.txt`](../data/cycle198/recount198.txt)): independent Python (no cores, no union-find, no dedup; BFS on G and on
  every G − t) on K4's 101 direct records, A on all 260 pairs, B on the 30 pairs with m, n ≤ 7, against `cmp198` with the search on every
  config: **1,280 cells, 57,441 fits, 0 mismatches.**

## 5. Scope, blind spots, budget
- Exact under: one dropped or one extra letter; at most one wrong letter among the 24 crib positions (carved or crib side); two periodic keys
  2 ≤ m, n ≤ 26 on the listed pair lists; A–Z/KRYPTOS (solver A) or AZ>KA/KA>AZ (solver B); direct or behind the pure K3-law decimations.
- A wrong letter on a bridge (solver A) is invisible to any crib test; those configs are covered by the strict fit and decode one letter wrong.
- **Not covered:** one error behind the non-M = N decimation families (case 184 ran solver A there strictly; ≈ 24× cost, needs a faster
  deletion solver: I-227, I-231); themed/keyed alphabets; two wrong letters; indel + wrong letter + three keys; m or n > 26.
- **Budget overrun (disclosed):** heavy compute ≈ 18 min against the 8-minute target — probe ≈ 3 min (s8 banks, gprof), rehearsal 3.1 min
  (control decimation runs over whole sample banks, since restricted), meter 8 s, **registered run 03:58:40–04:09:56 PT = 11.3 min**
  (K4 9.4 min, nulls 1.9 min), control rerun 4 s, recount 25 s. The probe had predicted ≈ 10 min for the M = N stage and the run was not
  cut to fit; lesson I-229.

## 6. What it means
Allowing K2's kind of slip *and* one wrong crib letter does not rescue the two-keyword stack: where the 24 cribs still have power after one
letter is forgiven (direct and behind the true-length decimations), four fits turned up against a bound of 12.7, and all four are static.
Case 184's exclusion is robust to one bad crib letter on those cells.
