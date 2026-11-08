# Case file 138 — Zig-zag autokey: direction flips letter by letter (cycle 150)

**Idea.** Sanborn used one tableau for K1–K2 but the direction of use is a free choice for an encipherer working by hand. An autokey where the clerk alternates Vigenère and Beaufort (or variant) on successive letters is a simple layered twist that defeats the standard autokey tests in the repo, since those all assume one fixed form. Cycle 146 tested per-phase direction for **periodic** keys; this extends it to **autokey** keys.

**Model.** c_j = s + a·p_j + b·f_j (mod 26) with (a,b) = (1,1) Vigenère, (−1,1) Beaufort, (1,−1) variant; the form follows a fixed cycle of length 2 or 3 (36 cycles, the 3 uniform ones being ordinary autokey). Feed f is the ciphertext or the plaintext L letters back (L 1–96). A–Z and KRYPTOS numbering. Direct and behind 165,065 transpositions, both directions, both layer orders.

**Method.** Exact: with a ciphertext feed every crib letter (24 of them for L ≤ 21) gives an independent value of s, so a true configuration scores 24/24; plaintext feed uses only crib-to-crib links. `tools/cycle150/zigauto.c`.

**Controls.** 6/6 planted keys recovered with full English (CT feed direct, behind a bank entry, carved order, inverse permutation; PT feed 11/11).

**Result.** Direct K4 best 7/24. Behind the bank (9.1 × 10^9 configs per text) K4 best 10/24, nulls 12 and 11; K4's tail counts are slightly *below* both nulls. PT-feed best 9 vs nulls 9–10. **Negative.**

**Not covered.** Form cycles longer than 3 or keyed by a word; per-letter shift that also steps (progressive + zig-zag); keyword-mixed plain alphabets with zig-zag.
