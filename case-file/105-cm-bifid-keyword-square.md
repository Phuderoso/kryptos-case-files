# 105 — CM-Bifid with one keyword square (cycle 117)

**Question.** Cycle 93 ([case file 88](88-bifid-w-free.md)) treated W as a null and tested Bifid on the 92-letter
W-free text. One square was excluded. **Two independent squares** (the ACA "CM Bifid", conjugated-matrix Bifid: the
plaintext coordinates come from square S1, and ciphertext letters are read from square S2) stayed open. Exact SAT
found only orientation 0, periods 28 and 30, consistent for K4, and nulls were consistent at 1–8 periods. Annealing
failed its planted control, so that case could not be read. K1–K3 used keyword-mixed alphabets. If Sanborn built
either square from a keyword, the case becomes exactly solvable.

**Why one keyword square is enough.**
- **A: S2 known, S1 free.** Undoing S2 gives the full coordinate stream, so every plaintext position gets a *cell* of
  S1. The plaintext is then a simple substitution of a known cell sequence. The cribs must map letters to cells
  consistently and one-to-one. Survivors would be finished by quadgram hill-climbing.
- **B: S1 known, S2 free.** The cribbed plaintext letters put known digits into the stream. Each ciphertext letter's
  row and column are two stream digits, so known rows (columns) must agree per letter, and an injective letter→cell
  completion must exist. This is checked exactly by bipartite matching.

**Space.** 264 themed keyword alphabets (KRYPTOS, A–Z, reversed, themed words; the cycle 59–77 list), W removed,
filled by rows or by columns: 524 distinct squares. Every period 1–92, orientation 0. (Cycle 93's SAT already
excludes orientation 1 for any two squares.) Cribs: EASTNORTHEAST at 20, BERLINCLOCK at 60 of the W-free text.

**Results** (`tools/cycle117/`, `data/cycle117/`).

| test | K4 | 6 shuffled nulls | planted controls (p 28, 30, 7) |
|---|---|---|---|
| A: keyword S2, free S1 | **0 of 48,208** | 0 each | 3/3 found at the true (p, S2), 1–2 consistent each; hill-climb reads the plaintext back (q −4.34) |
| B: keyword S1, free S2 | **0 of 48,208** | 0 each | 3/3 found at the true (p, S1), only at their true period |

At periods other than 28 and 30 these zeros agree with cycle 93's any-square SAT (an independent audit with
different code). At 28 and 30 they are new.

**Conclusion.** Negative. CM-Bifid on the W-free text with **either** square built from a K1–K3-style keyword is
excluded at every period. The only surviving CM-Bifid case is two non-keyword squares at p 28 or 30, which the cribs
cannot settle.

**Still open.** Two free squares at p 28 and 30 (needs a language attack that passes a planted control). CM-Bifid on
6×6 squares over the full 97 letters with keyword squares (26 letters + 10 digits). Keyword squares built by other
routes (spiral, diagonal, keyword-columnar).
