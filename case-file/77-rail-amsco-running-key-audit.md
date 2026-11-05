# 77 — Audit: cycle 45's running keys behind rail fence / Redefence / AMSCO (cycle 79)

**Type:** audit + gap closure (diversity rule: cycle 78 was an extension; 79 is free; **80 must be a new family**).

## Why
Cycle 45 ran running keys behind cycle 44's 1,873,954 rail/Redefence/AMSCO permutations with the cycle-35 tool
`bookrk`. Cycle 74 audited `bookrk` only on the cycle-12 transposition family. Two things were never checked:
(1) whether cycle 44's generator actually produces the rail fence / Redefence / AMSCO a textbook would, in a direction
the solver can use; (2) whether every key text listed for cycle 45 was really testable.

## Method
- `tools/cycle79/gen79.py` re-implements rail fence, Redefence (rails read in key-word order) and AMSCO (key-word
  column order, 1- or 2-letter first cell, continuous alternation or ACA row-alternating starts) from the textbook
  descriptions as **string operations**, independent of `tools/railamsco_gen.py`, and looks each one up in
  `perms_A.bin` + `perms_B.bin`.
- Seven controls enciphered with Sanborn's verified K1/K2 rule (KA tableau, C = P + K in KA numbering; exact inverse of
  the decryptor that reproduces K1 with PALIMPSEST), key = a running text at a random offset, model A (key in
  plaintext order, then transpose) and model B (textbook transposition first, then key in carved order). Stress
  points: Carter vol. I forward and reversed, KJV John, K3 plaintext reversed, K1–K3 plaintext, Carter's **last
  possible offset**, AMSCO width 9 (NORTHEAST) from the larger `perms_B` file. Solver: unchanged `bookrk` on a 3,014-
  permutation slice (3,000 random + planted), threshold 14. Each reported configuration was re-deciphered in full.

## Results
1. **Membership: 14/14 textbook transpositions are in the cycle-44 family, both as map and inverse** — rail r = 3, 7,
   29; Redefence CLOCK, BERLIN, KRYPTOS; AMSCO KRYPTOS, BERLIN (both start sizes, both row rules), CLOCK, SHADOW,
   LUCID, NORTHEAST (both starts).
2. **Controls: 7/7 recovered** at 24/24, each at the planted offset, in Sanborn's mode (`bookrk` mode 21), and each
   re-deciphers to **all 97 planted letters** (`analysis/cycle79_runs.txt`). Model A is found at the map, model B at
   the inverse — the family carries both, so the frame convention does not blind it. One extra 24/24 (control 2) is
   the same K2 key inside the K1–K3 plaintext text: expected. Best non-planted depth 10.
3. **A real gap.** `bookrk` uses non-cyclic offsets (offsets 0 … T − 97). For key texts **shorter than 97 letters**
   (K1 plaintext and ciphertext, 63 letters; K0 Morse, 81; each also reversed) there is no valid offset, and the tool
   silently scores them 0. Cycle 45's README line listed "carved texts", but **these six were never tested behind
   rail/AMSCO**, and the longer carved texts (336–850 letters) were never tested at wrapping offsets.
4. **Gap closed.** The cyclic tool `carved_rk69` (audited in cycle 74; 11 substitutions) passed 3/3 new wrapping
   controls (K1 plaintext behind AMSCO BERLIN model B, K0 Morse behind Redefence CLOCK model A, K1 ciphertext reversed
   behind rail r = 3 model A), then ran all **24 carved texts, cyclic, × 11 substitutions × all 1,873,954
   permutations × both layer orders**: **K4 best 11/24, 0 full fits** (33 configurations at 11); shuffled K4 nulls
   (3) best 11, 11, 12, 0 full fits. **Negative.**
5. K4 on the slice through `bookrk`: best 7/24, same as 2 shuffled nulls (7, 7). Cycle 45's own run is complete:
   8 chunks summing to 1,873,954 permutations; its null baseline covered 2 of the 8 chunks (noted, not redone —
   K4 there 7–9 vs nulls 8–10).

## Verdict
**PASS with one correction.** Cycle 45's negatives for the long books (Carter vol. I, KJV John) and the longer carved
texts stand. Its claim for the *short* carved texts was unearned until now; with this cycle it is covered (cyclic,
11 substitutions; the 18 Quagmire-style mixed modes of `bookrk` remain untested for the short texts).

Limits: rail fence only from the top rail in the textbook check (the family itself has every starting offset);
AMSCO widths ≤ 9; key-word column orders with ties left to right.

Reproduce: `tools/run_cycle79.sh` (needs cycle 44's permutation files and cycle 45's chunks/texts).
