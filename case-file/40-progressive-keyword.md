# 40 — Progressive keyword key behind a transposition (cycle 41)

**Hypothesis (labelled HYPOTHESIS).** K4 uses a keyword on the KRYPTOS (or straight) tableau, as K1–K2 do, but the
keyword does not simply repeat: every time it comes round again it is shifted by a further *s* letters. This is the
"progressive key" of nineteenth-century manuals (Kasiski describes it; it defeats a plain periodic test because the
key never repeats exactly). Written out, the key at index *i* is

key(i) = k[i mod L] + s · ⌊i / L⌋ (mod 26),

with Vigenère (c = p + key) or Beaufort (c = key − p) on the A–Z or KRYPTOS numbering. Variant Beaufort is
Vigenère with key and step negated, so it is covered. *s* = 0 is the ordinary periodic key, kept as a sanity check.
The coverage table listed "other step rules (keyword-driven steps)" as open after cycle 40; this is the most
hand-friendly of them.

**Layers.** The substitution sits on either side of each of the 165,065 transpositions used since cycle 19
(identity included; all column orders w ≤ 8, keyword columnar, routes, K3-style single/double rotations,
inverses). Model A: the index is the plaintext position (substitute, then transpose). Model B: the index is the carved
position (transpose, then substitute).

**Test (exact).** For each transposition, numbering, model, mode, L = 1–26 and s = 0–25, each of the 24 crib letters
fixes one value of k[i mod L]; the configuration is consistent only if every class agrees. For L ≤ 13 a consistent
configuration fixes the whole key in model A; in model B a few classes can stay unfixed, and those letters are filled
by quadgram hill-climbing (reported as `free=`). Every consistent configuration with L ≤ 13 is decrypted and scored
with English quadgrams. For L 14–26 the key has too many free letters; consistent configurations are only counted and
compared with shuffled nulls. 892,671,520 exact tests per text.

**Controls.** 20 shuffled-K4 nulls (same letters, random order). 10 planted controls: an English passage from
Carter (K3's source) with EASTNORTHEAST and BERLINCLOCK at the official positions, enciphered with a random
transposition, numbering, model, mode, L (1–13), s (1–25) and random key letters.

## Results
| Text | L ≤ 13, s = 0 | L ≤ 13, s > 0 | L 14–20, s > 0 | L 21–26, s > 0 (overfit) |
|---|---|---|---|---|
| K4 | 0 | **0** | **0** | 6 / 89 / 2,358 / 8,959 / 47,037 / 719,494 |
| 20 shuffled nulls | 0 (all) | 0 (all) | 0 in 16 nulls, 1 (at L = 20) in 4 | 0–29 / 74–151 / 2,301–2,630 / 8,897–9,033 / 45,822–48,152 / 688,586–741,125 |

- **10/10 planted controls recovered and ranked first** (quadgram −4.03 to −4.50; L 1–13, both models, both
  numberings, both modes, including three model-B cases with one free class that the first draft of the solver
  missed — see audit below).
- K4's L 21–26 counts sit inside the null ranges at every L: **no signal**, as expected for that much freedom.
- Full output: [`analysis/cycle41_progkw.txt`](../analysis/cycle41_progkw.txt). Code:
  [`tools/progkw.c`](../tools/progkw.c), [`tools/progkw_controls.py`](../tools/progkw_controls.py),
  [`tools/run_cycle41.sh`](../tools/run_cycle41.sh).

## Verdict
**Negative.** A progressive keyword key of length ≤ 20 with any step, on the A–Z or KRYPTOS tableau, Vigenère or
Beaufort, directly on the copper or on either side of any of the 165,065 transpositions, cannot produce the official
cribs. Lengths 21–26 are untestable by this method (K4 inside null range).

## Audit notes
- **Own bug, caught by controls.** The first run assumed every key class is pinned by EASTNORTHEAST. That is true in
  model A but not in model B, where the transposition scatters the crib positions; 3 of 10 planted controls were
  missed. The solver now fills unfixed classes by hill-climbing, and all 10 are recovered. K4 had 0 consistent
  configurations at L ≤ 13 in both runs, so the verdict did not change, but the first run's control table would have
  been wrong.
- **Independent re-check of cycle 13.** The *s* = 0 slice is the ordinary periodic key on a fixed tableau behind the
  same transpositions. It gives 0 consistent configurations for K4 at every L ≤ 20 (cycle 13 tested p ≤ 16), so
  cycle 13's exclusion reproduces with different code and extends to p ≤ 20 for the AZ/KA tableaux.
