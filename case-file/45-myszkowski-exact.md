# 45 — Myszkowski transposition, tested exactly (cycle 46)

> *The Myszkowski man had only ever been roughed up in an alley: cycle 4 shook him with annealing, got "eight conflicts", and let him walk. Tonight he got a proper interview. Every way his keyword could repeat a letter, eight columns wide and under, and every themed word I could think of past that. He had an alibi for every one.*

## Why
The coverage table listed Myszkowski as "annealing only (cycle 4, heuristic), nothing exactly". It is the classic way to put a **keyword with repeated letters** on a columnar transposition (tied columns are read together, row by row, left to right), and K1–K3's keywords (PALIMPSEST, ABSCISSA) both repeat letters. Plain columnar (no repeats) has been tested since cycle 13; Myszkowski permutations are different permutations, not covered by it. **New family** for the diversity rule.

## Method (`tools/run_cycle46.sh`, `tools/myszkowski_gen.py`, checker `tools/railamsco.c` unchanged from cycle 44)
- **Transpositions (1,104,415 incl. inverses and identity):** every rank pattern with at least one tie for widths 3–8 (all weak orderings of the columns, 552,210 patterns), plus 33 themed keywords with repeated letters at widths up to 18 (PALIMPSEST, EASTNORTHEAST, BERLINCLOCK, UNDERGRUUND, DESPARATLY, TUTANKHAMEN, HOWARDCARTER, VIRTUALLYINVISIBLE, WELTZEITUHR, CHECKPOINTCHARLIE, …), ranked both in A–Z and in KRYPTOS-alphabet order. Each as encryption and decryption permutation. The generator reproduces the textbook example (WEAREDISCOVEREDFLEEATONCE under TOMATO gives ROFOACDTEDSEEEACWEIVRLENE).
- **Substitution:** periodic or progressive keyword key (key_i = k[i mod L] + s·⌊i/L⌋, L 1–26, s 0–25), Vigenère or Beaufort (variant covered by sign), A–Z or KRYPTOS tableau, both layer orders. Exact crib consistency over all 24 known letters; 6.0 × 10⁹ tests per text.
- **Nulls:** 3 shuffled K4s through the whole family. **Controls:** 4 planted English texts with the cribs at the official positions, encrypted under random Myszkowski permutations (all landed on width 8) with random progressive keys (L 7–13), run on a ±2,000-permutation window.

## Results (`analysis/cycle46_myszkowski_summary.txt`)
| Text | Consistent, L ≤ 20 | Partial fits L = 21 / 22 / 23 |
|---|---|---|
| K4 | **0** | 104 / 225 / 4,641 |
| null 1 | 0 | 15 / 193 / 4,103 |
| null 2 | 0 | 3 / 180 / 4,762 |
| null 3 | 0 | 28 / 199 / 5,417 |
| controls 81–84 | 4/4 recovered at the planted permutation and key, all ranked first by quadgrams | — |

**The L = 21 excess, checked.** K4's 104 fits at L = 21 sit above the three nulls (3–28), so I listed them (`tools/myszkowski_l21.c`). They are one cluster, not 104 witnesses: 89 width-8 permutations that differ only in columns no crib touches, 54 of them sharing a single setting (A–Z, carved-index key, Beaufort, s = 19); the rest fall into five more settings, the same number of distinct settings as null 3. Filling the key classes the cribs miss by quadgrams, K4's best L = 21 decryption scores −6.72 per quadgram (gibberish), null 3's best −6.83; the planted English plaintexts score −4.0 to −4.4 on the same table. **Look-elsewhere artefact of correlated permutations; no signal.** L ≥ 21 stays crib-underdetermined, as in cycles 41 and 44.

**Verdict.** No Myszkowski transposition of width ≤ 8 (any tie pattern) or with any of 33 themed repeated-letter keywords, on either side of a periodic or progressive keyword substitution with L ≤ 20, fits K4's 24 known letters. **Negative.**

## What this does not cover
Myszkowski widths 9–14 with arbitrary tie patterns (7.1 × 10⁶ patterns at width 9 alone; feasible in 2–3 cycles with a checkpoint), running keys behind Myszkowski (cycle 35's `bookrk.c` takes the same permutation file, so this is a cheap follow-up), Myszkowski combined with a second transposition, and non-additive substitutions.
