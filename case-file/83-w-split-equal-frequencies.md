# Case file 83 — Audit: the "W-split" equal-frequency groups (cycle 87)

**Claim audited:** numberworld.blog, [*Kryptos – The Cipher (Part 6-c)*](https://www.numberworld.blog/2026/04/kryptos-cipher-part-6-c-equal-letter.html) (April 2026), building on a mid-2010s
[Puzzling Stack Exchange answer](https://puzzling.stackexchange.com/questions/25931/unsolved-mysteries-kryptos/30772#30772): split K4 at its five Ws into six
blocks; odd blocks (B1, B3, B5) and even blocks (B2, B4, B6) each hold 46 letters and have the *same histogram shape*
(one letter ×5, two ×4, four ×3, six ×2, nine ×1), with different letters. The blog suggests this is not the by-product
of an ordinary cipher.

## Preregistered rule
Taken verbatim from the blog before any counting: split at every occurrence of one letter, number the blocks, put odd
blocks in one group and even blocks in the other. **Event** = equal group lengths **and** identical sorted count vectors.
Look-elsewhere version: the event happens for *any* letter that occurs at least twice.

## Results (`tools/cycle87/wsplit.py`, `tools/cycle87/maps_and_k13.py`; numbers in `data/cycle87/`)
| Test | Result |
|---|---|
| Positive control: real K4, split at W | reproduces the blog exactly: 46/46, shape (5,4,4,3,3,3,3,2,2,2,2,2,2,1×9) in both groups |
| Other split letters in real K4 | only W gives the event |
| 200,000 shuffled K4s (same letters): P(equal lengths at W) | 0.0197 (about 1 in 51) |
| P(identical shape \| equal lengths at W) | 0.0053 (about 1 in 190); a random 46/46 split of the 92 non-W letters gives 0.0044 |
| P(event at W) | **1.05 × 10⁻⁴ (about 1 in 9,500)** |
| P(event for any split letter) | **5.7 × 10⁻⁴ (about 1 in 1,800)** |
| Natural baseline: all 335 windows of 97 letters in the K1–K2 cipher panel (431 letters) | 0 events (expected about 0.2 at the shuffled rate) |
| Is group 2's histogram a shift or reflection of group 1's on A–Z or the KRYPTOS alphabet (104 maps)? | best map preserves the count of 10 of 22 letters; random relabelings give median 10, max 14, P(≥ 10) = 0.83: **no relation** |

## Verdict
The observation is **real and correctly stated**, and it is unusual under a shuffled-letters model: about 1 in 1,800
even allowing any split letter. It is **not** strong evidence of a planted structure, for three reasons:
1. It was found after the fact. The rule (split letter, parity grouping, histogram *shape* rather than letters) is one
   of many simple statistics people have run on K4 for 35 years; a few hundred such tries make a 1-in-1,800 hit
   expected somewhere.
2. Half the rarity is the equal 46/46 lengths (1 in 51), which is just where the five Ws happen to fall.
3. Shape equality ignores which letters occur; the letters differ almost entirely between groups, and no
   alphabet shift or reflection relates them, so the property gives no handle for a decryption.

The blocks do keep the cribs whole (EASTNORTHEAST in B2, BERLINCLOCK in B5), but with five cut points and two short
cribs that is likely anyway; not tested further.

**Still open, cheap:** if W is a null/separator (the X role in K1–K3), test known families on the 92-letter W-free text
with cribs shifted accordingly — the cribs stay inside blocks, so this is a clean, crib-testable variant.
