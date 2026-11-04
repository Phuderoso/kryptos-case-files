# 19 — An English running key behind a transposition (cycle 20)
> *Cycle 16 said the trick only works when nobody shuffled the deck. I went back and read my own notes. If the key goes on first and the shuffle comes after, you can un-shuffle and the key's handwriting is right there again.*

## 1. Why this (and an audit of cycle 16)
Cycle 16 scored the 24 forced key letters of a running-key cipher as English and marked "running key with a transposition before or after" as untestable, because the key letters "would no longer be contiguous". **That was only half right.** If the order is *substitute with the running key, then transpose* (Model A, the order K3's transposition and K1/K2's tableau would suggest for a layered K4), undoing the transposition puts every plaintext letter back in its own position, so the key letters under EASTNORTHEAST (positions 22–34) and BERLINCLOCK (64–74) are again two contiguous fragments of the key text. Only the opposite order (transpose, then running key) scatters them. This cycle tests Model A.

**HYPOTHESIS R2.** K4 = English running key (any source text) on a KRYPTOS-keyed or straight tableau (Vigenère, Beaufort or variant Beaufort), followed by a transposition from the cycle 19 family: all column orders for widths 2–8, K3-style single and double rotations (widths 2–49, columns read up or down, left or right), and every inverse, **165,064 transpositions × 6 tableaux ≈ 1.0 million candidates**.

## 2. Test (`tools/k4_runkey_trans.py`)
For each candidate, undo the transposition, derive the 24 key letters and score the two fragments with the same English quadgram table as cycles 4–16 (mean log10 over the 18 quadgrams). No source text is named or needed.

## 3. Controls ([runkey_trans_control.txt](../analysis/runkey_trans_control.txt))
Eight planted texts: a Jane Eyre passage with K4's cribs inserted, encrypted with a Dracula running key (neither book is in the quadgram training set) on a random tableau, then a random transposition from the family. **The planted key fragments ranked first in 8 of 8**, scoring −3.54 to −4.77 (e.g. SAGOWEALLWENT / SSOFSOMEOFU behind a double rotation). **PASS.**

## 4. Results ([runkey_trans_report.txt](../analysis/runkey_trans_report.txt), [runkey_trans_nulls.txt](../analysis/runkey_trans_nulls.txt))
| Item | Best score | Best fragments |
|---|---|---|
| K4 | **−5.03** | HAPTATRIBEFXC / SAYSHONHEEK (KA, variant Beaufort, inverse 8-column order) — not English |
| Shuffled-K4 nulls (12 seeds) | −5.00 to −5.67 | e.g. MGSNOWNANDLOT / FOURKISMEQU (−5.00) |
| Planted English controls (8) | −3.54 to −4.77 | always rank 1 |

K4's best sits inside the null range (one shuffled copy scored higher), well short of every planted control. With a million candidates per text, phrases like "SNOWNAND" and "THEMEC" appear by chance; they are look-elsewhere noise.

## 5. Verdict
| Hypothesis | Status |
|---|---|
| R2: English running key, then columnar (w ≤ 8) or K3-style single/double rotation, KA/AZ tableau, three modes | **negative** |
| Cycle 16's note "transposition before or after: untestable" | **corrected**: the substitute-then-transpose order is testable and is now negative for this family |
| Transpose first, then running key (key letters scattered) | open; needs two-stream annealing or a language-model key prior |
| Running key on themed mixed tableaux behind a transposition (627k × 165k) | open (too large exhaustively; could be sampled) |
| `?` as 98th symbol with a running key | not tested this cycle |
