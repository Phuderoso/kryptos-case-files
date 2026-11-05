# Case file 94: polyalphabetic homophonic behind transpositions, whole-text check

Cycle 102 finishes the job [case file 93](93-polyalphabetic-homophonic.md) left open. Cycle 101 found that a periodic shift key (length 1–3) plus any many-to-one map, behind the 340,256-permutation bank, leaves crib-consistent survivors on K4 at the same rate as on shuffled ciphertexts. The cribs can't separate them, so this cycle reads the whole text.

## Method
- Re-ran the cycle-101 solver with no print cap on the two big banks (`perms97`, `dec_perm`, L = 3), and kept the complete small-bank lists from cycle 101. K4: **1,389** distinct survivors (L 2–3, all four banks); null 1: 1,637; null 2: 3,766.
- For each survivor: key and transposition fixed, the map f fixed at every crib-forced entry, and the remaining (free) entries of f chosen by hill-climbing on English quadgrams, 30 random restarts. Cribs stay hard. Code: [`tools/cycle102/polyanneal.c`](../tools/cycle102/polyanneal.c).
- Planted controls: the five cycle-101 controls (English plaintext "WE DUG THROUGH THE RUBBLE ... BERLIN CLOCK TOWER AS THE SUN WENT DOWN"), each run at its true configuration and on every false survivor.

## Results
| Text | Survivors annealed | Best quadgram score | Median | Readable? |
|---|---|---|---|---|
| K4 | 1,389 | −5.10 | −5.82 | no (best: `ERRONECNTRARTSRATARSB EASTNORTHEAST NTSEENEATELST...`) |
| Shuffled null 1 | 1,637 | −5.18 | −5.87 | no |
| Shuffled null 2 | 3,766 | −5.03 | −6.33 | no |
| Planted controls (5) | true config | −3.98 to −4.21 | | **yes, 5/5** (d3 off by one letter, RUMBLE for RUBBLE; the others read with a few wrong homophone guesses) |

Most K4 survivors leave only 3–8 cipher values free, so the cribs nearly fix the whole text, and what they fix is gibberish. K4's best sits between the two nulls.

**Reading.** Polyalphabetic homophonic substitution (periodic key L ≤ 3, any many-to-one map, A–Z or KRYPTOS order, shift before or after the map) behind the 340,256 bank permutations is **excluded**: every crib-consistent configuration was read and none is English, while the same check reads all five planted controls.

Side note from the controls: cycle 101's planted keys for b1 and d2 were printed in letter form, but the solver normalises the key to start at 0 in alphabet-index form. The true configurations do pass once the key is written the solver's way, so the cycle-101 control claim stands.

## Still open
- Key lengths L ≥ 4 behind transpositions (cribs lose power fast: needs a scoring-first search).
- Transpositions outside the bank, especially Zodiac-340-style diagonal reading at width 21 (Bean 2024).
