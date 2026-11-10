# Case file 183 — One bad letter in the columnar sandwich: case 182 under a single wrong crib letter (cycle 196)

**Status:** negative. **Type:** audit (195 was a new family). IDEAS [I-212](../IDEAS.md) via pointer I-211; part of I-003.
Pre-registered in [`tools/cycle196/PREREG196.md`](../tools/cycle196/PREREG196.md) (commits 7fc5072, ad67600, 3ed599b, 597e6c6, 10ef71e,
~19:52–19:53 PT) with the run script, pair lists, structure output, plants, checker, decoder, recount, aggregators, meter output and null
seeds, **after** a whole-bank structure pass, the one-error chance meter on 40 uniform random texts metered apart by tableau type (I-193,
I-205), a pre-K4 exactness recount and the control rehearsal (16/16, notes disclosed), and **before** any K4 or registered-null run. A second
pre-registration ([`PREREG196b.md`](../tools/cycle196/PREREG196b.md), commit 60b4740, ~19:57 PT) fixed the pooled reference for a grid rank
flag before any fresh null was run. Solver: case 181's [`cmp194.c`](../tools/cycle194/cmp194.c), **unchanged**; banks: case 182's col1/col2.

**Result in one line:** if K4 were made by **a periodic keyword pass on the plaintext (period m), a keyed columnar (case 50's 1,837 keyword
orders, either direction, or a themed double columnar), and a periodic keyword pass on the carved text (period n)** (case 182's sandwich:
A–Z>KRYPTOS, KRYPTOS>A–Z, A–Z>A–Z, KRYPTOS>KRYPTOS; Vig/Beau/variant; S1/S2) **and one of the 24 crib positions carried a wrong carved or crib
letter**, then **every registered cell has full power under one error and has been tested exactly: single columnar 139 ordered pairs per
model, themed double columnar 136 per model (each incl. 8 with m = n and 63–66 with lcm > 26, up to 105), 6,600 distinct cells run (8,800
counting the exact one-tableau equivalents), 9 fits against a bound of 12.41 (two-tableau 9 vs 8.27, one-tableau 0 vs 4.14), and all 9
decode in full to gibberish → `EXACT-EXCL` (one-error scope, chance fits decoded and rejected).** Pairs with cell U > 0.05 (486 / 489 per
model) were not run and are **`LOW-POWER`**. Controls 16/16; recount identical; one grid rank flag (raw e ≥ 3 count) traced to period-multiple
copies of two band-edge coincidences, cluster-aware count at chance. **No solution.**

## 1. Why this
Case 182 needed all 24 crib letters exact. K1–K3 carry slips (PALIMPCEST, IQLUSION, DESPARATLY, UNDERGRUUND), and a wrong letter on a cyclic
crib edge kills the planted config. Case 181 did this audit for the K3-law routes; this file does it for the keyed columnar between the
passes. Prior-coverage grep: no case file runs a one-error test with two arbitrary periodic keys around a keyed columnar. kryptosbot's
public record (findings page, status 29 Sep 2026) reports "a single error combined with a columnar transposition (with an optional periodic
key) … closed at widths 2–13", i.e. one periodic key; two arbitrary keys on both sides of the columnar are not in that statement.

## 2. Method (exact)
As case 181 (I-202): a wrong letter at slot t is a deleted edge; every slot of the failing component tried, deletions with the same 2-core of
K − t deduplicated; fit iff all cyclic components are consistent, or exactly one component K fails and some distinct core of K − t is
consistent. One-tableau stacks (A–Z>A–Z, KRYPTOS>KRYPTOS) are additive and BB = VV, BV = VB exactly (a → −a), so they run VV/VB only.

