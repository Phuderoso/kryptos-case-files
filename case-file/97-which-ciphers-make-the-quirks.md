# Case file 97: which ciphers make doubles that line up at width 7?

**Cycle 105, 2026-11-05.** Code and raw output: [tools/cycle105](../tools/cycle105/).

## Question
K4 has three statistical quirks: five of its six doubled letters fall on one residue mod 7 (look-elsewhere excess 4.14 over moduli 2–25), eleven repeated vertical bigrams at width 21, and a flat IC of 0.0361. Instead of guessing a cipher and testing cribs, this cycle asked the reverse question: when English is enciphered with each candidate family, how often do those quirks appear by themselves?

## Method 1: simulation (`sim.py`, `modwin.py`)
97-letter windows from a Gutenberg English text, 20,000 per family, random keys and random column orders. T1 = doubles excess at least 4.14; T2 = width-21 repeats at least 11; T3 = IC at most 0.040.

| Family | T1 | T2 | T1 and T3 |
|---|---|---|---|
| Random letters (null) | 0.0013 | 0.0019 | 0.0008 |
| Monoalphabetic | 0.0011 | 0.46 | 0 |
| Vigenère p7 / p14 / p21 | 0.0019 / 0.0023 / 0.0018 | 0.014 / 0.005 / 0.005 | ≤ 0.001 |
| Quagmire III (KRYPTOS alphabet) p7 | 0.0016 | 0.014 | 0.0003 |
| Progressive p7, autokey, Gromark, running key | 0.0015–0.0019 | 0.002–0.005 | ≤ 0.001 |
| Columnar w7, then Vigenère p7 | 0.0019 | 0.008 | 0.0007 |
| **Vigenère p7, then columnar w7** | **0.012** | 0.011 | 0.0034 |
| **Vigenère p7, then columnar w14** | **0.014** | 0.013 | 0.0034 |
| Columnar w21, then monoalphabetic | 0.010 | 0.45 | 0 |

Only one shape lifts the doubles quirk well above chance: **a periodic substitution followed by a columnar transposition whose width is a multiple of the period** (about 10× the null rate; the scan in `simulation.txt` shows the lift appears only when the width is a multiple of p). The winning modulus is 7 in 245 of 552 hits for "p7 then w14", against 9 of 62 for random letters. So K4's quirk is roughly 25–30 times likelier under "period-7 substitution, then width-14 (or 7) columnar" than under chance. That is a pointer, not proof: about 1% of such ciphertexts show it at all, and no family reproduces the width-21 bigram quirk with a flat IC (joint rate ≤ 1 in 10,000 everywhere).

## Method 2: exact crib test of that shape (`subcol.py`)
Periodic substitution (period p dividing the width w) applied first, then a complete columnar transposition (every column order, not just keyword orders), in both reading directions. Tableaux: Vigenère, Beaufort and variant Beaufort over A–Z and the KRYPTOS alphabet. Backtracking with the cribs held fixed.

- Planted controls: 5/5 true orders accepted; in the strongly constrained direction the search finds the true order as the unique solution (w14 p7, w7 p7, w10 p5 KA).
- **K4: 0 consistent orders** for every w 5–12, every p dividing w (p ≥ 3), both directions, all six tableaux; w13 direction 0 and direction 1 (Vigenère A–Z); **w14 with p 7 and 14, direction 0, all six tableaux.**
- Not finished: w13 direction 1 (other tableaux), w14 direction 1, w21. These have many crib-free columns and need a smarter search (fix the crib-bearing columns, then count the rest).
- A free mixed alphabet per phase ("general") is satisfiable everywhere and needs language scoring, so it is not a test.

kryptosbot reports a similar negative for columnar widths 4–9 with key lengths 1–24 on the A–Z alphabet; this adds the KRYPTOS alphabet, the Beaufort forms and widths up to 14.

## Verdict
The doubles quirk has a natural mechanism (substitution first, then a columnar transposition whose width is a multiple of the period), and the simple tableau version of it is ruled out at the widths above. **Negative**, with one clear lead: a mixed-alphabet (Quagmire-style) substitution behind a width-14 or width-21 columnar, scored by language.
