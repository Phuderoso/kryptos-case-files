# Case file 139 — Hill under one carving error, and which exclusions already tolerate one (cycle 151)

**Cycle 151, 2026-11-08. Variant / audit** (IDEAS [I-003](../IDEAS.md), [I-005](../IDEAS.md), [I-006](../IDEAS.md); Firefly review F3; the cycle 150 community idea of a carving error).

## Why
An exact "all 24 crib letters must agree" test throws out the true key if one carved letter is wrong. K1–K3 each carry a one-letter
slip ([case 10](10-style-profile.md) §3), so every high-impact exact exclusion should say whether it survives one. The periodic
tableau family ([case 23](23-one-letter-anomaly.md)), Quagmire I–III ([108](108-quagmire-one-crib-error.md)), the stepping disk
([107](107-stepping-disk-one-crib-error.md)) and Kryha ([110](110-kryha-one-crib-error.md)) were already audited. **Hill was not:**
[case 26](26-hill-behind-transposition.md) lists "Hill combined with a carved-anomaly layer" as untested, and Hill is the family behind
the published HILL conjecture of Bauer, Link and Molle (extra L on the tableau; *Cryptologia*, a conjecture, not evidence).

## Model and method (`tools/cycle151/hill1e.c`)
Plain Hill decryption `out = D·c` on n-letter blocks, n = 2, 3, 4; A–Z and KRYPTOS numbering; every alignment; directly on the copper
and behind all 165,065 bank permutations in both directions, in both layer orders (model Q: transposition undone first; carved order:
Hill on the carved text, then transposition). Cribs at the official positions 22–34 and 64–74 (1-based; 21–33 and 63–73 in code).

- A wrong carved letter (a substitution, not a dropped or extra letter) lands in **exactly one** Hill block, so it can only break that
  block's crib equations. For each block that carries cribs: drop its equations, solve every row of D exactly mod 2 and mod 13 (CRT),
  keep invertible D.
- **Exact one-letter repair:** the dropped block must then be fixed by changing one of its n letters to some other letter so that it
  reproduces all of its own crib letters. That is the one-carving-error model.
- **One wrong crib letter** (Sanborn's clue itself wrong in one letter): only one equation dropped (`eqdrop`), a sub-case of the above.
- Solution spaces above 4,096 matrices per block-drop are counted as `under` (a blind spot), not decoded.
- Survivors are decrypted in full and scored by mean log10 quadgram (English ≈ −4.1).

## Controls (`data/cycle151/controls_check.txt`)
Six planted Hill encryptions of the English control text with **one corrupted carved letter** under a crib (n 2 direct, n 3 direct
KRYPTOS, n 2 model Q entry 4242, n 3 carved order inverse entry 120000, n 4 model Q entry 77777, n 4 direct): **6/6 recovered**. In each
the strict test fails (strict = 0), the right block is dropped, the repair names the **exact corrupted carved position** and its true
letter, and the decryption is full English (−4.04 to −4.10). Two uncorrupted controls (n 3 direct, n 2 carved entry 99999) pass the
strict test (strict = 1) and also decode as English.

## Results (`data/cycle151/results.txt`, 38 s wall on 8 processes for three texts)
| n | configs per text | K4 strict | K4 eqdrop | K4 blockdrop | K4 repaired | null1 (eqdrop / blockdrop / repaired) | null2 |
|---|---|---|---|---|---|---|---|
| 2 | 2,641,044 | 0 | 0 | 0 | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| 3 | 3,961,566 | 0 | 0 | 0 | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| 4 | 5,282,088 | 0 | 0 | 164 | **0** | 2 / 132 / 0 | 4 / 136 / 2 (best −7.50, gibberish) |

- **n = 2 and 3: nothing survives even with one block dropped**, for K4 and both nulls. With 24 cribs each row keeps 6–11 checks after a drop.
- **n = 4:** dropping a block leaves about one check per row, so 132–164 configurations per text pass the weaker block-drop screen
  (K4 slightly more, 164, from its 5,598 invertible matrices), but **none of K4's passes the exact one-letter repair**; null 2 has 2 that do,
  both unreadable (best −7.50). K4 also has **0** one-wrong-crib-letter survivors (nulls 2 and 4).
- Blind spot: 0 underdetermined block-drops for K4 (null 1 had 4).
- The strict counts (0) reproduce cycle 27's result with an independent implementation.

**Verdict.** `EXACT-EXCL`: Hill n = 2–4 with A–Z or KRYPTOS numbering, directly or on either side of the 165k bank, is excluded **even with one wrong
carved letter (substitution) or one wrong crib letter**. At n = 4 the block-drop screen alone has little power (it fires on shuffled text at the same rate);
the exclusion rests on the exact repair, which has power there (its 0–2 hits per text are at chance).

## Audit: which exclusions already tolerate one error (IDEAS I-006)
Families scored by the **largest agreeing set** of crib letters report how close the best configuration came, so a one-letter slip would show as ≥ 22–23 of 24.
| Family (cycle) | Scoring | One carved-letter substitution | Status |
|---|---|---|---|
| Constant-digit running keys (148) | best agreeing set of 24 | breaks ≤ 1 crib | **robust by design**: K4 best 10/24 |
| Zig-zag autokey incl. ordinary CT/PT autokey, A–Z/KRYPTOS, behind the bank (150) | best agreeing set (CT n = 24 for L ≤ 21; PT 20–22 links) | CT feed breaks ≤ 2 cribs (own letter + one fed letter), PT feed ≤ 1 | **robust by design**: K4 best CT 10/24, PT 9 |
| Periodic Vig/Beau tableau, direct and behind the cycle-19 family (24) | strict, re-run with one crib dropped | — | audited: negative, p ≤ 18 |
| Quagmire I–III (120), stepping disk (119), Kryha (122), reflector machines (118) | leave-one-out / slip filter | — | audited: negative |
| Hill n = 2–4 direct and behind the bank (151) | exact repair | — | **audited this cycle: negative** |
| Mixed-direction periodic (146), vocabulary Quagmire / autokey behind the bank (133–137), ptfree (139–149), Gromark (129–130), columnar w 9–11 (124–126), Sequence transposition (127–128), Hill + key (143–144), Hill 5/6 (141–142) | strict | not audited | open: IDEAS I-007, I-008 and follow-ups |

## Scope and blind spots
- Only a **substituted** letter. A dropped or extra carved letter shifts every later Hill block and is not covered here (it is covered for periodic keys in case 23).
- Numbering A–Z and KRYPTOS only (arbitrary numbering was closed strictly for 2×2 only, case 28). Transpositions only from the 165k bank.
- Hill + additive key (cycles 143–144) and Hill n ≥ 5 were not re-run under one error.
- Two errors not tested.

## Community check (2026-11-08)
kryptosbot's findings page (status of 29 Sep 2026) reports one-letter carved-text perturbations and a single wrong / missing / extra / swapped letter with grid
rearrangements tested negative within its families, and notes that two-character differences anchored to Sanborn's archive were never run; it lists
the circled tableau letters in the working papers as an open, unanalysed lead (secondary source; queued as IDEAS I-002 / I-009). Public status: K4 unsolved;
Paradigm holds the archive and runs a hash checker.
