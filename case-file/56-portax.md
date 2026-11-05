# Case file 56 — Portax (ACA period-pair digraphic on a Porta slide), exact (cycle 58)

**Why this family.** Owed since cycle 57's next-ideas list. Portax is the ACA's digraphic cousin of Porta (cycle 32):
the plaintext is written in lines of p letters, lines are taken in pairs, and each vertical pair (top letter, bottom
letter) is enciphered with the key letter of its column on a four-row slide (A–M over a sliding N–Z row; A C E … Y over
B D F … Z). It is reciprocal, period-based and needs only a keyword: K1–K3-style ingredients, but digraphic and with
pairs p letters apart, which no test in this repo has modelled. Not in the repo's case files or in kryptosbot's
published list (Sept 29, 2026). New family for the coverage table (diversity rule).

## Model (`tools/portax.c`)

Pair (P1, P2) with column shift k (0–12; key letter pair AB = 0 … YZ = 12, all 13 tried per column, so any key and
both slide directions are covered). P1 is located in the upper half (row A–M, or the N–Z row shifted by k), P2 in the
lower half (column c holds letters 2c, 2c+1). Different columns: rectangle swap; same column: both letters move to the
other row of that column. The map is an involution (checked), so decryption = encryption. Letters are alphabet
indices, so the same code runs Portax on any keyed alphabet (a K1/K2-style variant; the ACA standard is A–Z).
97 is odd: trailing letters with no partner in the last line pair are left unconstrained (a crib letter there cannot be
checked). Each column's shift is solved independently and exactly from every crib letter that falls in that column's
pairs; a configuration survives only if every column admits a shift. Periods p = 1–48.

**Layers.** (a) directly on the copper; (b) behind each of the 96,630 cycle-12 transpositions (entries carrying the −1
omitted-letter marker skipped, as noted in cycle 57), in both orders: Portax then transposition, and transposition then
Portax.

**Survivors with almost nothing checked.** At p ≈ 31–37 the transpositions can move most crib letters into the unpaired
tail, so a "survivor" may have 0–3 constrained pairs. Such hits are reported but counted as untestable; a hit is called
**informative** when at least 8 pairs are checked.

## Results (`data/cycle58/`)

| Run | Configs per text | K4 | 5 shuffled nulls | Planted controls |
|---|---|---|---|---|
| A–Z and KRYPTOS alphabets, behind 96,630 transpositions × 2 orders (+ direct), p 1–48 | 17,956,896 | 6 hits, **0 informative** | 6–16 hits, 0 informative | CTL1 (A–Z, SHADOW, p 6, direct), CTL2 (KRYPTOS alphabet, UNDERGRUUND, p 11, direct), CTL3 (LAYER, p 5, behind perm 5000, order 1), CTL4 (PALIMPSEST, p 10, behind perm 20000, order 2): **4/4 recovered** |
| All 86,731 keyed alphabets, direct, p 1–48 | 4,163,088 | **0** | 0 each | CTL1, CTL2 recovered (unique hits) |
| 264 themed alphabets (cycle 12 list) behind 96,630 transpositions × 2 orders, p 1–48 | 2,370,310,272 | 1,915 hits, **1 informative** | 1,927–2,218 hits, 0 informative | CTL5 (r:SHADOW alphabet, BERLIN, p 6, behind perm 40000): **recovered**; CTL5 also shows 2 chance informative hits |

K4's one informative hit (themed alphabet #31, perm 93100, Portax first, p = 37, 10 single-letter checks) decrypts to
`LWFMGXOTDSLGBCPCTVSWMEASTKZDIHUEKRYYY…`: unreadable, and at the chance rate the planted control text shows (2 such
hits). All K4 hit counts sit inside the null range.

**Verdict.** Portax with periods 1–48 is **negative** directly on the copper (any of 86,731 alphabets, any key) and
behind the cycle-12 transposition family (A–Z, KRYPTOS and 264 themed alphabets, any key). Open: other conventions for
the odd 97th letter / short last line pair (e.g. the last partial block split evenly between its two lines), arbitrary
alphabets (SAT), wider transposition families, and Portax as the inner layer of a K3-style grid read.
