# Case file 64 — Four-square with arbitrary cipher squares (cycle 66)

**Why this test.** The coverage table had never opened Delastelle's **four-square** (or any Wheatstone-type
multi-square digraphic). Case file 20 ruled out every 5×5-square cipher as K4's last layer because K4 uses all 26
letters, but two square shapes hold exactly 26 letters — **2×13 and 13×2** — and a 6×6 square holds A–Z plus 0–9. Those
were never tested. Four-square is also the textbook "simple thing in plain sight" for a 1988 artist with a cipher
manual: two plain squares in a fixed order, two scrambled ones. This is a new family, so it satisfies the diversity rule.

**Model.** Plaintext pairs (a, b) from a fixed pair offset (pairs start at position 1 or 2, so a leading or trailing
odd letter passes through). a sits at (r_a, c_a) and b at (r_b, c_b) in the plain square P; the output is
x = C1[r_a][c_b], y = C2[r_b][c_a]. P is one of 264 themed alphabets (A–Z, KRYPTOS-keyed, Z–A and the repo's themed
set) written into the shape row by row; for 6×6 the digits are either appended (A–Z then 0–9) or interleaved in the
ADFGVX style (A1B2…J0). **C1 and C2 are arbitrary** — any permutation of the cells.

**Exact test.** Each crib pair fixes one cell of C1 and one of C2. The configuration survives only if those
assignments are a partial injection (one letter per cell, one cell per letter) in each square. Full pairs inside the
cribs: 11 at either offset (6 in EASTNORTHEAST, 5 in BERLINCLOCK). Layers: (i) direct; (ii) order A, four-square then
one of the 96,630 cycle-12 transpositions (I[j] = CT[p[j]]); (iii) order B, transposition then four-square (the known
plaintext letters move with the permutation, so fewer full pairs survive). Perm entries for an omitted slot break their
pair. Total ≈ 1.6 × 10⁸ configurations per text per shape.

**Controls and nulls.** 12 planted controls (4 shapes × 3 layers) built from Moby-Dick text with the cribs placed at the
official positions, random cipher squares, random themed plain square, random offset and permutation. 25 shuffled-K4
nulls (seeds 6600–6624).

## Results
| Layer | K4 | 25 shuffled nulls | Planted controls |
|---|---|---|---|
| Direct, all 4 shapes, 264 alphabets, both offsets | **0 configurations** | 0 for every null | 4/4 found at their own alphabet and offset |
| Order A (four-square → transposition), 11 pairs | 13,134 / 3,408 / 3,795 / 20,654 survivors (2×13 / 13×2 / 6×6 / 6×6-ADFGVX) | ranges 1,398–25,015 / 815–6,974 / 717–9,551 / 3,290–37,267; K4 ranks 6, 3, 5, 3 of 26 | 4/4 found at their own permutation, alphabet and offset |
| Order B (transposition → four-square) | max 10–11 full pairs | max 11 for nulls | 0/4 reach the print threshold (n ≥ 10): **blind** |

**Reading.** (1) **Direct four-square on 2×13, 13×2 or 6×6 with a themed plain square is excluded exactly** — no
choice of cipher squares fits the 24 crib letters, while every planted control is found. (2) Behind a transposition
(order A) the 11 crib pairs are too weak: thousands of configurations survive for K4 and every null alike. K4 sits in
the upper part of the null range in all four shapes but inside it (best rank 3 of 26), so this is not evidence.
A cheap side check — decoding the extra non-crib pairs whose two cipher letters were already placed and scoring their
bigrams — does **not** separate controls from nulls (controls' own configurations score −1.94 to −2.23 vs null bests
−1.85 to −2.49), so it was not used to rank anything. (3) Order B is blind: after a transposition too few crib pairs
stay adjacent.

**Verdict.** Negative where the test has power (direct). Behind transpositions the family is crib-underdetermined;
closing it needs a full four-square hill-climb per survivor (a standard, well-behaved attack on ~100 letters), gated by
the planted order-A controls. The 6×6 shapes are also unlikely on their face: a 6×6 four-square emits digits unless
the cipher squares hide all ten digits in cells letter pairs never reach, which the appended layout allows only
partly.

**Files.** `tools/c66.c` (exact checker), `tools/gen66.py`, `tools/mknulls66.py`, `tools/summarize66.py`,
`tools/run_cycle66.sh`; `data/cycle66/` (controls, nulls, `results66.txt`, per-run digest `out66_digest.txt`, bigram table; full 14 MB raw outputs kept on the investigation machine).
