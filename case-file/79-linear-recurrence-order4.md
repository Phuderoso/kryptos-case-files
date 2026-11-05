# 79 — Linear-recurrence key mod 26, order 4 behind transpositions (cycle 81)

> *Last night the walker could remember three steps. Tonight I gave him four, and a head start on five.*

Extension of [case file 78](78-linear-recurrence-key.md): key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26), arbitrary weights, key on plaintext positions, then transposition (model A); KA/A–Z, Vigenère/Beaufort (variant = Vigenère negated).

## Faster exact solver (`tools/cycle81/linrec81.c`)
The first block-1 equation after d is fixed is linear in c_L: c_L·(K₁[1]−K₁[0]) = (K₁[L+1]−K₁[L]) − Σ_{j<L} c_j (K₁[L+1−j]−K₁[L−j]) (mod 26). Its 0, 1, 2 or 26 roots come from a lookup table, so only c₁…c_{L−1} are enumerated — 26× fewer tests, same exact check as cycle 80 (all block-1 equations, then propagation 34–73 must reproduce all 11 BERLINCLOCK key values). **Equivalence:** on cycle 80's L3 control window it returns the identical single hit; direct K4 L 1–6 again 0 (now 2 s instead of 32 s).

## Results
| Text | Scope | Tests | Hits |
|---|---|---|---|
| **K4** | 165,065 perms, L 1–4 | 1.19 × 10¹⁰ | **0** |
| 5 shuffled K4 nulls | 165,065 perms, L 4 | 1.15–1.17 × 10¹⁰ each | 0 each |
| **K4** | perms 0–19,999, L 5 (checkpoint) | 3.65 × 10¹⁰ | **0** |

## Planted controls (4/4, exact planted perm, c and d among the hits; decryption of 34–96 from block 1 alone)
| Control | Planted | Hits | Decryption |
|---|---|---|---|
| L4_fib4_KA_Vig | tetranacci c = (1,1,1,1), seed KRYP, perm 1,180 | 1 | ECONDSNORTHSEVENTYSEVENDEGREE… |
| L4_AZ_Beau_affine | c = (2,9,1,17), d = 11, perm 158,827 | 1 | TLIESTHENUANCEOFIQLUSIONKASCA… |
| L4_KA_Beau | c = (7,0,3,5), d = 0, perm 141,209 | 4 | ISLASTMESSAGEXTHIRTYEIGHTDEGR… |
| L5_direct_AZ_Vig | c = (4,6,1,22,9), d = 3, direct | 27 | RTEDTHECANDLEANDPEEREDINTHEHO… |

## Verdict
**Negative.** Order ≤ 4 behind the 165,065 transpositions is excluded (cycle 80: ≤ 3); order 5 excluded on the first 20,000 transpositions (checkpoint `analysis/cycle81/L5_checkpoint.txt`; resume with `linrec81 CT perms97.bin 20000 165065 5 5`, ≈ 1.5 h on 8 cores — not worth a cycle sequence unless a reason appears). Run took about 11 minutes wall time, over the 8-minute budget because of the L5 slice.

## Still open
L 5 on perms 20,000+; L 6 behind transpositions; model B (key on carved positions); recurrences over mixed alphabets; non-linear generators.
