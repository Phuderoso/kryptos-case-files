# 192 — The W-rectangle and its half-turn: exact counts, a shuffled-K4 null, and what it can and cannot mean (cycle 205)

> *A stranger left a chalk drawing on the wall: four W's at the corners of a box, the cribs running along its edges. Before
> anyone builds a key on it, count how often chalk lands like that by itself, and ask what a key would have to do to draw it.*

**IDEAS:** I-259 (via I-264). **Status:** descriptive / exploratory, **not pre-registered** (the definitions are the external author's,
fixed before this cycle; the null design was written before any null number was read, but no PREREG commit was made). **Code:**
[`wrect.c`](../tools/cycle205/wrect.c) (exact enumeration), [`wnull.c`](../tools/cycle205/wnull.c) (null), [`run_w259.sh`](../tools/cycle205/run_w259.sh).
**Results:** [`wrect_out.txt`](../tools/cycle205/wrect_out.txt), [`wnull_out.txt`](../tools/cycle205/wnull_out.txt),
[`results205.json`](../tools/cycle205/results205.json). Heavy compute ≈ 2.5 min (8 workers, one owned process group, `setsid` + `timeout`).

**Source** `[external, sourced]`: glthr, *Kryptos K4: The W-Rectangle and Its Half-Turn*, [glthr.com, 2026-11-11](https://glthr.com/kryptos-k4-a-rectangle-hidden-in-the-cipher).
Claim: in rows of 19, four of K4's five W's (1-idx 21, 37, 59, 75) sit one cell in from the corners of the 5 × 19 grid, the fifth (49)
one cell right of the centre; EASTNORTHEAST starts right after a W, BERLINCLOCK ends right before one; the half-turn p → 96 − p
swaps the 2024 alternating W-groups (20 | 15 | 11 | 9 | 15 | 22 letters, equal frequency shapes) except ZZ and the trailing AR.

## 1. Exact reproduction of the published placement counts
All 5-subsets a < b < c < d < e of 1..97 (64,446,024). Definitions (written to match the post, then checked against it):
EQ = alternating groups equal in size (a + c + e − b − d = 49); RECT = some width w ∈ 3..48 puts a, b on one row and d, e on another
with col a = col d, col b = col e; SYM = RECT and centred on the w × ⌊97/w⌋ grid (a + e = R·w + 1); INSET = SYM with a at row 2, col 2.

| pattern | this repo | glthr | |
|---|---|---|---|
| all placements | 64,446,024 | 64,446,024 | match |
| EQ | 1,272,384 | 1,272,384 | match |
| SYM ("W rectangle on opposite cells") | 26,734 | 26,734 | match |
| SYM + centre mark | 1,815 | 1,754 | **differs** (my "within one cell of the centre, same row" is looser; their exact definition is not stated) |
| SYM + INSET | 775 | 775 | match |
| EQ & SYM | 650 | 650 | match |

So the published exact counts are independently reproduced except the centre-mark line, which is a definitional gap, not an error claim.

## 2. Null: permutations of K4 (letter counts kept) and iid-uniform texts
For each text, for every letter with ≥ 4 occurrences, every 4-subset of its positions is tested for SYM (all widths 3..48), and every
other occurrence of the same letter as a centre mark; "eq" and "shape" apply only to letters with exactly 5 occurrences (as W in K4):
alternating groups of 46 / 46 with identical frequency-shape histograms. **Positive control:** K4 itself raises every flag (all 6 = 1).
**Cross-check of definitions:** on iid-uniform texts my rates match the post's 119M-text simulation (any symmetric rectangle 4.62 % vs 4.6 %;
inset + centre 0.0094 % vs 0.010 %).

| event (some letter …) | shuffled K4, n = 200,000,000 | iid uniform, n = 40,000,000 |
|---|---|---|
| SYM rectangle, any width | 3.28 % | 4.62 % |
| SYM + INSET + centre mark (the K4 arrangement) | 5.09 × 10⁻⁵ (10,183) | 9.39 × 10⁻⁵ (3,756) |
| 5-occurrence letter: EQ & SYM | 3.05 × 10⁻⁵ | 3.80 × 10⁻⁵ |
| EQ & SYM & equal frequency shapes | 1.95 × 10⁻⁷ (39) | 1.5 × 10⁻⁷ (6) |
| INSET + centre & EQ | 9.0 × 10⁻⁸ (18) | 5 × 10⁻⁸ (2) |
| **INSET + centre & EQ & shapes (all of K4's W pattern)** | **0** (95 % upper 1.5 × 10⁻⁸) | 0 (upper 7.5 × 10⁻⁸) |

(The crib-edge condition was not added: the cribs' positions are fixed, so given INSET in the 5 × 19 grid the edges are determined; it
adds no independent rarity beyond the 5 × 19 choice, as the post's own footnote 3 notes for the half-turn.)

**Reading.** Under the stated definitions the full W pattern is rarer than about 1 in 67 million permutations of K4. That is **not a
p-value for "coincidence"**: the definitions were chosen after the pattern was seen (in 2016 and 2024 for the groups, 2026 for the
rectangle), and there is no count of the other geometric patterns that would have been reported had they appeared. A cipher's output
is also not a random permutation. Treat it as: *the W placement is a real, reproducible, unusual structure under two simple nulls;
its look-elsewhere correction is unknown.* Label: `UNUSUAL (selection-uncorrected)`; no claim of intent.

## 3. What a key would need to produce it (analytic, exact)
- **Half-turn as a transposition layer adds nothing for periodic keys.** Reading the 95-cell grid by p → 96 − p is a reversal of
  positions 1..95 (AR untouched; no crib touches 96–97). A key periodic in the read-out index j = 96 − p is periodic with the same
  period in p (class j mod L ↔ class (96 − p) mod L, a bijection of residue classes), so every direct periodic exclusion
  (Vigenère / Beaufort / variant, A–Z / KRYPTOS tableaux, cycle 13, and progressive keys, cycle 41) carries over unchanged. Same
  for any per-phase arbitrary-bijection model (case 11's SAT periods): the open/closed period list is identical. `EXACT` (by argument).
- **W = enciphered stop (plaintext X).** Under case 11's free per-phase bijection model this adds nothing for stop letter X: the
  crib plaintext has no X and the crib ciphertext has no W, so X→W never clashes with a crib pair; five equal ciphertext letters
  from five equal plaintext letters only require the five phases (mod P) to agree on X→W, which is free. It **does** bite in
  shared-alphabet models (Quagmire III/IV, single keyed tableau), where X→W fixes the key letter of each W phase → queued as I-266.
  Under a periodic key with a fixed tableau, five equal pairs force equal key letters at positions 21, 37, 49, 59, 75 (mod L);
  they share one residue class only for L ∈ {1, 2} (differences 16, 12, 10, 16), so for other L the key must repeat a letter by design.
- **The "TL" pairs** (opposite crib cells 25/71 and 29/67, ciphertext VZ and RV, both shifted −4) are a single observation among many
  comparisons in the post; not tested here.

## Limits
Not pre-registered; definitions inherited from the post (one line differs); nulls are permutations and iid texts, not cipher outputs;
no look-elsewhere correction; the "K4-like groups" of the post allow other letter counts, here only exactly-5-occurrence letters;
nothing here decrypts anything. **No solution.**
