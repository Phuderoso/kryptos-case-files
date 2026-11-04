# Case file 48 — Bazeries digit-group reversal ("le chiffre à numéro") × substitution

**Cycle 49, 2026-11-04. New family (diversity rule).**

## Idea
Étienne Bazeries's number cipher (1890s) is a hand system in the K1–K3 spirit: pick a number (say 3752), cut the text
into groups of 3, 7, 5, 2, 3, 7, … letters, write each group backwards, and put a simple substitution on top (Bazeries
used an alphabet keyed by the number written out in words). The key is a single memorable number, the transposition is
"reverse the pieces", and the result looks nothing like a columnar or route grid, so none of the repo's 165k
transpositions, rail/AMSCO, Myszkowski or grille families contain it.

## Test (exact)
- Transposition: digit keys of length 1–8 over digits 1–9 (zeros dropped, as Bazeries did), groups cycled from the
  first letter, each group reversed; optionally the whole text reversed as well. 48.4M keys × 2 = **96,855,120
  permutations** (with aliases, since cribs only see some group boundaries).
- Substitution, each checked against the 24 crib letters at the official positions (21–33, 63–73):
  - **arbitrary monoalphabetic** (covers Bazeries's spelled-number alphabet and any keyword alphabet): one-to-one check;
  - **periodic Vigenère / Beaufort** (variant Beaufort is equivalent for consistency), A–Z or KRYPTOS tableau,
    L 1–14, key applied before or after the reversal.
- Code: [`tools/bazeries.c`](../tools/bazeries.c), controls [`tools/ctl49.py`](../tools/ctl49.py), run
  [`tools/run_cycle49.sh`](../tools/run_cycle49.sh). Results in [`data/cycle49/results.out`](../data/cycle49/results.out).

## Results
| Text | Keys ≤ 7 digits | 8 digits | Hits |
|---|---|---|---|
| **K4** | 10.76M perms | 86.09M perms | **0 mono, 0 periodic (any L 1–14, any tableau/mode/order)** |
| 3 shuffled-K4 nulls | 10.76M each | — | 0 |
| Planted: mono, key 3752 | | | recovered (true key first; 10 aliases) |
| Planted: mono, key 61834 + whole reversal | | | recovered |
| Planted: KA Vigenère after, SHADOW, key 2864 | | | recovered, key fragment SHADOW |
| Planted: A–Z Beaufort before, PALIMPSEST, key 957 | | | recovered, key fragment PALIMPSEST |
| Planted: KA Vigenère before, ABSCISSA, key 4931726 + reversal | | | recovered, key fragment ABSCISSA |

**Verdict: negative.** No Bazeries number key of up to 8 digits, with a monoalphabetic or short periodic substitution,
fits K4's cribs. 5/5 planted controls recovered; nulls 0.

## Limits / still open
- Numbers with 9+ digits, or digits read as two-digit group sizes (10–99).
- Groups read in another order (e.g. columns of a grid of reversed groups), or reversal combined with a running key.
- Periodic keys L ≥ 15 (cribs become weak there; would need English scoring).
