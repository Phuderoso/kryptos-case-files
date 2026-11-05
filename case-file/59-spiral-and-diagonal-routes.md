# Case file 59 — Spiral and diagonal routes behind a periodic key

> *K3's clerk walked the room in a circle. Nobody had asked whether he ever walked it as a snail does, from the wall
> inward, or across it on the slant, corner to corner. Tonight I made him do both.*

## 1. Why this
The coverage table's transposition backbone (cycle 12's 96,630 permutations, cycle 13's 147,709 strips, cycle 44's
rail/Redefence/AMSCO, cycle 59's decimations) contains routes only as **8 row/column/boustrophedon read-offs**.
A grep of the case files found no **spiral** and no **diagonal** route: the two classic ACA "route" transpositions a
1989 hobbyist manual lists right after the row/column ones, and the most "drawn in plain sight" way to scramble a
grid. Diversity rule: new transposition structure (cycle 60 was an extension of autokey).

## 2. Model
- **Grids:** width w = 2–48, h = ⌈97/w⌉; text written row by row with the empty cells at the end, row by row with the
  empty cells at the start, or column by column. Empty cells are skipped when reading.
- **Routes (24 per grid, each also read backwards):** inward spirals from each of the 4 corners, clockwise and
  counter-clockwise (backwards = outward spirals); diagonal read-offs from each corner, both first-step directions,
  straight and zig-zag. Every route kept as a permutation **and** its inverse (write-by-route/read-by-rows and the
  reverse). 6,094 distinct permutations; 23 were already in the cycle-12 family, identity removed: **6,070 new**
  (0 overlap with the strip family). Generator: `tools/route_gen61.py`.
- **Substitution:** periodic Quagmire III (same keyed alphabet on both sides), Vigenère and Beaufort (variant =
  Vigenère consistency), key indexed by plaintext position or by carved position (both layer orders).
- **Test:** exact, `tools/periodic_exact59.c` (cycle 59), all 24 crib letters at the official positions must agree
  with one key letter per residue class. No scoring.

## 3. Controls and nulls
- 3 shuffled-K4 nulls (`data/cycle61/null*.txt`, seed 61).
- 3 planted controls (`data/cycle61/controls.txt`): a K3-flavoured plaintext with both cribs in place, encrypted
  through route permutations 1234, 6063, 3035 with KRYPTOS/PALIMPSEST Vig order 0, KRYPTOS/SHADOW Beau order 1,
  A–Z/ABSCISSA Vig order 1. **All three recovered with their exact key** (PALIMPSEST, SHADOW, ABSCISSA) on 264 themed
  alphabets; ctl1 also recovered on 20,946 alphabets.

## 4. Results (`data/cycle61/results61.txt`)
| Alphabets | Periods | K4 | Nulls (3) |
|---|---|---|---|
| 264 themed | 1–19 | **0** | 0, 0, 0 |
| 264 themed | 20 | 2 | 1, 1, 5 |
| A–Z + KRYPTOS | 1–21 | **0** | 0, 0, 0 |
| A–Z + KRYPTOS | 22 / 23 / 24 | 3 / 34 / 185 | 2–8 / 44–61 / 160–171 |
| 20,946 keyword alphabets | 1–14 | **0** | 0, 0, 0 |

K4's two p = 20 hits decrypt to noise outside the cribs (e.g. `EVKWWWNRVZBBPODTKOQSF·EASTNORTHEAST·ZXNRTVCX…`),
and their number sits inside the null range; at p ≥ 22 the cribs no longer constrain the key and the counts are the
same for K4 and the nulls.

## 5. Verdict
**Negative.** No spiral or diagonal route of a w × h grid (w 2–48, three fill conventions) under a periodic
Quagmire III key fits the cribs at periods where the test has power (≤ 19 themed, ≤ 21 A–Z/KRYPTOS, ≤ 14 on 20,946
alphabets). Not covered: spirals/diagonals in **non-rectangular** layouts (the sculpture's 4-row-of-K4 panel shape,
ragged rows of the carving itself), double routes (spiral then columnar), and running keys or autokey behind these
routes (cheap follow-up: reuse `autokey_exact60.c` with `route_perm.bin`).

## 6. Reproduce
`sh tools/run_cycle61.sh` (≈ 2.5 min on 8 cores).
