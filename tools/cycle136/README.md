# Cycle 136 tools — transposition-first autokey, vocabulary Quagmire III alphabets

`akcarve.c` tests CT-fed and PT-fed autokey against every vocabulary-keyed
Quagmire III alphabet (10,056 words, the K1/K2 construction: unique letters
then A–Z) on both sides of the 165,065-entry bank (330,130 permutations
counting inverses).

The new index is **transposition first, key at the carved position**: after the
letters are moved, an autokey of lag L is applied at the carved index. Any
primer of that length is tested — the 24 official cribs either set a primer
letter or constrain the autokey recurrence (cycle 19 / 22 did this for the
A–Z/KRYPTOS shift tableaux; cycles 133–134 did vocabulary alphabets only as
model Q, and only for dictionary / phrase primers). The plaintext-index order
(key at the original position, then transpose) is run on the same alphabets,
now for *any* primer rather than a listed word or phrase.

- **PT** — plaintext-fed autokey: `K[j] = primer[j]` if `j < L` else the
  previous plaintext letter of the autokey layer.
- **CT** — ciphertext-fed autokey: `K[j] = primer[j]` if `j < L` else the
  previous ciphertext letter of the autokey layer.
- Modes: Vigenère, Beaufort and variant Beaufort (the three are distinct:
  the feedback letter is constrained, so variant is not the dual of
  Vigenère). Lags 1–16 (the same cutoff as cycles 13, 120 and 135: for
  L ≤ 16 the 24 cribs always give at least eight extra constraints). A hit
  needs at least 6 extra crib constraints and is re-checked against all 24
  official crib letters.

`akcarve CT words.txt perms.bin label lo hi [LMAX]`

`plant.py` — 4 independent Python-encrypted controls and 2 shuffled nulls
(seeds 13601–13602). `run_cycle136.sh` — K4, then two nulls, 8-way parallel
per text (K4 is a checkpoint before the nulls).

Lists come from `tools/cycle131/mklists.py` (10,056 words).
