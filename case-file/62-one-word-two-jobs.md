# Case file 62 — One word, two jobs (cycle 64)

**Why this test.** The K1–K3 style profile ([case file 10](10-style-profile.md)) says Sanborn's keys are real words and
that he is economical with them: KRYPTOS keys the alphabet *and* the tableau in K1 and K2. Cycle 63's journal asked the
obvious follow-up: what if one English word does two jobs in K4, setting **both** the keyed-columnar column order
(K3's family of trick) **and** the mixed tableau alphabet (K1/K2's trick)? Cycle 52 tested keyed columnar × periodic
key, but only for 1,837 orders from 3,000 frequent words and only on the A–Z/KRYPTOS tableaux. This cycle widens the
vocabulary to a full English word list and ties the alphabet to the same word. It is an extension (cycle 63 opened a
new family), so the diversity rule is respected.

**Model.** For each word W (length 4–20): mixed alphabet A_W = W with repeats removed, then the rest of A–Z; column
order = alphabetical order of W's letters (ties left to right). Plaintext written row by row under W (last row short),
columns read in W order — or the inverse permutation, or **no transposition** — with a periodic key of **any** value
and length L ≤ 22 applied before or after it, Vigenère or Beaufort, on the A_W tableau (Quagmire III style). The A–Z
and KRYPTOS tableaux are run on the same orders for reference. `DOUBLE=1` repeats the same W columnar twice (K3 is a
double transposition, here with one word for both passes). Exact test against the 24 official crib letters
(EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-based), checker identical to cycle 52 (s = 0, i.e. periodic keys only).

**Vocabulary.** The cycle-56 themed + frequent list plus the public [dwyl `words_alpha`](https://github.com/dwyl/english-words)
list (370,105 words), letters only, length 4–20: **367,184 distinct (order, alphabet) entries**. Regenerate with
[`tools/c64_gen.py`](../tools/c64_gen.py) (the 12 MB list is not committed).
Tools: [`tools/c64.c`](../tools/c64.c), [`tools/ctl64.py`](../tools/ctl64.py), [`tools/run_cycle64.sh`](../tools/run_cycle64.sh);
outputs in [`data/cycle64/`](../data/cycle64/). The whole single run (7 texts) takes about 6 s on 8 cores.

## Controls (planted English, cribs at the official positions, searched over the full vocabulary)
| Control | Word (order + alphabet) | Layers | Key | Recovered |
|---|---|---|---|---|
| CTL1 | LANTERN | columnar, key before, Vigenère on A_W | GLOW | yes (L = 4, plus trivial L = 8, 12), −4.09/quadgram |
| CTL2 | UNDERGROUND | inverse columnar, key after, Beaufort on A_W | SHADOWS | yes, only hit |
| CTL3 | PERIMETER | columnar, key after, Vigenère on A_W | EGYPTIAN | yes, only hit |
| CTL4 | LUMINOUS (order only) | inverse, key before, KRYPTOS tableau | KRYPTOS | yes, top hit (other words with LUMINOUS's 8-column order give partial fits) |
| DCTL1 | LANTERN twice | double columnar, inverse, key after, Beaufort on A_W | GLOW | yes (`DOUBLE=1`) |
| DCTL2 | CHAMBER twice | double columnar, key before, Vigenère on A_W | CANDLE | yes (`DOUBLE=1`) |

## Results
| Run | Text | Consistent, L ≤ 13 | Distinct configurations at L = 22 (best quadgram) |
|---|---|---|---|
| single / none | K4 | **0** | 27 (−6.93) |
| single / none | shuffled K4, seed 6400 | 0 | 19 (−6.91) |
| single / none | shuffled K4, seed 6401 | 0 | 14 (−6.97) |
| double (same word twice) | K4 | **0** | 0 |
| double | nulls 6400 / 6401 | 0 / 0 | 1 / 1 lines |

At L 14–21 K4 has one fit each at L = 20 and 21; the nulls have 0 and 2. The L = 22 fits leave only two or three
key letters under-determined and are crib-in-gibberish, e.g. `NKJHAZLZMZJKFAELCIDZP EASTNORTHEAST FOCHNWINDDCRIELCGCIGTWAPRODWX BERLINCLOCK …`
(BOSSILY, −6.93). K4's 27 versus 19 and 14 is within what two nulls can bound; it is not a signal, and the best K4
score equals the nulls'.

## Verdict
**Negative.** No word from a 367,184-entry English vocabulary, used as both the keyed-columnar order and the mixed
tableau alphabet (or as the alphabet alone, or as both passes of a double columnar), admits any periodic key of
length ≤ 21 that fits K4's cribs; the L = 22 fits are at null level and unreadable.

**Still open:** progressive keys (s > 0) on A_W tableaux; key-word alphabets built differently (keyword then rest
starting after the last keyword letter, reversed, KRYPTOS-prefixed); two different words for order and alphabet beyond
cycle 52's list; running keys on A_W tableaux behind the same columnar.
