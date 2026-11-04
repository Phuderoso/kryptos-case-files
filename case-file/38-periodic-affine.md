# Case file 38 — Periodic affine substitution, with and without a transposition

**Cycle 39, 2026-11-04.** Status: **negative** (periods 1–13 fully tested; 14–26 have no detection power).

## Why
The repo's coverage had no affine family at all. K1–K3 only ever add a key letter (Vigenère on a keyed tableau),
but a hand cipher that *multiplies* as well as shifts (c = a·x + b mod 26) is the simplest step beyond that and
was never excluded: a = 1 everywhere is ordinary Vigenère, so this family strictly contains the periodic tests of
cycles 1, 13 and 24 for a fixed numbering. This cycle was chosen under the diversity rule (cycles 37–38 were both
"hex inside hex" variants).

## Model (`tools/affine.c`)
- Letters numbered A–Z (A=0) or by the KRYPTOS alphabet (K=0).
- Each position class r = index mod L (L = 1–26) has its own affine map c = a_r·x + b_r, a_r one of the 12 units
  mod 26, b_r any of 26 — 312 maps per class, chosen independently (no keyword needed).
- Model A: affine at plaintext index, then transposition (`carved[P[i]] = s[i]`). Model B: transposition, then
  affine at carved index. Same conventions as `tools/vernam.c`.
- 165,065 transpositions (cycle 19's family plus identity) × 2 numberings × 2 orders × 26 periods.
- **Exact step:** every class's maps must agree with all of its crib letters. **Scoring step:** whenever every
  class carries a crib letter, or L ≤ 13 (classes with no crib letter then range over all 312 maps), the remaining
  choice of maps is made by coordinate ascent on English quadgrams (4 restarts) and the full 97-letter
  decryption is scored. Lines scoring above −5.0 are printed.

## Results (`analysis/cycle39_affine.txt`)
| text | crib-consistent configs, L 1–13 | best quadgram, L 1–13 | best quadgram, L 14–26 | lines > −5.0 |
|---|---|---|---|---|
| K4 | 35 | −6.55 | −4.91 | 2 |
| 10 shuffled K4 nulls | 34–167 | −6.44 to −6.74 | −4.80 to −4.95 | 4–14 |
| 9 planted controls (L 4–13, both numberings, 6 model A, 3 model B) | — | planted plaintext ranked **first 9/9** | — | — |

English plaintext of this length scores about −4.1 with the same quadgram table.

- **L 1–13: negative.** K4's 35 crib-consistent configurations decrypt to noise (−6.55), squarely inside the null
  range, while every planted control comes out on top with its exact plaintext.
- **L 14–26: no power.** With so few crib letters per class, coordinate ascent over free maps overfits any text to
  about −4.9 (K4's two "best" lines at L = 24 are word salad with the cribs pasted in). K4 is indistinguishable from
  shuffled nulls here; this range is *not* excluded, only untestable by this method.
- Audit inside the cycle: the first run left model-B controls with a crib-free class unscored (control 37 missed);
  fixed by letting crib-free classes range over all 312 maps for L ≤ 13, after which 9/9 controls were recovered.

## Limits
Transpositions limited to cycle 19's family; one affine map per class (no autokey or progressive multiplier);
numberings only A–Z and KRYPTOS; L ≥ 14 untestable by quadgram ascent.

## Reproduce
`cd tools && python3 export_perms.py && sh run_cycle39.sh` (about 1 minute on 8 cores).
