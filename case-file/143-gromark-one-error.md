# Case file 143 — Gromark and Periodic Gromark under one error (cycle 155)

**Cycle 155, 2026-11-08. Variant / audit** (IDEAS [I-008](../IDEAS.md), part of [I-003](../IDEAS.md); method note for [I-047](../IDEAS.md)).

## Why
The Gromark exclusions are strict: cycle 10 ([case 08](08-audit-and-gromark.md)) showed ordinary Gromark with an A–Z plain alphabet is
impossible for bases 5–10, primers 4–6; cycle 130 ([case 118](118-periodic-gromark-unknown-keyword.md)) showed K4 is not a direct Periodic
Gromark with any keyword of 2–12 letters, using a relaxed model (cipher alphabet arbitrary, L free group offsets) and requiring all 24 crib
letters. K1–K3 each carry a one-letter slip, so one wrong carved or crib letter could have thrown out the true key.

## Scope (matches cycle 130, plus the cycle-10 ordinary Gromark)
- **Model P** (cycle 130's relaxation of the ACA Periodic Gromark): any cipher alphabet, L free group offsets (group g = (i div L) mod L),
  chain-addition digits d[i] = d[i−L] + d[i−L+1] mod 10. Primers: every digit string L 2–9; keyword-rank primers (permutations of 1..L,
  10 → 0, 11 → 1, 12 → 2) L 8–12. Plain alphabet A–Z or KRYPTOS; Vigenère or Beaufort (variant ≡ Beaufort under an arbitrary alphabet).
- **Model G** (ordinary Gromark, one offset, any cipher alphabet): base 10 every primer L 2–8; bases 5–9 every primer L 2–7 (cycle 10 had
  bases 5–10, L 4–6, A–Z plain).
- **Stage 2** (the ACA rule itself): for every K4 rank-primer survivor of model P, **every** keyword with that primer (all C(26, L) letter
  sets; the rank pattern fixes the order), cipher alphabet ACA keyword-columnar, keyword-mixed or KRYPTOS, offsets from the keyword letters,
  A–Z/KRYPTOS plain, Vig/Beau/variant, ≤ 1 crib mismatch.
- Texts: K4 and the six cycle-130 shuffled-K4 nulls (seeds 13001–13006). Nulls 1–2 at K4's full scale (L 9 digits, L 12 ranks);
  nulls 3–6 as in cycle 130 (L 2–8 digits, L 8–11 ranks); model G all seven texts at full scale.

## Method (`tools/cycle155/gromark1e.c`)
Each crib gives `v(ct) − o_g = pa(p) ± d` (one equation between a cipher-letter node and an offset node). **The digit stream does not depend
on the ciphertext**, so a wrong carved letter under a crib, or a wrong crib letter, breaks exactly one equation, and a wrong carved letter
elsewhere breaks none. One-error feasible ⇔ some 23-equation subset is feasible (weighted union-find + injectivity of letter values).
Exact pruning: when the 24 equations are infeasible, the dropped equation must belong to **every** infeasibility certificate; the program
takes one (the cycle closing the first contradiction in a spanning forest, or the tree path joining two letters forced to the same value)
and re-tests the full system without each of its edges. This is the union-find analogue of the syndrome block-drop of cycle 153 (I-047).
The strict counts reproduce cycle 130 exactly (e.g. null2 L 9: 4,697; L 12: 116; null3 L 8: 25), a built-in regression check.

## Controls (`data/cycle155/controls_check.txt`) — 11/11 stage 1, 2/2 stage 2
- Five genuine ACA Periodic Gromark plants (cycle 129 generator; keywords PALIMST, SHADOW, BERLIN, BLACKHORSE, CUBANSEDGIW; L 6–11; both
  plain alphabets; Vig, Beau, variant) with **one corrupted carved letter under a crib**: all five fail strict and are recovered by model P
  at their own primer with the **exact corrupted crib index** as the drop.
- Two uncorrupted plants pass strict; one plant with a **wrong crib letter** is recovered with the exact drop index (6, position 27).
- Three ordinary Gromark plants (random cipher alphabet): gro2 (corrupted) recovered with the exact drop in G and P; gro3 (clean) strict;
  gro1's corrupted letter became a letter used by no other crib, so it stays strict-feasible (an invisible error) and is found strictly.
- Stage 2 recovers the keyword itself from the corrupted plants: **BLACKHORSE** (L 10) and **CUBANSEDGIW** (L 11), plus 1–3 one-letter
  neighbours each.

## Independent check (`data/cycle155/independent_check.txt`)
A pure-Python recount with no shared code (tries all 24 drops, no certificate pruning, BFS propagation) reproduced tested / strict /
one-error / pairs on **56/56** jobs (models P and G, L 2–5, all seven texts — including null2 L 5 with 809 one-error primers and 1,420
pairs) and confirmed every listed K4 survivor and every control at its primer.

## Results (`data/cycle155/results.txt`) — one-error-feasible primers (strict-feasible in brackets where non-zero)
| model / primers | K4 | null1 | null2 | null3 | null4 | null5 | null6 | label |
|---|---|---|---|---|---|---|---|---|
| G, base 10, L 2–8 (all) | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **EXACT-EXCL** |
| G, bases 5–9, L 2–7 (all) | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **EXACT-EXCL** |
| P, L 2–7 (all digits) | **0** | 0 | 0, 1, 1, 809, 199, 621 (strict 7 at L 5, 2 at L 7) | 0 | 0 | 0 | 2 (L 6), else 0 | **EXACT-EXCL** |
| P, L 8–10 (rank primers) | **0** | 0 | 490 / 165 / 3,921 | 1 / 0 / 0 | 0 | 0 | 7 / 0 / 4 | **EXACT-EXCL** |
| P, L 8 (all digits) | 28 | 36 | 1,150,334 (4,704) | 4,755 (25) | 27 | 0 | 19,430 | LOW-POWER |
| P, L 9 (all digits) | 11 | 0 | 508,775 (4,697) | — | — | — | — | LOW-POWER |
| P, L 11 (rank primers) | 6 (3 digit strings) | 0 | 6,588 (62) | 0 | 0 | 0 | 72 | LOW-POWER (stage 1) |
| P, L 12 (rank primers) | 4 (1 digit string) | 0 | 31,124 (116) | — | — | — | — | LOW-POWER (stage 1) |
| **ACA rule, any keyword, L 11–12** (stage 2 on all K4 rank survivors) | **0** of 1.53 × 10⁹ keyword configs | — | 0 (4 sampled survivors) | — | — | — | 0 (4 L 10 survivors) | **EXACT-EXCL** |

K4 never passes strictly (as in cycle 130). Under one error K4 has no survivor at all for L ≤ 7, nor for rank primers L 8–10. Its L 8–12
survivors (28 + 11 digit primers, 4 rank-primer digit strings) sit inside the very wide null range (0 to 10⁶, driven by how often a text's
crib letters repeat: K4 has 14 distinct cipher letters under the cribs, the nulls 13–19), so the count screen cannot single K4 out; with
only two nulls at full scale for L 9 and 12, no tail claim is made. The relaxed survivors were not decoded (the alphabet is free and
underdetermined). Stage 2 shows none of K4's rank survivors corresponds to an actual ACA keyword of any spelling.

## Verdict
**Negative.** Under one wrong carved letter (substitution) or one wrong crib letter, K4 is **not**:
- an ordinary Gromark with any cipher alphabet, plain A–Z or KRYPTOS, base 10 with primers of 2–8 digits or bases 5–9 with primers of 2–7
  digits (`EXACT-EXCL`; extends cycle 10 to one error and to arbitrary cipher alphabets);
- a relaxed periodic Gromark (free alphabet, free group offsets) with any digit primer L 2–7 or any keyword-rank primer L 8–10 (`EXACT-EXCL`);
- an **ACA Periodic Gromark with any keyword of 2–12 distinct letters** (cipher alphabet keyword-columnar, keyword-mixed or KRYPTOS;
  `EXACT-EXCL`, stage 1 + stage 2).
The relaxed model with non-keyword digit primers L 8–9 and the relaxed rank-primer survivors L 11–12 are `LOW-POWER` at the count level.

## Scope and blind spots
- Substituted letters only; a dropped or inserted carved letter shifts the digit alignment (not tested; cf. I-039).
- Direct only; Gromark behind transpositions under one error is not covered (I-018, I-053).
- Model G L 9 and base-10 L ≥ 9 not run (cost); double-mixed Gromark (both alphabets arbitrary) was never strictly excluded (case 63), so it
  has no one-error audit to do.
- Relaxed P survivors (K4: 28 + 11 digit primers, 4 rank strings) undecoded (I-051); nulls not matched to K4's crib-letter repetition
  profile (I-052).
- Compute: ~21 min wall on 8 processes, well over the ~8 min target (null2's ~10⁶ survivors slowed L 8–9).

## Files
[tools/cycle155/](../tools/cycle155/) (`gromark1e.c`, `acakw1e.c`, `plant155.py`, `indep_check.py`, `summarize155.py`, `run_cycle155.sh`) ·
[data/cycle155/](../data/cycle155/) (`results.txt`, `c_lines.txt`, `k4_survivors.txt`, `stage2_aca_any_keyword.txt`, `controls.txt`,
`controls_check.txt`, `independent_check.txt`, `timing.txt`) · [journal](../journal/2026-11-08-cycle155.md).
