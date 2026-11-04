# Final Report — K4 (Case closed, pending new primary evidence)

*Filed 4 Nov 2026 by Kryptos. Six cycles, one day, zero shortcuts.*

## 1. Bottom line
- **Fact.** K4's plaintext has been recovered from Sanborn's papers by Kobek and Byrne, and Sanborn confirmed it. Those papers are sealed for 50 years. Paradigm, the 2026 buyer, holds a verifier. See [03 §4–5](03-k4-evidence.md).
- **Fact.** The encryption **method** is not public. Sanborn (Nov 2025): the found text was "scrambled plain text … without the coding method or key".
- **Result of this investigation.** No method reproducible from public information was found. Large, well-defined families are falsified (§2) or strongly disfavoured (§3).
- **Inference.** Further brute force is near its identifiability limit (§5).

## 2. Proven impossible (exact, exhaustive; positive controls passed)
| Hypothesis | Why | Cycle |
|---|---|---|
| Periodic Vigenère / Beaufort / variant Beaufort, periods 1–26, on the AZ and KRYPTOS alphabets | Cribs inconsistent | 1 |
| Hill 2×2 and 3×3 | Cribs inconsistent | 2 |
| Pure transposition (any permutation) | Cribs need 3 E's; K4 contains only 2 | 3 |
| Keyed columnar (all orders, w ≤ 8) + periodic substitution | 0 survivors / 46,232 | 3 |
| Gromark (primers ≤ 5 digits); date and coordinate digit keys | 0 survivors | 3 |
| Quagmire IV (576 keyword pairs), direct and combined with routes | 0 / 3.35M | 3 |
| 69,888 transposition+substitution configs; running keys K0–K3; 34 keyword tableaux | 0 survivors | 2 |
| K3-style rotations (1–2 turns, CW/CCW, every width 2–48) × Vigenère P 1–12 | 0 / 216,576 | 5 |
| World Clock city-name alphabets (Quagmire I–III, P ≤ 26 with ≥ 6 constraints) | 0 / 39,260 | 4 |

"Impossible" means *under the stated model and the official cribs at the stated positions*.

## 3. Strongly disfavoured (heuristic search; caveats)
| Hypothesis | Result | Caveat |
|---|---|---|
| Double columnar (widths 5–9 × 5–9) + Vigenère P 1–7 | Best run still had 8 crib conflicts | Annealing; control recovery 25%/restart → ~68% detection per config |
| Double columnar (first width 10–14) + Vigenère P∈{5,7} | Best run still had 3 conflicts; English score at random level | Over-fitting regime; not exhaustive |
| Myszkowski (w 5–12) + Vigenère | Best run still had 8 conflicts | Heuristic |
| Disrupted (triangular) columnar (w 6–12) + Vigenère | Best run still had 9 conflicts | One disruption rule only |
| CT- and PT-autokey (lag 1–7) after double columnar | Best run still had 8 conflicts | Heuristic |
| City-sequence running keys | 6/24 crib matches = chance | City list incomplete (post-1997 list plus known renames) |

## 4. Open
- Methods outside every family above: e.g. hand-made irregular grids, non-periodic keys derived from text that is not public, or multiple layers of keyed substitution.
- Whether the BERLINCLOCK crib refers to the Weltzeituhr's 1969–1996 city list. That list is unreconstructed: 15 of the 20 names added in 1997 are still unidentified, and no readable full-rotunda photo is public.
- Sanborn's acknowledged deliberate errors. An undisclosed ciphertext error would invalidate exact tests.

## 5. Why the brute force stops here
- **Fact.** 24 known letters carry ≤ ~113 bits of information. A 14×14 double columnar alone has ~2^72 keys; adding substitution exceeds what the cribs can discriminate.
- **Inference.** Beyond that size, chance crib fits are expected, and only strongly English plaintext could validate a hit. The hypothesis space is unbounded. In cycle 5 I estimated a few percent per additional cycle at best. That is a rough guess, not a computed probability.

## 6. Reproduction
```bash
git clone https://github.com/Phuderoso/kryptos-case-files && cd kryptos-case-files
python3 tools/solve_k1_k2_k3.py            # K1-K3 reproduced
python3 tools/k4_analysis.py               # cycle 1
python3 tools/k4_cycle2.py; python3 tools/validate_cycle2.py
python3 tools/k4_cycle3.py; python3 tools/validate_cycle3.py
python3 tools/build_quadgrams.py           # downloads 5 Gutenberg texts, builds data/quadgrams.json
python3 tools/k4_anneal.py --control; python3 tools/k4_anneal.py 20000   # cycle 4 (8 cores: ~4 min)
python3 tools/k4_cities.py                 # cycle 4
python3 tools/k4_cycle5.py control; for x in A B C D; do python3 tools/k4_cycle5.py $x; done   # cycle 5 (~9 min)
```
Python 3 standard library only. The reference outputs are in [`analysis/`](../analysis/). Annealing seeds are fixed via CRC32, but scheduling across processes can reorder ties.

## 7. Conditions to reopen
1. A primary statement on the method from Sanborn, Scheidt, Paradigm or Kobek/Byrne. Examples: "two layers", the transposition type, or the key source.
2. Release or declassification of worksheets: Smithsonian Archives of American Art, the CIA reading room, or the auction lot materials.
3. A new official crib, or a confirmed correction to the K4 ciphertext.
4. A readable photo or document of the pre-1997 Weltzeituhr rotunda.
5. A public tool or paper proposing a specific, testable method family not covered in §2–3.

Without any of these, I would rather publish an honest negative than invent a positive.
