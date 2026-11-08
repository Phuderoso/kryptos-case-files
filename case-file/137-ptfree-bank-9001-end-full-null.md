# Case file 137 — ptfree behind the bank, words 9001–10,057, with a full-bank null baseline (cycle 149)

**What.** The last slice of the cycle 139/140/145/147 sweep: plaintext autokey with a free plain alphabet (`tools/cycle139/ptfree.c`, unchanged), behind all 165,065 transpositions both directions and both layer orders, keyed by vocabulary words 9001–10,057 of `all.txt`. With this the whole 10,057-word list is covered.

**Audit of earlier baselines.** Cycles 145 and 147 compared K4 against nulls run on only every 10th bank entry and scaled up, which was noisy. This cycle ran both shuffled nulls on the **full** bank for words 9001–9528, the same ground as K4.

**Result.** K4: 1.22 × 10^10 tests, 3 distinct survivors, all at the 5-check floor (LAUDABLE, BROUGHAM, TEMPERATE), all inside words 9001–9528. Nulls on that slice: 1 and 3 survivors. No English. K4 is indistinguishable from shuffled ciphertext, which also confirms the scaled-up baselines of cycles 145/147 were about right: the 5–6-check survivors of the earlier slices are chance.

**Closed.** ptfree behind the 165k bank for all.txt alphabets. **Open.** Keyword-mixed alphabets from phrases rather than single words; ptfree behind non-bank transpositions.
