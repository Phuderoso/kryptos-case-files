# Case file 96: the doubled letters at width 7

K4 has six doubled letters, at carved positions (0-indexed) 18 BB, 25 QQ, 32 SS, 42 SS, 46 ZZ and 67 TT. Five of the six start at a position ≡ 4 (mod 7), so written seven to a line they stack in the same two columns. This is an old observation (an NSA analyst in 2007; Gillogly 1999; Bean 2021; the numberworld blog in 2017). Cycle 103 found that the width-21 signal partly rides on it, since 25, 46 and 67 are 21 apart. Cycle 104 measures it and tests what could cause it.

## 1. Is it real?
Statistic: for every modulus m 2–25, the largest excess of doubles in one residue class over the uniform share, maximised over m (so the look-elsewhere effect is built in). Against 20,000 shuffles of K4's own letters: **K4 excess 4.14, p ≈ 0.0009** ([`doubles.py`](../tools/cycle104/doubles.py)). Caveat: the statistic was chosen after the pattern was known, as it was by everyone before us. Under the cribs, three of the doubles are plaintext **NO** (25), **ST** (32) and **IN** (67).

## 2. What could cause it? Three tests
| Model | Range | K4 | Nulls | Controls |
|---|---|---|---|---|
| Progressive periodic key: k[i+p] = k[i] + D (a period-p key that shifts by D every period), A–Z/KRYPTOS, Vig/Beau/variant ([`prog.py`](../tools/cycle104/prog.py)) | p 1–48, D 0–25, ≥ 4 crib checks | **0** | 0 in 50 shuffles | 6/6 recovered ([`ctlprog.py`](../tools/cycle104/ctlprog.py)) |
| Fully general periodic substitution: each phase its own arbitrary alphabet (no tableau) ([`genper.py`](../tools/cycle104/genper.py)) | p 1–48 | **inconsistent at every p ≤ 7** and at 9, 10, 14, 15, 17, 21, 25, 34, 42, 43, 45; consistent p 8, 11–13, 16, 18–20, 22–24, 26+ | p 7 consistent in 29% of shuffles; p 15/17/19 only ~3% | (exact test; true config always passes) |
| Width-w columnar, any order, both directions + fully general periodic, phase on plaintext or carved position ([`colgen.py`](../tools/cycle104/colgen.py)) | w 2–8, p 1–14 | p 1–3: **0**; p 4: 59, p 5: 337, p 6–7: 22k–31k | 3 nulls: p 3: 0/54/0; p 4: 16–76; p 5: 270–1,503 | 3/3 recovered, with 0–3 false hits at p ≤ 3 ([`ctlcol.py`](../tools/cycle104/ctlcol.py)) |

**Reading.**
- A period-7 key cannot cause the doubles: even seven completely independent alphabets contradict the cribs at p = 7. In plain arithmetic, the doubles at 25 and 32 need the same key step (plaintext NO and ST both differ by +1), but TT at 67 needs +5.
- The progressive version (a period-p key drifting by D each period) is **excluded** for p ≤ 48.
- Columnar transposition w ≤ 8 + general periodic substitution is **excluded for p ≤ 3**. For p ≥ 4 it sits at null level: the cribs can't judge it, and with that many free alphabets English scoring is weak, so it stays **open but low-value**.
- So the doubles are still unexplained. Their phase pattern (two "+1" pairs, one "+5") is the kind of thing a key that changes partway through, or a transposition whose rows are 7 wide, would produce.

## Still open
- A key that changes at a boundary between 32 and 67 (e.g. at a W, or at 63) while keeping the width-7 phase.
- Rows of 7 as the transposition grid (K3-style route on a 7 × 14 block with the "?" as the 98th cell), with a tableau substitution rather than free alphabets.
