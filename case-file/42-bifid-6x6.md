# 42 — Bifid on a 6×6 square, alone and followed by a substitution (cycle 43)

> *Case file 20 closed every 5×5 square on a head count: K4 uses all 26 letters, and a 25-cell square can't print them. A 6×6 square can: 26 letters and ten other signs. Nobody in this office had walked through that door yet.*

## The model (`tools/k4_bifid6_sat.py`)
Delastelle's Bifid on a 6×6 square holding the 26 letters and 10 other signs (digits) in **any arrangement**. For a block of length L (period p, last block shorter), the coordinate stream is the L row digits then the L column digits; output letter k takes stream digits 2k and 2k+1. Wherever the input position behind a stream digit is cribbed, that's an equality between a square coordinate of a known plaintext letter and one of a known ciphertext letter. The square is encoded as an arbitrary 36×36 bijection (one-hot) and solved exactly with CaDiCaL (pysat). Only necessary conditions are encoded, so **UNSAT is a proof of exclusion** for that period and orientation.

Two models, periods 1–97, both orientations (carved text = Bifid encryption of the plaintext, or the reverse):
- **one square** — classic Bifid;
- **two squares** — independent input and output squares, which is the same thing as Bifid followed by any monoalphabetic substitution (the open item case file 20 left).

## Results

| Text | One square: consistent periods (enc / dec) | Two squares (enc / dec) |
|---|---|---|
| **K4** | **0 / 0** of 97 | 3 / 11 of 97 (enc 28, 30, 66; dec 31, 67, 76–78, 82, 83, 86–89) |
| 5 shuffled-K4 nulls | 0 / 0 each | 3–31 / 2–8 (mean ≈ 13 / 6) |
| planted controls, one square, p = 5, 9, 17 | exactly the true period, nothing else | — |
| planted controls, two squares, p = 7, 13 | — | true period found, plus 27–28 / 8–16 false ones |

Raw output: `analysis/cycle43_bifid6_{k4,nulls,controls}.txt` and the matching `.json`.

## Verdict
- **Bifid with any 6×6 square, any period, either orientation: excluded** (exact, with sharp controls). Together with the census rule-out in case file 20, plain Bifid is closed as K4's last layer for every square size that fits 26 letters.
- **Bifid followed by a monoalphabetic substitution (two squares): not excluded, and not supported.** The 24 cribs are too few to judge it: planted controls pass at many wrong periods, and K4's 14 surviving (period, orientation) pairs are fewer than the shuffled nulls average. This is an honest *open*, not a lead.

## What would close the two-square case
For each of K4's 14 survivors, anneal both squares together with crib-forced equalities and a quadgram score, with a planted two-square control at a surviving period as the gate. If the control is not recovered in the time budget, the attack is too weak and the result must say so.
