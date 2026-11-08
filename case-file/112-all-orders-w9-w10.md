# 112 — Every column order of width 9 and 10, behind a periodic key (cycle 124)

**Why.** Cycle 123's audit found that the 165,065-transposition bank stops at width 8: "behind the bank" never meant an arbitrary 9- or 10-column order. Cycle 123 closed *themed keyword* orders w 9–13; this cycle closes **all** orders of width 9 and 10, so a keyword nobody guessed (or a non-word order) no longer hides there. Ten columns is also the width of K3-style 10-letter keys (PALIMPSEST) and of the Nihilist square (cycles 50–51).

**What was tested (exact, `tools/cycle124/allcol.c`).**
- Transposition: all 9! + 10! = 3,991,680 column orders on the ragged 97-letter grid, rotation 0; read by columns (textbook columnar) or by rows with permuted columns; both directions (σ and σ⁻¹). ≈ 1.6 × 10⁷ transpositions.
- Substitution: periodic key p 1–18 (exact claim) and 19–22 (scored), A–Z or KRYPTOS tableau, Vigenère/Beaufort (variant ≡ Vigenère for consistency), key before (plaintext index) or after (carved index) the transposition.
- Test: all 24 crib letters (EASTNORTHEAST 21–33, BERLINCLOCK 63–73, 0-based) consistent with one key.

**Controls.** Four planted messages built by an *independent* textbook encryptor (`plant.py`): PALIMPSEST columnar + KRYPTOS key (KA, p 7, key first); LODESTONE columnar then Beaufort SHADOWFORCE (p 11, key after); UNDERGRUND row read then ABSCISSA (p 8); inverse NORTHEAST columnar after a 16-letter KA key. **4/4 recovered** at their true order, mode, direction, alphabet and period (p 16 control: the true order is one of 24 survivors that differ only in crib-free columns). Decrypts read back the planted text at −4.1 to −4.3 per quadgram.

**Results.**

| Text | p 1–18 survivors | p 19–21 | p 22 | best p 22 score |
|---|---|---|---|---|
| K4 | **0** | 0 | 720 | −6.45 |
| null1 | 0 | 4 | 144 | −6.30 |
| null2 | 0 | 2 | 60 | −6.82 |
| null3 | 0 | 0 | 132 | −6.74 |

English is about −4.2 to −4.7 on this scale. K4's raw p 22 count looked high against the first three nulls, so seven more shuffled nulls (seeds 128–134) were run at p ≤ 22 and survivors were collapsed to crib-distinct configurations (same carved positions for the 24 crib letters): K4 has **242**, the ten nulls 0, 2, 4, 14, 29, 62, 98, 99, 148, 316. K4 ranks 2nd of 11, inside the null spread, and every K4 decrypt is unreadable. Not a lead ([`results.txt`](../data/cycle124/results.txt)).

**Verdict (fact, for this family).** No column order of width 9 or 10 (column or row read, either direction) combined with a periodic Vigenère/Beaufort/variant key of period ≤ 18 on the A–Z or KRYPTOS tableau, key before or after, produces K4. Periods 19–22 are crib-underdetermined and their fits are at null level and unreadable.

**Still open.** Widths 11–13 with arbitrary orders (11! = 4 × 10⁷: feasible next, ~10 min split over cycles); mixed (non-tableau) alphabets behind w 9–10; running key / autokey behind w 9–10; double columnar with one w ≥ 9 leg.

Data: [`data/cycle124/`](../data/cycle124/). Journal: [cycle 124](../journal/2026-11-08-cycle124.md).
