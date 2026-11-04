# 14 — Keys longer than the alphabet, and a key that restarts with every carved row (cycle 15)
> *Everybody stopped counting at twenty-six. The copper doesn't. Its rows are thirty-one letters wide.*

## 1. Why this
Cycle 1 tested fixed-tableau periodic keys only up to period 26, and cycle 11b's SAT proofs stop at 25. Yet the sculpture suggests a longer natural period: in the panel transcript ([case file 06](06-physical-and-copies.md)) K4 fills the end of row 25 and three full rows of **31** letters. A K1/K2-style keyword tableau whose key **restarts at the start of every carved row** is exactly a period-31 key (the row offset only relabels residues). More generally, a key phrase longer than 26 letters (e.g. a multi-word phrase) gives a period of 27–96.

**HYPOTHESIS L1.** K4 = fixed-tableau Vigenère / Beaufort / variant Beaufort over AZ or the KRYPTOS alphabet (K1/K2's tableau), with a key of period 27–96; P = 31 is the "row-restart" case.

## 2. Test (`tools/k4_longperiod.py`)
For long periods the cribs rarely collide, so the test has two steps:
1. **Consistency:** each residue class mod P must get one key letter from all crib positions in it.
2. **Readability:** a consistent key fixes the key on every residue the cribs touch, so it fixes the plaintext at every position in those residues (typically 40–86 of 97 letters). The non-crib part of that partial plaintext must read as English (mean quadgram log-probability, same table as cycles 4+).

420 families (70 periods × 2 alphabets × 3 modes; variant Beaufort duplicates Vigenère with a negated key and is kept for the record).

## 3. Control ([longperiod_control.txt](../analysis/longperiod_control.txt))
English with the cribs planted at K4's positions, KA-Vigenère with a random period-31 key: P = 31 (KA) is consistent and its revealed partial plaintext reads THEYWEREBURI… WALLGOEAS… TUNTILYOURE…, scoring **−4.38** per quadgram (P = 62, its multiple, −4.2). **PASS.**

## 4. Results ([longperiod_report.txt](../analysis/longperiod_report.txt))
| Item | Result |
|---|---|
| **P = 31, row-restart key** (all 6 families) | **impossible**: the cribs contradict each other in every family |
| Consistent families, K4 | 282 / 420; three shuffled-K4 nulls give 282, 283, 282, so consistency itself is chance |
| Best partial plaintext of a consistent family | **−6.99** per quadgram (P = 65, KA Beaufort: ZONVSENAG…), versus −4.2 to −4.4 for the planted English. Every consistent family reads as gibberish |
| P = 27–29 (the most constrained consistent cases, 82–86 letters revealed) | −7.6 to −8.3, gibberish |

## 5. Verdict
| Hypothesis | Status |
|---|---|
| L1, P = 31 (key restarts every carved row), fixed AZ/KA tableau | **negative** (crib contradiction) |
| L1, any P from 27 to 96, fixed AZ/KA tableau | **negative** (consistent cases give non-English partial plaintext) |
| Long periods with **arbitrary** mixed alphabets (Quagmire, P ≥ 26) | **open**: too few collisions for the cribs to decide; needs language scoring with a search over alphabets |
| Long key after a transposition | **open** |
