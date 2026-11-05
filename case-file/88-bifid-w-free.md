# Case file 88 — Bifid 5×5 on the W-free text (cycle 93)

**Question.** Cycles 87–92 treated W as a null, which leaves a 92-letter text over exactly 25 letters — the alphabet a
5×5 square holds. Cycle 21 ruled out 5×5 Bifid as K4's last layer only because K4 has 26 letters, and cycle 43
closed Bifid on 6×6 squares. Neither covers **W as a null + Bifid on a W-less 5×5 square**. This is a new family
for the repo (the README coverage table listed "W-free Bifid" as open).

**Model.** plaintext (no W) → Bifid with a 5×5 square holding the 25 W-less letters in **any** arrangement, period
p → insert five Ws. Cribs on the W-free text: EASTNORTHEAST at 20–32, BERLINCLOCK at 60–70. Every period 1–92, two
orientations (orient 0: ciphertext = Bifid-encrypt(plaintext); orient 1: Bifid's decrypt direction used to encrypt).
Two models: **one square** (classic Bifid) and **two independent squares** (= Bifid followed by any one-to-one
relettering of the 25 letters).

**1. Exact SAT** ([tools/cycle93/bifid5w.py](../tools/cycle93/bifid5w.py), adapted from cycle 43; CaDiCaL via PySAT).
Each output letter's row and column equal two digits of the input coordinate stream; where the stream position is
cribbed, that is an equality between square coordinates of two known letters. Only necessary conditions are encoded,
so UNSAT proves exclusion.

| | one square, orient 0 | one square, orient 1 | two squares, orient 0 | two squares, orient 1 |
|---|---|---|---|---|
| K4 W-free | **0/92** | **0/92** | 2/92 (p 28, 30) | 0/92 |
| 5 shuffled W-free nulls | 0/92 each | 0/92 each | 1, 5, 6, 7, 8 | 1, 2, 2, 3, 4 |

Planted controls (random W-less squares, cribs planted in English filler): one square p 5 (orient 0), p 11
(orient 1), p 21 (orient 0) — **each consistent at exactly its true period and orientation and nowhere else**.
Two squares p 7 (orient 0) — exactly its true period; p 13 (orient 1) — true period found, plus 7 false hits.

**Verdict (one square): W-null + Bifid on any W-less 5×5 square is excluded for every period, both orientations.**
With a relettering afterwards (two squares), K4 survives at 2 of 184 configurations while shuffled nulls survive at
3–11, so the cribs can't judge that model and K4 shows no signal (it sits at or below the null level).

**2. Annealing the two survivors** ([tools/cycle93/bifsa.c](../tools/cycle93/bifsa.c): both squares free, score =
English quadgrams + 3 × crib matches). Raw output in [data/cycle93/results.txt](../data/cycle93/results.txt) (sa_ = first pass, sb_ = second pass; cts = control and null ciphertexts).

- First pass (40 restarts × 4M steps): the planted two-square p 28 control was **not** recovered (best 13/24 cribs,
  −4.41 per quadgram), so this pass is underpowered. K4 p 28: 5/24, −4.62; K4 p 30: 9/24, −4.58; three shuffled nulls
  at p 28: 6–8/24, −4.53 to −4.68 — K4 is indistinguishable from the nulls.
- Second pass (16 restarts × 20M steps): control still **not** recovered (15/24 cribs, −4.41); K4 p 28: 2/24, −4.54;
  K4 p 30: 8/24, −4.63; two nulls: 9–10/24, −4.57 to −4.64. Again K4 sits at the null level, but with the control
  failing this is **not** a test of the two-square model.

**Caveats.**
- The two-square survivors (orient 0, p 28 and 30) are **open**, not excluded, until an annealer recovers a planted
  control of the same shape.
- The model has no outer periodic key. Bifid + mod-25 periodic key (the cycle 91 shape) is still open.

**Next for this family.** A stronger search for the two-square case: take the crib-forced coordinate equalities from
the SAT model as hard constraints (anneal only over squares the solver accepts), or enumerate SAT witnesses and score
each; then W-free Bifid + periodic mod-25 key with exact SAT, as cycle 91 did for Playfair.
