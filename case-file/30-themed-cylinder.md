# Case file 30 — The cylinder, rebuilt: KRYPTOS-themed disks, any number of disks, any starting disk

*Cycle 31, 2026-11-04. Status: **negative** directly on the copper; **no signal above chance** behind transpositions.*

## 1. Why this
Cycle 30 closed the Army M-94 (25 published disks, message starting on disk 1, one 25-letter line per offset). Its journal left two follow-ups: a cylinder whose disks are **keyword alphabets of the Kryptos words** (Bazeries built his disks from keyword phrases; Sanborn's K1–K2 alphabet is itself a keyword alphabet), and a cylinder with **fewer disks or a message that starts mid-cylinder**. Both are cheap, exact, and in the "simple thing in plain sight" spirit.

## 2. Model
- **Disk sets.** (a) THEMED: 30 keyword-mixed alphabets (keyword letters de-duplicated, then the rest of A–Z), from a word list fixed in code *before* any run: KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK, BERLINCLOCK, EASTNORTHEAST, SHADOW, ILLUSION, IQLUSION, LUCID, MEMORY, LANGLEY, SANBORN, SCHEIDT, WEBSTER, CARTER, EGYPT, TUTANKHAMUN, UNDERGRUUND, LAYERTWO, DESPARATLY, DIGETAL, INTERPRETATU, POSITION, MAGNETIC, VIRGINIA, ANTIPODES, MORSE, SLOWLY. (b) M94: the 25 disks from cycle 30.
- **Cylinder.** *n* distinct disks (any subset of the set, any order), *n* = 4 … 30 (themed) or 4 … 25 (M-94). The message may start on any disk (phase *s* = 0 … *n*−1). Letter *i* goes on disk (*i*+*s*) mod *n*, and every line of *n* letters is read off its own row offset *g* = 1 … 25.
- **Test.** Exact: each crib letter restricts which disks fit its column at each offset; a depth-first search over the offsets of the lines that hold cribs, then bipartite matching for distinct disks. No scoring.
- **Behind a transposition.** K4 = T(cylinder(P)) for each of the 165,065 transpositions of the cycle 19/22 family (column orders w ≤ 8, K3-style rotations, inverses, identity).

## 3. Results ([report](../analysis/cylinder_report.txt))
| Test | K4 | Shuffled-K4 nulls | Planted controls |
|---|---|---|---|
| Themed, direct (459 (n, s) cells) | **0** | 0 in all 20 | 3/3 found at their planted (n, s) |
| M-94, direct (319 cells) | **0** | 0 in all 20 | 3/3 found, each the only hit |
| Themed, behind 165,065 transpositions | 45 perms / 425 cells | 20–97 perms / 128–441 cells (10 nulls) | 2/2 planted (perm, n, s) found |
| M-94, behind 165,065 transpositions | 1 perm / 1 cell | 0–37 perms (10 nulls) | 2/2 planted (perm, n, s) found |

## 4. Verdict
| Hypothesis | Status |
|---|---|
| Themed-keyword cylinder (30 disks), any n ≤ 30, any start, any offset per line, on the copper | **impossible** |
| M-94 disks, any n ≤ 25 and any start disk (extends cycle 30) | **impossible** |
| Either cylinder behind any of 165,065 transpositions | **no signal**: K4's hit counts sit inside the shuffled-null range, so the filter cannot tell K4 from noise there |

## 5. Honest limits
- Behind transpositions the test only filters; a hit leaves free disks and free offsets for crib-free lines, so it cannot be read as English without a second stage. Because K4 is at the null level, I did not build that stage this cycle; it is a lead, not a closure.
- Only one layer order (cylinder first, transposition second). Order B (transposition first) was not run for the new disk sets.
- The themed list is 30 words; another word, or phrase disks (Bazeries style, multi-word), would need its own run. Many keyword alphabets share long straight tails, which makes the themed set more permissive than the M-94 set (seen in the controls: true ciphertexts light up neighbouring (n, s) cells too).

## Reproduce
```
python3 tools/cylinder_disks.py            # writes themed.txt, validates every disk is a permutation
gcc -O2 -o cyl tools/cyl.c
./cyl themed.txt k4.txt 4 30               # direct
./cyl m94.txt k4.txt 4 25
./cyl themed.txt k4.txt 4 30 perms97.bin   # behind the transposition family (a few minutes per text)
python3 tools/cylinder_controls.py         # planted controls and shuffled nulls
```
