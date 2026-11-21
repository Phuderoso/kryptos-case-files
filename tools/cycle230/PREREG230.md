# PREREG230 — cycle 230 pre-registration (filed before the registered run)

Filed 2026-11-21 ~07:49 PT (America/Vancouver). Slots: 228 free, 229 audit (I-335), so **230 is a new-family cycle** (I-341 / I-334).
Seeds: 209575 (smoke shuffle, used), 209576 (plants), 209577–209586 (10 nulls). **Next free seed after this cycle: 209587.**
Base: origin/main 01e8230.

**Disclosure (before filing).** One run of `bsk230` on the real K4, direct scope, was started by mistake before this file existed
(a smoke build with default thresholds). It was killed within seconds; its output file was never opened (only its line count, 53,
was printed by the same command) and was deleted. The smoke shuffle (209575) was then run in full twice (v1, and an arithmetic
speed-up, identical output). Nothing from K4 informed any threshold below.

## Part A (new family, I-299 generalised): bounded-shift keys on two keyed alphabets

**Why.** Case 200 asked for key digits 0…9 (base 10, anchored at 0). I-299 queued other bases and two-digit groups. Two points:
(1) bases b ≤ 10 anchored at 0 are subsets of case 200's range, so they were already excluded wherever case 200 was `EXACT-EXCL`
(direct, bank); only b ≥ 11 (and offsets) are new; (2) the natural generalisations of "a small numeric key" are **a window of W
consecutive shift values at any offset** (a digit key whose cipher alphabet is slid, keys 1–9, a base-b key with the alphabet
rotated; any base ≤ W) and **a key alphabet of ≤ D distinct shift values** at arbitrary values (a short keyword's letters reused in any
order or pattern, binary / ternary keys, a few-letter running key). Neither is in the coverage table: periodic, autokey, Gromark and
running keys all fix the stream's *structure*; this tests only its *range* and so covers every such structure at once.

**Model.** As case 200 / `gron214.c`: plaintext p, plain alphabet X, cipher alphabet Y, shift k per letter: Vigenère form
c = Y[x(p)+k], variant c = Y[x(p)−k], Beaufort c = Y[k−x(p)] (mod 26). Behind a transposition (model Q): layer letter i carved at
S[i] (S = family row, dir 0, or its inverse, dir 1). The 24 crib shifts k_j are order-free, so the filter holds for any key stream
and for both layer orders.

**Filter (`bsk230.c`).** Survivor ⇔ (W) all 24 k_j lie in one circular window of ≤ W values, or (D) the k_j take ≤ D distinct values.
Registered primary thresholds: **W ≤ 9, D ≤ 6**. The tool also lists W = 10 and D = 7 (WMAX 10, DMAX 6 on the command line, so the D
list is D ≤ 6 and the W list is W ≤ 10); width and pop are printed per survivor, so W ≤ 8 and D ≤ 5 are sub-counts. W = 10 is reported
as a descriptive scan only. Analytic chance (uniform shifts): W ≤ 9 ≈ 26·(9/26)^24 ≈ 2.2·10⁻¹⁰ per pair-form, so ≈ 5 cells per
2.26·10¹⁰ pair-forms; D ≤ 6 gives a few cells; the keyed alphabets are structured, so the empirical null counts, not these figures,
decide.

**Scopes.** A1 direct: X, Y ∈ the 86,731 alphabets (`alpha.bin`, sha 2b4ffb69…), all ordered pairs, 3 forms (2.26·10¹⁰ pair-forms).
A2 bank (165,065 rows × 2 dirs) and A3 all.bin (165,782 × 2 dirs): X, Y ∈ 144 themed (`themed144.bin`), all ordered pairs, 3 forms.

**Decode level (K4, nulls, plants).** For each survivor the allowed key set is the *observed* set of the 24 crib shifts for D, or the
minimal covering arc (all values of the window) for W; a beam search (width 3000, crib positions fixed, all other positions free over
the allowed set, mean log10 quadgram `qg.bin` over quadgrams that touch no crib position and have no '?') returns the best free-key
text. This is an *optimised* score, so it is compared only across K4 / nulls / plants under the same code (not against the
I-330 bar, which assumes a determined key); a plant counts as read if the beam text equals the plaintext at ≥ 90 % of the non-crib
positions or scores at least the true plaintext's score. The best text of any K4 survivor is printed and judged for English by eye.

**Gates.** P (plants, seed 209576, `plant230.py`): 20 plants, i.i.d. keys from a window (W 5–9) or from a D 3–6 value set, 10 direct
(X, Y from alpha.bin; tool run with xstride 86,731, xoff = true X) and 10 behind a random bank / all.bin row (themed X, Y; tool on a
101-row slice). Pass: ≥ 19/20 recover the true (row, dir, X, Y, form) (or its inverse twin) as a survivor, reported with the Wilson
95 % interval. R (recount): an independent Python re-derivation of the width / pop of every K4 and null survivor and of 3,000 random
non-survivors (0 mismatches).
**Nulls.** 10 fresh shuffled K4 (`random.Random(209577 + i)`), null i on the sub-slice X ≡ i (mod 20) (direct) or rows ≡ i·2 (mod 20)
(bank, all.bin): 1/20 scale; null-equivalent cells = count × 20.

**Labels (as in cases 200 / 202).** Per scope and criterion (W ≤ 9, D ≤ 6): K4 0 cells with null-equivalent ≥ ~1 chance cell →
`EXACT-EXCL` (discriminating; scope exactly the listed alphabets, one-crib-error NOT covered); K4 0 with null-equivalent 0 in
every null → `INSUFFICIENT-DISCRIMINATION` for that criterion (a zero is not informative about power); K4 > 0: cluster rule I-291
(same X, Y, form, row; single-linkage ≥ 16/24 map agreement; inverse twins merge), decode level as above, label `NO-SIGNAL` if the
K4 cluster count lies in the null band and decodes to gibberish. A successful plant validates recovery only within the scope above.
Heavy compute ≈ 9 min wall total (`timeout`, owned process group).

## Part B (news, desk, notes)
News check and the Voynich desk's recent public files integrated in the case file with attribution.
