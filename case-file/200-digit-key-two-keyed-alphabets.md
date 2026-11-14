# Case 200 — Digit keys on two keyed alphabets (Gronsfeld / Gromark "keyed on both sides"), and the I-292 blind plants (cycle 214)

**Slot:** new family (212 new family, 213 audit, so 214 must be new; I-293). Pre-registered in
[PREREG214](../tools/cycle214/PREREG214.md) (commit e96bd4b) before any part ran. Ideas: **I-295** (new, tested), **I-292** (tested),
**I-291** (cluster rule registered), **I-293** (done). Code: [`tools/cycle214/`](../tools/cycle214/); raw results: [`data/cycle214/`](../data/cycle214/).

## Part A — I-295: any digit key, both alphabets keyed

**Model.** c = Y[x(p)+k] (Vigenère form), c = Y[x(p)−k] (variant), c = Y[k−x(p)] (Beaufort form), with k ∈ {0…9}. X (plain) and
Y (cipher) are keyed alphabets. Behind a transposition: model Q (layer letter i carved at S[i]).

**The filter is key-agnostic.** The 24 crib positions give 24 values k_i for each (S, X, Y, form). If any falls outside 0…9, *no*
digit key of any kind (periodic Gronsfeld, Gromark chain, running digits, dates, constants) can produce K4 under that configuration.
The crib pairing (p_i, K4[S[i]]) does not depend on whether the key runs on the plaintext index or the carved index, so the filter
covers both layer orders at once. Expected chance survivors per pair-form ≈ (10/26)²⁴ ≈ 1.1 × 10⁻¹⁰.

**Solver.** `gron214.c` (sha 7e3ccf27…), OpenMP, early exit. Independent checker `check214.py` re-derives every survivor's digits
from scratch and decides Gromark chain consistency (k_n = k_{n−L} + k_{n−L+1} mod 10, primer L 1–40; exact elimination mod 2 and mod 5)
and periodic-digit consistency (P 1–40), for key index = plaintext position (ix 0) and carved position (ix 1).

**Gate (seed 209225).** 20 plants (10 direct with X, Y from the 86,731 list; 10 behind a random bank/all.bin row with themed X, Y, solver
on a 101-row slice), Gromark primer L 2–10 on either index: **20/20** recovered as digit-consistent *and* Gromark-consistent at the
true L and index → **PASS** (≥ 19/20). Checker recount of all 8 reported search/null survivors: **0 mismatches**.

**Results** (wall: 11 + 10 + 11 s for K4; 66 s with all nulls).

| scope | pair-forms | analytic E (cells) | K4 cells | null-equivalent cells | Gromark / periodic L ≤ 25, K4 |
|---|---:|---:|---:|---:|---|
| A1 direct, X, Y ∈ 86,731 alphabets, 3 forms | 2.26 × 10¹⁰ | 2.48 | **0** | 2 (1 X, 2 near-identical Y: 1 cluster) | — |
| A2 bank 165,065 × 2 dirs, X, Y ∈ 144 themed, 3 forms | 2.05 × 10¹⁰ | 2.26 | **0** | 3 (3 clusters, 10 tenth-nulls) | — |
| A2 all.bin 165,782 × 2 dirs, X, Y ∈ 144 themed, 3 forms | 2.06 × 10¹⁰ | 2.26 | **2 = 1 cluster** (inverse twins 94432/1, 94433/0) | 1 | **none** at either index |

The one K4 cluster: X = SLOWLYDESPARATLY-keyed (/Z), Y = MAGNETIC-keyed (/K), Beaufort form, crib digits
`353093431550239694766323`. No Gromark primer L ≤ 25 and no digit period ≤ 25 fits at either index; Gromark fits only at
L 27–30 (ix 0) / 27–40 (ix 1), which every plant and every random digit string also satisfies (vacuous, crib span 21–73). Best
agreement with π, e, √2, √3, √5, φ, ln 2, γ digit streams at any offset ≤ 900 (either index): 7–9 / 24, chance level.

**Chance rate of the Gromark layer.** For 5,000 uniform random 24-digit crib strings, Gromark L 1–25 or periodic P 1–25 (either index,
K4's survivor row) is consistent for 0.62 %; the first non-zero rates are at L ≥ 20 (`rates214_gromark_given_digits.txt`). So the
expected chance count at the Gromark level is ≈ 2.3 × 0.006 ≈ 0.014 per scope.

**Labels (as registered).**
- Digit level: K4 within the null band in every scope → **`NO-SIGNAL`**. Because the filter is necessary for every digit key, the
  K4 zero in A1 and A2-bank is also, logically, an **exact exclusion of every digit-key cipher in those scopes** (random texts give
  ~2 chance cells per scope, so a true configuration would not be hidden among false ones; the exclusion still says nothing outside
  the listed alphabets).
- Gromark chain and periodic Gronsfeld, L/P 1–25, both indices: K4 0 in all three scopes, chance ≪ 1 → **`EXACT-EXCL`
  (discriminating)**. L ≥ 26: **`NO-DISCRIMINATION`** (vacuous).
- all.bin cluster: no digit structure found → **`NO-SIGNAL`**.

**Blind spots.** Only the 86,731 list (direct) and the 144 themed alphabets (behind families); vocabulary × themed behind families is
not run (I-296). Base 10 only (I-299). No carving or crib error (I-297). Key on letters of other lengths (two-digit groups, "hex inside
hex" regrouping) not covered here. Not a test of arbitrary alphabets (the both-arbitrary problem is underdetermined).

## Part B — I-292: the Voynich desk's 10 blind grid-aligned wrapped-offset plants (credit: Voynich desk)
- Inputs: `ciphertexts.txt` sha 21d476a2…; truths sha 4daad92b… (unopened until the blind file was committed, commit e3665e2,
  `results214b_blind.txt` sha ad1564ef…).
- Unchanged `wrbank` (binary 614082dc…, source 1001272d…), full bank, L 16 only, 3 s per plant.
- Scored by her detection rule (`score214b.py`): **10 / 10 recovered → PASS** (bar ≥ 9/10). Lines per plant 2 / 2 / 2 / 2 / 2 / 2 / 4 /
  4 / 12 / 4; the extra line in G01–G06 is the inverse twin (same effective map); G07–G10 add near-equivalent rows (G09: 6 column
  orders, 12 lines). Case 194 stratum A (aligned rows) is now planted at non-zero and wrapped offsets too.

## Part C — I-291 cluster rule (registered, credit: Voynich desk)
Cells of one text are one cluster iff (a) same family, tm/form, L, segE, segB, o1, o2 (Part A: same X, Y, form) and (b) single-linkage on
effective maps agreeing on ≥ 16/24 crib positions; identical maps (inverse twins) always merge. Applied above. The cases 193–198
recount is still open (I-291, pointer I-298).

## Part D — case 198 addendum
Filed in [case 198](198-word-restart-themed-keyword-tableaux-hash-join.md) (addendum 1): the Voynich desk's L 15 Poisson tail.
