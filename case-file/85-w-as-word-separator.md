# Case file 85 — W as a word separator, key restarting per block (cycle 89)

**Idea.** Cycle 88 ([case file 84](84-w-as-null.md)) dropped the Ws and let one periodic key run through the 92 letters.
The other natural reading of a separator is that each block between Ws is enciphered on its own, with the key
starting again at the block's first letter (as a person enciphering word by word would do). The cribs sit wholly inside
blocks: EASTNORTHEAST at offsets 0–12 of block 2, BERLINCLOCK at offsets 4–14 of block 5, so one shared key is exactly
testable.

**A consequence worth stating.** If W is reserved as a separator, the cipher letters inside the blocks never produce W.
With a 26-letter cipher alphabet the chance of that by accident is about (25/26)⁹² ≈ 0.027, so the reading favours a
25-letter, W-less cipher alphabet. Both were tested.

**Tests (exact; `tools/cycle89/restart.py`, numbers in `data/cycle89/results.txt`).** Periodic key p 1–20, Vigenère and
Beaufort, restart at every block:
1. plaintext and cipher alphabet each A–Z or KRYPTOS (mod 26);
2. the same alphabets with W removed (mod 25);
3. Quagmire III over the 86,731 themed keyed alphabets (mod 26);
4. the same themed alphabets with W removed (mod 25).

**Results.** K4: **0 consistent keys in all four tests.** Shuffled nulls (non-W letters shuffled, Ws kept in place):
0 in every test. Planted controls (one per test, built under the restart model, cribs intact): **4/4 recovered** with
full readable plaintext.

**Verdict.** W as a separator with a short periodic key restarting at each block is **excluded** for p ≤ 20 over these
alphabets. **Negative.**

**Still open:** a different key per block (untestable from the cribs alone, since each crib lies in one block); a
running key restarting at each block; the separator reading combined with a transposition inside each block.
