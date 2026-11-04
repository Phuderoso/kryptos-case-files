# Case file 29 — The M-94 cylinder (Jefferson/Bazeries wheel cipher), alone and behind a transposition

*Cycle 30, 2026-11-04. Status: **negative** for the 25 published M-94 disks.*

## 1. Why this, why now
Every cycle so far assumed one tableau (straight or KRYPTOS-keyed) or arbitrary alphabets fitted by a solver. A wheel cipher sits between those: many **fixed, published** mixed alphabets, used in an order, read off a few rows away. It is the classic US Army/CIA-museum hand device (the M-94, Army 1922–1943, Navy CSP-488), it is "in plain sight" (the alphabets are printed everywhere), and it gives 25 letters per line, a block structure a sculptor could carve. No earlier cycle tested it. Prior: low; the test is cheap and exact, so it is worth closing.

## 2. Model
- Disks: the 25 M-94 alphabets B1…Z25, as text from [jproc.ca](http://www.jproc.ca/crypto/m94.html) and [bribes.org](https://bribes.org/crypto/cryptographe_M94.html), which agree. ([Crypto Museum](https://www.cryptomuseum.com/crypto/usa/m94/index.htm) has two typos: F5 repeats U, Z25 repeats K. Not used.) All 25 checked to be permutations of A–Z.
- Letter *i* is enciphered on disk π(*i* mod 25), and the ciphertext is read *g* rows away (*g* = 1…25), with **a different *g* allowed for every 25-letter line** (the M-94 rule: the operator picks any generatrix per line). Reading up or down is the same set of *g*.
- π is **any** order of the 25 disks. The crib letters give, per column, the set of disks that fit; a bipartite matching then checks that distinct columns can get distinct disks. Exact, no scoring.
- Order A: K4 = transposition(M-94(plaintext)). Undo each of the 165,065 transpositions (cycle 19/22 family: all column orders w ≤ 8, K3-style single/double rotations, inverses, identity), then test.
- Order B: K4 = M-94(transposition(plaintext)). The cribs move with the transposition, so lines and columns change per transposition; offsets are searched line by line with pruning.

## 3. Results ([report](../analysis/m94_report.txt))
| Test | K4 | Shuffled-K4 nulls | Planted controls |
|---|---|---|---|
| Direct (no transposition) | **0** | 0 of 20 | 1/1 found (planted offsets 12, 21, 14) |
| Order A, 165,065 transpositions | **0** | 0 / 0 / 0 (3 nulls) | 2/2 found, each the **only** hit: planted transposition and offsets |
| Order B, 165,065 transpositions | **0** | 1 false hit in 10 nulls (null 1) | 2/2 found (one unique; one among 72 hits, all equivalent re-orderings that move the cribs the same way) |

## 4. Verdict
| Hypothesis | Status |
|---|---|
| M-94, 25 published disks, any disk order, any offset per line, on the copper | **impossible** |
| Same, behind any of 165,065 transpositions (either layer order) | **0 consistent** (order B has a ≈ 1-in-10 per-text false-hit rate, so it is a weaker filter, but K4 had none) |

## 5. Honest limits
- Only the M-94's 25 disks. Jefferson's 36 wheels (alphabets not recorded), Bazeries's 20 keyword disks, the M-138 strip cipher (100 strips, secret) and Sanborn-made disks are **not** tested; a KRYPTOS-keyed disk set would need its own alphabets.
- One disk per position, cycling every 25 letters. A message started mid-cylinder, or a cylinder of fewer disks, is not covered.
- The disk matching is not unique (several disk orders can fit the cribs), so a hit would only be a candidate; there were none.

## Reproduce
```
python3 tools/m94_alphabets.py                 # validates the 25 alphabets
gcc -O2 -o m94_trans tools/m94_trans.c         # order A / direct
gcc -O2 -o m94_trans2 tools/m94_trans2.c       # order B
./m94_trans k4.txt                              # direct
./m94_trans k4.txt perms97.bin                  # order A, about 5 s
./m94_trans2 k4.txt perms97.bin                 # order B, about 5 s
```
`m94.txt` is the 25 alphabets, one per line. `perms97.bin` is the cycle 22 transposition family (int16, 165,065 × 97).
