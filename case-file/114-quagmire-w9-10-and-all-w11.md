# Case file 114: Quagmire I/II behind any width 9–10 order, and every width-11 order

**Cycle 126, 2026-11-08. Verdict: negative.**

## Why
Cycle 124 closed every column order at widths 9 and 10 behind a periodic key, but only with matching alphabets on both sides (A–Z/A–Z or KRYPTOS/KRYPTOS, i.e. Vigenère and Quagmire III). Sanborn's K1–K2 tableau is KRYPTOS-keyed, and a hand cipherer could just as easily have keyed only one side. That gives Quagmire I (keyed plaintext alphabet) and Quagmire II (keyed cipher alphabet). Width 11 was the next gap in the coverage table.

## What was tested (exact, all 24 crib letters)
- **Part A.** All 9! + 10! column orders, columnar or row read, permutation and its inverse, key applied before or after the transposition, Quagmire I and II, Vigenère and Beaufort forms (variant has the same consistency), every period 1–18.
- **Part B.** All 11! = 39,916,800 column orders with the same options and all four alphabet pairs (A–Z, Quagmire I, II, III), periods 1–18.

## Controls and nulls
- 4/4 planted controls recovered at their true alphabet pair, form, key model and period: Quagmire I Vig p7 behind PALIMPSEST (w10); LODESTONE (w9) then Quagmire II Beaufort p9; SHADOWLESS row read (w10) then Quagmire I p4; UNDERGROUND (w11) then Vigenère p8.
- Shuffled K4: 0 survivors in Part A (3 nulls). Part B: 0 and 4 survivors (all at p18, the noise edge already seen in cycle 124).

## Result
**K4: 0 survivors in both parts at every period ≤ 18.** Periodic Quagmire I/II behind any keyed columnar of width 9–10, and any periodic tableau key (all four alphabet pairs) behind any width-11 order, are excluded up to period 18. Periods ≥ 19 are crib-underdetermined at these widths (see case file 112).

## Still open
Width 12–13 arbitrary orders (12! = 479M; needs a checkpointed multi-cycle run), Quagmire IV (two different keyed alphabets), running-key or autokey behind width 9–11 orders, and double columnar with a wide leg.
