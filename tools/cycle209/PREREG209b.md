# PREREG209b — corrected re-registration after run 1 broke on a code bug (cycle 209, 2026-11-13)

Written 2026-11-13 04:22 PT (America/Vancouver), after run 1 of PREREG209 (04:07:36–04:13:18 PT, seed block 209210).

## What broke (reported, no verdict from run 1)
Run 1 computed each plant's exact-moment z on the **plaintext** X. Case 191 (whose test this audits) computes it on the **enciphered**
plant Y: COL_P(X) = COL_P(Y), but the permutation moments depend on the row's own letter multiset, and K4 is a ciphertext. Run 1's
q values (P 8 ≈ 0.34–0.40, also for its paired C3 batch, against case 191's 0.0027–0.0062) are therefore meaningless; G3 failed (rates
0.004–0.013) and G1b failed (the descriptive C3 batch was checked against C4-forced positions, a gate-code slip). Run 1 is kept
unchanged in `run1/` and is **NO VERDICT** as PREREG209 says. The K4 numbers seen in run 1 were the masks (structure) and these broken q.

## Changes (only these)
1. z is computed on Y. C4 plants are enciphered row by row with a Quagmire IV key drawn from a pool of 256 randomised CP-SAT solutions
   consistent with K4's cribs (tag 3; distinct solutions reported), free letters of both alphabets completed uniformly per row. The
   paired C3 batch is enciphered exactly as case 191 (lib204 `encipher`, per-phase bijections).
2. New regression gate **G4b**: the paired C3 q at P 8 must reproduce case 191's exact-O3 q per model (0.0027 / 0.0037 / 0.0035 /
   0.0062) within 3 binomial SE. This gate would have caught the bug.
3. G1b checks C4 batches at crib + C4-forced positions and the C3 batch with lib204 `consistent_rows`.
4. Periods: P 8 registered (decision rule of PREREG209 unchanged: bar 0.00625, 2-SE band, one ×4 extension); P 13 and 23 descriptive
   (other periods dropped for budget). G2b bar recomputed for 12 configurations.
5. Gs and Gx are **reused from run 1** (mask code unchanged; both passed: 970/970 true letters allowed, C4 ⊆ C3, 0 unknown; 6/6 UNSAT
   confirmed by the full model, 20/20 SAT certificates). G0, G4 are re-run.
6. Fresh seed block **209211** (run 1 used 209210). Next free after this cycle: **209212**.
