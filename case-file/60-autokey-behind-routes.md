# Case file 60 — Autokey behind spiral and diagonal routes

> *The snail and the slant had only been asked one question: a key that repeats. Tonight I asked the other one —
> a key that feeds on its own words.*

## 1. Why this
Cycle 61 added 6,070 spiral/diagonal route permutations and tested them only against periodic Quagmire III.
Its "next ideas" list put autokey behind those routes first: the cycle-60 exact autokey solver already exists, the
compute is seconds, and autokey is the one keyed family kryptosbot (Sep 2026) explicitly says is *not* ruled out once
a rearrangement layer is added. This is an extension cycle (cycle 61 was the diversity cycle).

## 2. Model
- **Permutations:** `route_perm.bin` from `tools/route_gen61.py` (6,070 spiral/diagonal routes, w 2–48, 3 fills,
  each route and its inverse).
- **Autokey:** CT-fed and PT-fed, Vigenère / Beaufort / variant in alphabet-index space, lags L = 1–96, primer free
  (untested). Model A: PT → autokey → route → carved. Model B: PT → route → autokey → carved.
- **Alphabets:** 264 themed keyword alphabets (`data/tw_alpha.bin`, first 264; includes A–Z and KRYPTOS).
- **Test:** exact, `tools/autokey_exact60.c` (cycle 60): every crib pair the model links must satisfy the cipher
  equation; n = number of linked constraints. Reported hits are configurations where all n hold.

## 3. Controls and nulls
- 4 planted controls (`data/cycle62/controls.txt`, generator `tools/autokey_gen62.py`, seed 62): a K3-flavoured
  plaintext with both cribs in place, through random route permutations, one per model × feed.
  - A/CT vig L7 (route 4712): **recovered**, n = 24, full decryption reads the planted text.
  - A/PT beau L4 (route 1417): **recovered**, n = 16.
  - B/CT var L11 (route 533): **recovered**, n = 17, partial decryption reads the planted text.
  - B/PT vig L2 (route 1950): **recovered but weak**, n = 6 — the same n a null reaches by chance. B/PT behind a
    route links few crib pairs, so this cell is effectively blind (as in cycle 60).
- 3 shuffled-K4 nulls from cycle 61 (`data/cycle61/null*.txt`).

## 4. Result
| Text | max fully consistent n (any model/feed/mode/L/alphabet/route) |
|---|---|
| K4 | 5 (A/CT and B/PT) |
| null0 | 5 |
| null1 | 6 |
| null2 | 5 |

Hit histograms match the nulls cell by cell (e.g. A/CT n4: K4 15, null0 9; B/PT n4: K4 64, null0 50). No K4
configuration satisfies ≥ 6 linked constraints; true planted keys reach 16–24 in the testable cells. Raw output:
`data/cycle62/results62.txt`; run script `tools/run_cycle62.sh`.

**Negative** for autokey (CT- or PT-fed, Vig/Beau/variant, L 1–96, 264 themed alphabets) behind spiral and diagonal
routes, in the cells where crib linkage gives power (A/CT, A/PT, B/CT). B/PT behind routes stays untested in
practice, and alphabets beyond the 264 themed ones are not covered.

## 5. What's left
- Running keys (carved texts, Carter vol. I) behind the routes, quadgram-scored with shuffled baselines.
- Routes over the *carved* ragged rows of the right panel (row lengths from a text transcription).
- Double route (spiral then keyword columnar): K3's "two simple moves".
