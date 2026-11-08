# Cycle 134 tools — phrase-primer autokey behind the bank

`qphrase.c` extends cycle 133 from single vocabulary primers of length 3–10
to phrase primers: leftover vocabulary words of length 11–14, two joined
vocabulary words, and three themed words.

Cycle 133's hash filter needs n = 24 − 2L determined crib letters and is
underpowered for L ≥ 11. Here each of the 330,130 permutations is known as an
intermediate text, so the 24 official cribs *derive* the primer along the
autokey chains. A derived primer (possibly partial) is looked up in the phrase
set. Most settings fail the first extra chain check (~25/26) and never reach
the dictionary.

- **Q** — Quagmire III, keyed alphabet from any of 10,056 vocabulary words.
  PT-fed autokey for L 11–22 (3 directions) and CT-fed autokey for L 22–28
  (the primer now overlaps the first crib at index 21).
- **S** — repeating themed keyword (97 words) stacked with the same autokey,
  either order, on the A–Z or KRYPTOS tableau, 3 × 3 directions (KA and AK).

`qphrase CT words.txt themed.txt perms.bin label mode lo hi`
- `mode=Q` — rows lo..hi of `words.txt` as W
- `mode=S` — rows lo..hi of `themed.txt` as the repeating keyword

`plant.py` — 4 independent Python-encrypted controls and 2 shuffled nulls
(seeds 13401–13402). `run_cycle134.sh` — K4 + two nulls, 8-way parallel.

Lists come from `tools/cycle131/mklists.py` (10,056 words, 97 themed).
