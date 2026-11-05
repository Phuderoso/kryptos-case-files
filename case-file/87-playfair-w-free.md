# Case file 87 — Playfair on the W-free text (cycle 91)

**Question.** Cycles 87–90 kept returning to one structural fact: drop the five Ws and K4 becomes a 92-letter text
over exactly 25 letters. Even length and 25 letters is where Playfair lives (the omitted letter is usually J; here it
would be W). Cycle 21 excluded Playfair as K4's *last* layer because K4 has 26 letters, and cycles 82–86 tested
Playfair as an inner layer with a 26-letter outer key. Neither covered the model where **W is a null** and every layer
works on the W-less 25-letter alphabet.

**Model.** plaintext (no W) → Playfair with **any** 5×5 square omitting W → optional periodic outer key
(Vigenère, Beaufort or variant) on a W-less KRYPTOS or A–Z tableau, **mod 25** → insert five Ws. Cribs on the W-free
text: EASTNORTHEAST at 20–32, BERLINCLOCK at 60–70. Both pair alignments.

**1. Direct Playfair (no outer key) is impossible, by inspection.**
- Alignment 0 gives the ciphertext pairs BB, QQ, TT, SS, ZZ; alignment 1 gives SS, TT. Playfair never outputs a
  doubled pair.
- W-free position 31 encrypts S to S under the crib; Playfair never maps a letter to itself.

**2. With a periodic outer key: exact SAT** (CaDiCaL via PySAT; [tools/cycle91/sat91.py](../tools/cycle91/sat91.py),
adapted from cycle 83). The square, the key and the free partners of the half-crib pairs are all free variables. All 13
crib-touching pairs are constrained, every intermediate pair must have two different letters, and no intermediate letter
can be W.

| | p 1 | p 2 | p 3 | p 4 | p 5 | p 6 | p 7–8 |
|---|---|---|---|---|---|---|---|
| K4 (12 configs per p) | 0/12 SAT | 0/12 | 0/12 | 0/12 | 0/12 | 0/5 run | queued |
| 3 shuffled nulls (36 per p) | 0/36 | 0/36 | 0/36 | 0/36 | 0/36 | 0/12 run | — |

Planted controls (random W-less square, mod-25 key, cribs planted, via [mkctl91.py](../tools/cycle91/mkctl91.py)) at
p 3, 4 and 5: **3/3 SAT**.

**Verdict.** The W-null + Playfair + periodic mod-25 key model is **excluded for p ≤ 5** (and for 5 of 12 configs
at p 6). Raw output: [data/cycle91/results.txt](../data/cycle91/results.txt). The 55 queued jobs are in
[data/cycle91/remaining.txt](../data/cycle91/remaining.txt) and run with
[run91.sh](../tools/cycle91/run91.sh).

**Caveats.**
- Nulls are UNSAT as well, so this test excludes; it can't rank candidates.
- The controls were checked for satisfiability only; the cycle 83 controls already showed this encoding recovers the
  exact key.
- From cycle 86 we know that at p ≥ 8 the cribs stop constraining Playfair + key, so p 8 will need scoring on the
  full text rather than SAT.

## Cycle 92 addendum: p ≤ 7 closed

Resumed the queue. All 43 jobs finished, none hit the 420 s cap ([data/cycle92/results.txt](../data/cycle92/results.txt)):

- K4 p 6: the remaining 7 configs are UNSAT (12/12 overall).
- K4 p 7: 12/12 UNSAT.
- Shuffled nulls p 6: the remaining 24 are UNSAT (36/36 overall).

**Verdict: W-null + Playfair with any W-less square + periodic Vigenère/Beaufort/variant mod 25 (KA or A–Z, both
alignments) is excluded for p ≤ 7.** The 12 K4 p 8 configs are listed in
[data/cycle92/remaining.txt](../data/cycle92/remaining.txt). Expect them to be crib-underdetermined, as in cycle 86,
so p 8 needs scoring on the full text.
