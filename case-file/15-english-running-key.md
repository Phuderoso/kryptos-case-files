# 15 — An English running key from any book (cycle 16)
> *You don't need to find the book if you can recognise its handwriting. Twenty-four letters of the key are already on the table; if they came out of a novel, they'd read like one.*

## 1. Why this
Cycle 2 tested running keys from K0–K3 only, and cycle 14 listed "running keys from untried texts" as an open lead. Instead of guessing the book, this cycle uses a **source-agnostic** property: in a running-key Vigenère / Beaufort / variant Beaufort, the key is ordinary English text. At the crib positions the key letters are forced, and they form **two contiguous fragments** (13 letters under EASTNORTHEAST at 22–34, 11 under BERLINCLOCK at 64–74). If the key were any English text (Carter's diary, a speech, the Bible, a novel), those fragments would read as English.

**HYPOTHESIS R1.** K4 = running-key cipher with an English key text, applied directly to the carved ciphertext, on a themed tableau: plain alphabet Pa and cipher alphabet Ca each one of 264 single-word themed alphabets (AZ, KA, reverses; keyed, reversed-keyed and ACA-columnar alphabets of the 89 plain-sight words used since cycle 7, after removing duplicates), key letters read in Pa, Ca or AZ; Vigenère, Beaufort and variant. That covers K1/K2's Quagmire III tableau, plus Quagmire I, II and IV variants: **627,264 tableaux**.

## 2. Test (`tools/k4_runkey.py`)
For every tableau, derive the 24 key letters and score the two fragments with the English quadgram table used since cycle 4 (mean log10 over the 18 quadgrams).

## 3. Controls ([runkey_control.txt](../analysis/runkey_control.txt))
Seven planted texts: an English passage (Jane Eyre, not in the quadgram training set) with K4's cribs inserted, encrypted with a running key from Dracula (also untrained), on a fixed tableau (k:PALIMPSEST / k:BERLIN) and six random themed tableaux. **The planted tableau ranked first in 7 of 7**, scoring −3.67 to −4.86 (e.g. key fragments DIATEANDSOLEP / OFTHISISTHE). **PASS.**

## 4. Results ([runkey_report.txt](../analysis/runkey_report.txt), [runkey_null_best.txt](../analysis/runkey_null_best.txt))
| Item | Result |
|---|---|
| K4, best of 627,264 tableaux | **−5.13**: key fragments FGGENMEAGALEW / FMEDREATTSC (Pa = c:NUANCE, Ca = r:TISYOURPOSITION, Vigenère). Not English |
| Shuffled-K4 nulls, best per run (15 runs) | −5.15 to −5.67 |
| Planted English controls | −3.67 to −4.86, always rank 1 |

K4's best sits at the top edge of the null range (look-elsewhere over 627k tableaux), well short of every English control, and its fragments don't read.

## 5. Verdict
| Hypothesis | Status |
|---|---|
| R1: English running key (any source text), directly on the carved text, on these 627,264 themed tableaux | **negative** |
| Same with a transposition before or after | open: the crib key letters would no longer be contiguous, so this fragment test doesn't apply |
| Arbitrary (non-themed) mixed alphabets | open |
| Non-English or non-text key streams (digits, coordinates) | covered for small digits by cycles 11–13, otherwise open |

A named-text search (every offset of specific books) is subsumed by this test for these tableaux: any English book would show up as an English-scoring fragment pair, as the controls show.