**Pair selection — exact, text-free.** The bound U = Σ_K Σ_d (E_G/E_K)·E_d depends only on the crib graph, so a structure-only pass over the
**whole** bank ([`struct196.txt`](../tools/cycle196/struct196.txt), 20 s) gives each cell's exact U (cycle 194 had to estimate it from 1/512).
Registered: cell U ≤ 0.05 → col1 **139 pairs per model** (Σ U 0.224 per tableau setting), col2 **136 per model** (Σ U 0.293). Side note: S2 at
(m, n) has the same crib graph as S1 at (n, m), so their U are equal (the ciphers differ).

**Meter before K4** (40 uniform texts, seeds 19640–19679, col1[::45] 82 rows and col2[::209] 81 rows, all 625 pairs;
[output](../tools/cycle196/meter196_out.txt)): two-tableau S1 vs U, col1 bands 1–4 z −1.38, −1.21, +1.17, −0.30; col2 −1.07, −1.10, −0.54,
−0.37, band 5: 1 fit vs U 0.053 (one event, ≈ 5 %). Fits in bands ≥ 3: col1 46 vs U 41.0, col2 36 vs 38.4. One-tableau bands low and lumpy as
in cases 180–182 (I-205), so U is conservative there.

## 3. Results (K4; [summary](../data/cycle196/summary196.txt), [fits](../data/cycle196/fits_k4_196.txt), [cells](../data/cycle196/cells_k4_196.txt))
| Cell | Scope | Full-power cells run | U in them | K4 fits | Verdict |
|---|---|---|---|---|---|
| C1a | col1 (3,674 single keyed columnars), A–Z>KRYPTOS + KRYPTOS>A–Z, 4 forms, S1 + S2 | 2,224 (139 pairs × 8 × 2) | 3.58 | 3 | `EXACT-EXCL` one-error (3 chance fits decoded, gibberish) |
| C1b | col1, A–Z>A–Z + KRYPTOS>KRYPTOS, VV/VB (= BB/BV) | 1,112 (+ 1,112 exact equivalents) | 1.79 | 0 | `EXACT-EXCL` one-error |
| C2a | col2 (16,928 themed double keyed columnars), two-tableau | 2,176 (136 × 8 × 2) | 4.69 | 6 | `EXACT-EXCL` one-error (6 chance fits decoded, gibberish) |
| C2b | col2, one-tableau stacks | 1,088 (+ 1,088 equivalents) | 2.34 | 0 | `EXACT-EXCL` one-error |
| — | pairs with cell U > 0.05 (col1 486, col2 489 per model) | not run | — | — | `LOW-POWER` |

**9 fits vs a bound of 12.41** (Poisson P(X ≥ 9 | 12.41) ≈ 0.87; two-tableau alone 9 vs 8.27, P ≈ 0.45). All decoded with
[`decode196.py`](../tools/cycle196/decode196.py) under every consistent deletion ([decodes](../data/cycle196/decodes196.txt)):
- col1 ELECTRONIC/enc S2 KA>AZ BB 13 × 6, del 12: `logncqkypjnzgqdaiowlo EASTNORTHEASY cmbcjrynrctd…` (97/97)
- col1 SAILORS/inv S2 KA>AZ BV 10 × 8, del 1 (config U 1.2 × 10⁻⁶): `mezskswjqdihzxdcwatlq EESTNORTHEAST jaettjlajt…`
- col1 ARRESTED/enc S1 AZ>KA VB 5 × 14, del 12: `viyjuhqhktbyqalvhaucd EASTNORTHEASM zltzccsx…`
- col2 IQLUSION+NORTHEAST/inv S1 KA>AZ VB 2 × 17, del 16: `gufyeziizkwuxieoyneew … BERGINCLOCK osfztokl…`
- col2 COLUMN+OBELISK/inv S2 AZ>KA VB 15 × 3, del 9 or 23: `qdvhmhbimxfkoceunjayp EASTNORTHYAST qektjyhl…`
- col2 LOCATION+DOUBLE/enc S1 KA>AZ VV 20 × 5, del 12 or 23 (65/97): `?emepuohqvdskd??????? … faphjthzoaczk…`
- col2 ANTIPODES+CHAMBER/enc S1 KA>AZ VB 10 × 8, del 11: `jvepvvsjocojoeekaumnf EASTNORTHEAJT xsmgbohf…`
- col2 PETRIFIED+TRANSPOSITION/inv S1 KA>AZ VV 15 × 3, del 5 or 21: `kxzkbxfpfvhvdbveoswqk EASTNBRTHEAST huohrnyj…`
- col2 TRUTH+WELTZEITUHR/enc S1 KA>AZ BB 19 × 3, del 8 or 17 (75/97): `??cjwvyujjfewjpfk???? … sj????cvstdpvplolnasx…`

