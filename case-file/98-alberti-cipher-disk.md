# Case file 98: the Alberti cipher disk (a key that holds, then turns)

**Cycle 106, 2026-11-05.** Code and raw output: [tools/cycle106](../tools/cycle106/).

## Why this family
Every keyed family tested so far changes the key at every letter, on a fixed beat (periodic, progressive) or from the text itself (autokey, running key). Alberti's 1467 cipher disk, the first polyalphabetic cipher, works differently: the inner ring stays put for a stretch, usually a few words, then the encipherer turns it to a new setting at a moment he chooses (or at an index letter he drops into the plaintext). Between turns it is one plain monoalphabetic substitution. That fits the house style (one mixed alphabet on a disk or tableau, a simple trick in plain sight) and cycle 104's observation that "something keeps the beat, then changes its step between NORTHEAST and BERLIN". The repository had no test of a piecewise-constant key with irregular turns. Cycle 77's row key is the special case with fixed-length stretches; cycle 56's interrupted key restarts a keyword, it does not hold one setting.

## Model
Outer ring O (plaintext order) and inner ring I (cipher order). With setting s_j, plaintext letter p is enciphered as the inner letter at position O(p) + s_j (Vigenère sense) or s_j − O(p) (reversed ring, Beaufort sense). The setting is constant between turns, and turns can fall anywhere. **Statistic:** E = the number of adjacent crib pairs (12 inside EASTNORTHEAST, 10 inside BERLINCLOCK) that share a setting, so E = 22 − (turns inside the crib spans). With a turn every few words, a true configuration gives E ≈ 16–20. Random letters give E ≈ 0–2.

## Tests
| Test | Space | K4 | Shuffled nulls | Planted controls |
|---|---|---|---|---|
| Direct, tableau rings (`alberti.c`) | 86,731 keyed alphabets × 6 ring modes (Quagmire III / I / II shapes × Vig/Beau) | best **E = 7** | 5 nulls: 6–8 | direct KRYPTOS-ring control E = 19 (true value 19) found |
| Model A (disk, then transposition) (`alberti.c`) | 165,065 transpositions (cycle 19 family incl. identity) × 264 themed alphabets × 6 modes = 2.6 × 10⁸ | best **E = 9** (3 configs, i.e. 13 turns in 24 letters: not a disk) | 5 nulls: 9, 9, 9, 9, 10 | 4/4 recovered at the true permutation with the true E (19, 17, 19, 18) |
| Direct, **both rings arbitrary** (`alberti_maxsat.py`, RC2 MaxSAT, optimum proven) | any outer × any inner order (Beaufort included) | **min 5 turns** (E_max 17) | 12 of 20 finished in 200 s: 3–6 turns (8 of 12 need ≤ 4); 8 timed out | control: 2 turns found (true 3) |

Audit row (`audit104.py`): cycle 104's claim that a fully general periodic substitution (free alphabet per phase) is inconsistent at p ≤ 7 and at 9, 10, 14, 15, 17, 21, 25, 34, 42, 43, 45 was **reproduced exactly** by an independent partial-bijection check (p 1–48). **PASS.**

## Verdict
- **Tableau-ring Alberti disk (KRYPTOS or any of 86,731 keyed alphabets, direct) and Alberti disk behind the 165k transposition family (264 themed alphabets): excluded.** A real disk would sit around E ≈ 16–20. K4 tops out at 7 (direct) or 9 (behind transpositions), the same as the shuffled nulls, while every planted control came back at its true value.
- **Arbitrary rings, direct:** the cribs cannot tell K4 from noise. Shuffled texts fit just as well or better. One proven fact remains: **if K4 is a direct Alberti disk, the disk turns at least 5 times inside the 24 crib letters** (a stretch of under 5 letters on average). That is not how Alberti used it (a turn every few words), so the classic usage is effectively excluded too. A frequently turned disk is just a general polyalphabetic and stays crib-underdetermined.
- No full 97-letter decryption was produced or claimed.

## Still open
Arbitrary rings behind transpositions (needs per-permutation MaxSAT, plus English scoring); disk turns triggered by a carved index letter (e.g. W) with a fixed step, which would be a strict special case worth one quick exact run; disk + K3-style grid on the 98-cell `?` block.
