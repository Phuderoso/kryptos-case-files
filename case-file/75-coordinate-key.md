# 75 — The coordinate key: abscissa + ordinate on a grid (cycle 77)

**Type:** new family (diversity rule: cycle 76 was an extension, so 77 must be new).

## Why this family, and why it is new
K2's key is **ABSCISSA**, the x-coordinate; K2's plaintext is a pair of coordinates; the tableau on the right panel
is itself a coordinate grid (a header row of letters across, a column of row letters down). The plain-sight reading
of that hint: the key of each letter is not one keyword but a *pair* of coordinates. Write the plaintext row by row
into a grid of width w (starting at column offset o, as K4 starts mid-row on the copper); the letter in column c,
row r is enciphered with key

  k(c, r) = a[c] + b[r]  (mod 26, in the tableau's index space),

a = the **column (abscissa) key**, b = the **row (ordinate) key**. On the KRYPTOS or A–Z tableau this is exactly
"look the key letter up in the tableau at row word × column word": the tableau cell (r, c) of a shifted-alphabet
table is the sum of the two indices. It is a layered-simple idea of K1/K2's kind (one tableau, two words, nothing
exotic) and a hand cipher Sanborn could do with the tableau he carved.

Coverage check against the README table: a periodic key (b constant) and the progressive keyword (b[r] = s·r, cycle
41) are special cases, and case file 14 tested a key that *restarts* every carved row (period 31). The general
two-key form, with **both a and b arbitrary**, is not in any case file or the coverage table. It is equivalent to a
period-w Vigenère followed by a second Vigenère whose key is constant on blocks of w letters — a block key, also
untested.

## Test (`tools/cycle77/coord77.c`, exact, no English scoring in the decision)
Each crib letter gives one equation a[c] + b[r] = K; the equations form a bipartite graph (columns × rows) and are
solved exactly with a weighted union-find (the gauge a + t, b − t cancels). A configuration is **consistent** if no
cycle contradicts; its number of **checks** = edges that closed a cycle (independent exact tests). Both a and b
range over all 26^(w+R) values; nothing is assumed about them being words.

- Grid width w 2–48, every offset o 0…w−1 (1,175 (w, o) per text); Vigenère and Beaufort (variant has the same
  consistency as Vigenère, a and b negated).
- **Direct:** 264 themed alphabets as tableau (cycle 66 set, includes KA and A–Z): 620,400 configurations.
- **Behind 165,065 permutations** (cycle-19 family incl. identity, `perms97.bin`), KA and A–Z tableau, model A
  (coordinate key in plaintext order, then transposition) and model B (transposition first, then the coordinate key
  over the carved order): **1,551,606,300** configurations, 231,648,214 consistent (all at ≤ 5 checks).
- Cribs at Sanborn's positions (EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-based). No Bean pruning.

**Power** (`analysis/cycle77/power77_modelA.json`, `power77_modelB.json`): in model A the check count depends only
on (w, o): ≥ 2 checks for 1,000 of 1,175 (w, o), ≥ 5 for 793, ≥ 6 for 679; every offset of w 2–16, 18–23, 36–46
has ≥ 5. Blind: w 25–31 (0–2 checks; the cribs spread over too many columns). Model B is weaker (crib letters
scattered by the transposition): median 4–6 checks for w ≤ 20, falling to 0–2 for w ≥ 38; 300-permutation sample.

## Controls (`tools/cycle77/controls77.py`, `analysis/cycle77_controls_planted.json`, `analysis/cycle77/controls_out.txt`)
English plaintext (cycle-74 corpus) with the cribs at the official positions, a random family transposition,
column word × row word, run through the unchanged engine on a 5,000-permutation window around the planted one:

| # | planted | recovered | checks | other configs ≥ 6 in window |
|---|---|---|---|---|
| 0 | KA Vigenère, model A, w 8 o 0, ABSCISSA × PALIMPSEST | yes | 11 | 0 |
| 1 | A–Z Beaufort, model A, w 7 o 3, KRYPTOS × BERLINWALL | yes | 13 | 3 aliases (w 14, 21, 42, same perm) |
| 2 | KA Beaufort, model B, w 5 o 2, SHADO × IQLUSION | consistent, **blind** | 3 | — |
| 3 | A–Z Vigenère, model B, w 11 o 0, LAYERTWOXYZ × ORDINATE | yes | 7 | 1 alias (o 10, same perm) |
| 4 | KA Vigenère, model A, w 13 o 6, UNDERGRUUND… × CLOCK | yes | 8 | 1 alias (w 39, same perm) |
| 5 | A–Z Vigenère, model A, w 4 o 1, EAST × WELTZEITUHR | yes | 14 | aliases at w 22/44 (same perm, 7–8) |

**5/5 testable controls recovered** at the top of their windows; control 2 was found consistent but its
transposition leaves only 3 checks in model B (a measured blind spot, not a solver failure). Control 0's partial
decryption reads `…EDTHEEASTNORTHEASTEEVENI… TENTOMRBERLINCLOCKECHIEF…` (−4.25 per quadgram).

## Result (`analysis/cycle77_summary.json`, `analysis/cycle77/`)
| test | K4 | shuffled K4 (min–median–max) |
|---|---|---|
| direct, 264 alphabets: max checks of a consistent config | **1** | 1–2–3 (20 nulls) |
| transpositions, model A: max checks | **4** | 4–5–6 (13 nulls) |
| transpositions, model B: max checks | **5** | 4–5–5 (13 nulls) |
| model A configs ≥ 4 checks | 16 | 15–108–1,354 |
| model B configs ≥ 4 checks | 120 | 77–160–1,428 |

K4 sits at the low end of the shuffled baseline everywhere; one shuffled text reached 6 checks (A–Z Beaufort,
model A, w 15), so 6 is not a safe signal line for this family — and K4 reaches neither 5 (model A) nor 6.
The three K4 configurations with 5 checks (all model B) decipher, where the key is fixed, to non-English outside the
cribs (`analysis/cycle77/k4_results.txt`: −6.83 and −7.39 per quadgram on 89 and 97 letters; the third fixes
only 38 letters, mostly crib letters).

What is **excluded exactly** (a true key is always consistent): direct coordinate key on any of the 264 themed
tableaux for every (w, o) with ≥ 2 checks (1,000 of 1,175); behind the 165,065 permutations, model A on KA/A–Z ×
Vigenère/Beaufort/variant for every (w, o) with ≥ 5 checks (793 of 1,175, all w 2–16, 18–23, 36–46). Model B
leaves 3 consistent survivors at 5 checks (unreadable) and many low-check ones that cannot be told from chance.

## Verdict
**Negative.** The abscissa-plus-ordinate key — Sanborn's tableau read at (row word, column word), both words
arbitrary — does not fit K4 directly on 264 themed tableaux or behind the cycle-19 transpositions where the cribs
can test it. No plaintext found; nothing to submit.
Still open: blind widths w 24–35 (model A), model B at low power, mixed alphabets on both sides (Quagmire-style),
the carved ragged rows of the copper as the grid, nulls with a coordinate key, transpositions outside the family.

Reproduce: `cd tools/cycle77 && sh run77.sh` (needs `perms97.bin`, `a264.bin`; ~1.5 min per text on 8 cores).
Cycle 77 ran K4 + shuffled nulls 0–12 behind transpositions (nulls 13–19 only direct), stopped at the compute
budget; the script resumes from its per-chunk checkpoints.