Every one is random letters around the cribs; none has a word outside the cribs. The themed keyword names are row labels of the bank, not
evidence (every row of col2 is a pair of themed words).

## 4. Grid and the rank flag
**Grid** (K4 + 19 shuffles, seeds 19611–19629; tab2 + tab1s on col1[::8] = 460 rows, all 625 pairs; [grid](../data/cycle196/grid196.txt)):
two-tableau e ≥ 1 K4 22,781 vs 22,602–23,377 (p⁺ 0.80); e ≥ 2 312 vs 257–390 (p⁺ 0.50); **e ≥ 3 12 vs 1–8 (p⁺ 0.05, rank floor)**;
one-tableau p⁺ 0.25–1.00; pooled e ≥ 3 p⁺ 0.05.

**Pooled reference (PREREG196b, pre-registered before any fresh null; [result](../data/cycle196/pool196.txt)).** 40 fresh shuffles (19631–
19670) on the same cell: R (e ≥ 3 fits) 1–11, mean 5.42; pooled over 59 nulls 0 reach K4's 12, **p_pool 0.017** (= 1/60, the floor), binomial
SE 0.017. Registered verdict: **NOT REPLICATED** (rule p_pool ≤ 0.01). **Disclosed flaw in that rule:** with 59 nulls the smallest
attainable p is 1/60 = 0.017 > 0.01, so the rule could not have returned "replicated"; the honest reading is that raw R sits above all 59
nulls. **Why:** 8 of K4's 12 are period-multiple copies of two coincidences at the band edge (config U 2.8 × 10⁻⁴; CANNOT/enc and GAZING/enc
rows, S2 KA>AZ VB, n 24 or 16 with m 2/4/8, each the same key read at multiple periods). The cluster-aware count D (distinct row, model,
tableau pair, form; descriptive, defined after seeing the grid) is K4 6 vs pooled nulls 1–10, 19 of 59 ≥ 6, **p 0.33**. All of K4's e ≥ 3
grid fits sit in LOW-POWER cells and decode to gibberish ([grid decodes](../data/cycle196/griddecodes196.txt)). Not evidence; flag closed.
Lessons → I-216 (attainable thresholds), I-217 (cluster-aware grid statistic).

