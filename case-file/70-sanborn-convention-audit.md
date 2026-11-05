# 70 — Audit: do our solvers speak Sanborn's dialect? (cycle 72)

**Type:** audit (diversity rule: cycle 71 was a new family; this is the permitted extension/audit cycle; 73 or 74 must be new again).

## Why
Every planted control so far was enciphered by a generator written *alongside* the solver it tests, sharing the same
conventions (KRYPTOS-tableau numbering, which letter is the key, which index frame the key follows behind a
transposition). A shared convention bug would pass every such control and still make the K4 runs blind. kryptosbot
reported exactly this kind of failure in its own work (a Bean-constraint check applied in the wrong frame behind
rearrangements, and constraints that only hold on the A–Z alphabet; findings page, status Sept 29, 2026).

## What was checked
1. **Bean-style pruning.** `rg` over all 209 files in `tools/`: no solver prunes with Bean equalities or key-difference
   shortcuts. "Bean" appears only in the cycle 10–11 Gromark tools, which reuse his 39 base-10 primer-5 primers; cycle 65
   recomputed that census independently with both alphabets arbitrary and got the same 39. All prefilters
   (`liftkey.py`, `k4_trifid_trans.py`, `m94_trans2.c`) reject only on exact contradictions, so they are sound.
2. **External-convention controls.** New generator `tools/sanborn_controls.py` enciphers with the exact inverse of
   `solve_k1_k2_k3.py`'s `vig_dec`, which is asserted to reproduce the carved K1 (PALIMPSEST) and K2 (ABSCISSA). Keys are
   Sanborn's real words. A pass therefore means the solver's KRYPTOS tableau, key-letter convention and frame match how K1
   and K2 were actually made, and the recovered key must *spell the word*.
   - **Cycle 41 solver (`progkw.c`, periodic/progressive key behind 165,065 transpositions):** 6 controls (PALIMPSEST,
     ABSCISSA, KRYPTOS, BERLIN; identity and random transpositions; both layer orders). **6/6 recovered with the full
     97-letter plaintext and the key printed as the word itself** (e.g. `num=K model=B L=7 s=0 key=KRYPTOS`); one case
     with an unfixed key class was filled correctly by quadgrams.
   - **Cycle 59 solver (`periodic_exact59.c`, K3-law decimations):** 4 controls (perm M101 s37 a5, both directions;
     ABSCISSA, PALIMPSEST, KRYPTOS, BERLIN; key by PT position and by carved position). **4/4: exactly one hit each, at
     the true decimation and minimal period**, keys `ABSCISSA`, `??L?MPSEST` (two classes not touched by the cribs),
     `KRYPTOS`, `BERLIN`.
3. **Reproducibility.** Full K4 rerun of cycle 41 gives identical numbers (892,671,520 tests; 0 hits at L ≤ 13;
   partial counts at L 21–26 = 6 / 89 / 2,358 / 8,959 / 47,037 / 719,494, same as `analysis/cycle41_progkw.txt`).

## Verdict
**PASS.** No Bean-type pruning anywhere; the two backbone solvers recover messages enciphered exactly the way K1/K2
were, under K3's transposition law, in both frames. The K4 negatives of cycles 13, 41, 59 (and the tools that share
their crib-check code) are not convention artefacts. Limits: only Vigenère with Sanborn's KA tableau was tested
externally (he used nothing else in K1–K2); the other families' controls remain self-generated.

Output: [`analysis/cycle72_audit.txt`](../analysis/cycle72_audit.txt). Control ciphertexts and planted configs: [`analysis/cycle72_controls.txt`](../analysis/cycle72_controls.txt).
Reproduce: `tools/run_cycle72.sh`.