## 5. Controls and checks
- **Planted controls 16/16** (registered run 19:53:25 PT; [output](../data/cycle196/controls196.txt); [`plant196.py`](../tools/cycle196/plant196.py)
  = plant194 applied to case 182's plants, plant195 seed 19500 re-run byte-identical; one wrong carved crib letter (+7) on a 2-core slot;
  checker [`checkctl196.py`](../tools/cycle196/checkctl196.py)). P1 KRYPTOS columnar AZ>KA VV 7 × 11; P2 PALIMPSEST columnar KA>AZ BV 5 × 13;
  P3 LODESTONE inverse S2 8 × 12; P4 ALEXANDERPLATZ (width 14) KA>AZ VB 6 × 19; **P5 PALIMPSEST → KRYPTOS keyed columnar → ABSCISSA, slot 9**;
  P6 double KRYPTOS+PALIMPSEST A–Z>A–Z 3 × 25; P7 KRYPTOS>KRYPTOS BB 4 × 9 (found as VV); P8 m = n 7 × 7; P9 S2 BB 6 × 10: each found at its
  cell, and deleting the planted slot reproduces the planted plaintext everywhere except the corrupted letter. Plant config U span bands
  e = 1 (P4, 0.19) to e = 10 (P7), so recovery is not only for loud plants (answers the Voynich K063 remark that our plant recovery is
  reported pooled: P4 e 1, P3 e 2, P5 e 4, P6 e 4, P1 e 5, P2 e 6, P9 e 7, P8 e 8, P7 e 10, all recovered; an exact solver either finds a
  config in scope or has a bug, which the recount checks). P0 (no error) fits strictly. **PD (wrong letter on pendant slot 0) fits strictly
  and is reported as an undetectable error** (the strict decryption is wrong at 8 positions, the pendant edge's residue class). Negatives
  clean: N1 three passes, N2 random key, N3 = P1 with two wrong letters (slots 1 and 2), N4 a case-178 compound key, **N5 a K3-route sandwich:
  no fit at any columnar row** (found at its own route row).
- **Bank-level:** P5 with its wrong letter run against **all 3,674 rows of col1** (registered pairs, print U ≤ 0.05): found at row 0, config U
  1.3 × 10⁻⁶, together with 3 chance fits on other rows (2471 15 × 2 U 2.9 × 10⁻⁸; 1086 6 × 12; 2294 6 × 13) — one-error chance fits at the
  bound rate, the reason every K4 fit is decoded. P6 with its wrong letter on all 16,928 rows of col2 at its own (low-power) pair: found at
  row 2.
- **Rehearsal notes (disclosed in PREREG196):** solver reports the first slot of a deduplicated 2-core (P1 4 for 5, P3 4 for 23, P4 1 for 4,
  P6 3 for 22; I-195); the P5 bank check first printed at U ≤ 10⁻⁶ and hid P5's own row (I-214 again), now at the registered 0.05; the pre-K4
  recount script first interleaved two processes' output (spurious DIFFER), fixed with separate files.
- **Recount identical.** Before K4: [`recount196.py`](../tools/cycle196/recount196.py) (literal letter tables, all 25 deletions, no 2-core
  reduction; no shared code) on a uniform text (seed 19640), ctl195 rows 0 and 4, all 1,250 model-pairs: 13,712 fits identical. Registered:
  ctl195 (7 rows), all 1,250 model-pairs, tab2 × 4 + tab1s × 2: **K4 45,244, P1 45,402, P5 45,212, P6 45,437, n19611 45,305 fits, all
  identical**.

## 6. Cost
Structure pass 20 s, control rehearsal + bank checks 24 s, meter 54 s, pre-K4 recount 18 s; registered controls 12 s; registered run
19:53:37–19:56:01 PT (144 s: C1 9 s, C2 47 s, grid 52 s, recount 36 s); pooled reference 19:57:27–19:58:33 PT (66 s). ≈ 5.7 min heavy.

## 7. Limits (not covered)
- Pairs with cell U > 0.05 under one error (22 / 23 per model sit at 0.05–1, may be decidable with more care) → I-218.
- Themed × {A–Z, KRYPTOS} tableau pairs (case 182's C3) under one error; two or more wrong letters; dropped/extra letters (I-196).
- Double columnar beyond themed × themed; disrupted/Myszkowski columnars (I-213); m or n = 1 or > 26; three passes.
- A wrong letter on a pendant crib edge is invisible to every crib test (it only damages one residue class of the decryption).

## 8. Verdict
Keyword pass → keyed columnar (1,837 keyword orders either direction, or a themed double columnar) → keyword pass, on A–Z and/or KRYPTOS in
any order, Vig/Beau/variant, either index assignment, **with at most one wrong crib letter**: **`EXACT-EXCL`** in all registered cells (139 /
136 period pairs per model, every one full power under one error; 9 fits against a bound of 12.41, all decoded and rejected); **`LOW-POWER`**
for the pairs not run. No K4 solution.
