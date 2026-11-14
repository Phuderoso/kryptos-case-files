# 198 — Word restart on two-keyword Quagmire tableaux over all 144 themed alphabets, by hash join, behind the bank and the K3-law decimations (cycle 212)

> *Case 197 gave the clerk eight words to cut his alphabets from. Tonight I gave him the whole drawer: 144 themed alphabets, twenty thousand
> pairs, both ways to turn the tableau. Doing it pair by pair would take all night. So I sorted the alphabets by what they would have to say
> about the clue letters and matched them like fingerprints. Nothing fits below fourteen letters of key. Above that, the room fills up with
> strangers who fit for no reason. The shuffled ciphers fill it just as fast.*

**IDEAS:** I-284 (pointer I-286; new-family slot) + I-287 (audit add-on). **Pre-registration:** [`tools/cycle212/PREREG212.md`](../tools/cycle212/PREREG212.md),
local commit `83634a6` (2026-11-13 ~15:51 PT; sha256 3192376e…), before any registered run. Part B blind results committed in `fe71b46`
(~16:00 PT) before the sealed truths were opened.
**Code:** [`wrj.c`](../tools/cycle212/wrj.c) (OpenMP C, hash join; same model as `wrq.c`), [`run212.sh`](../tools/cycle212/run212.sh),
[`plant212.py`](../tools/cycle212/plant212.py), [`check212.py`](../tools/cycle212/check212.py), [`e212.py`](../tools/cycle212/e212.py),
[`readout212.py`](../tools/cycle212/readout212.py); part B [`blind212.py`](../tools/cycle212/blind212.py), [`score212b.py`](../tools/cycle212/score212b.py).
**Results:** [`data/cycle212/`](../data/cycle212/) (`results212_family.json` sha256 5c4ee7e9…, K4 survivor lines, per-batch nulls, read-out);
part B [`results212b_blind.json`](../tools/cycle212/results212b_blind.json) (sha256 4fb86603…), [`results212b_scored.json`](../tools/cycle212/results212b_scored.json).

## Why this (labelled)
- **Fact:** [case 197](197-word-restart-two-keyword-tableaux-behind-bank-and-decimations.md) tested R1 word restart on two-keyword Quagmire
  tableaux only for 8 K1–K3 words (62 pairs), because its per-pair loop costs ≈ 0.65 s per pair-form per family (≈ 15 h for 144²).
- **Fact (news, 2026-11-13):** kryptosbot.com's findings page still lists "repeating-key ciphers with two different keyword-mixed alphabets"
  as only partly tested in their frame. Our R1 word-restart slice is a different key schedule, but the alphabet question is the same.
- **Inference:** the consistency condition separates. Inside a key class, y(c_j) − y(c_j0) depends only on the cipher alphabet Y and the
  ciphertext letters, and x(p_j) − x(p_j0) depends only on the plain alphabet X and the cribs. So the pair loop becomes a join. That makes the
  full 144 × 144 table cost about 2 minutes per family instead of hours.

## Model and scope
As case 197: R1 (key index = position inside the plaintext word mod L), case 190's 4 × 2 crib segmentations, offsets o1, o2 ∈ 0..L−1, Quagmire
tableau (X plain, Y cipher, keyword alphabets), Vigenère form (variant counted once) and Beaufort form, then model Q behind the 165,065-row
bank or the 165,782-row K3-law decimations/routes (`all.bin`), both directions. **Alphabets:** the 144 themed alphabets
(`tools/cycle180/alpha_themed180.txt`). **Pairs:** 20,734 ordered (all but AZ/AZ and KA/KA) × 2 forms = **41,468 tableau-forms** (334× case 197).
**L 1–16.**

## Gates and controls
| Gate / control | Result |
|---|---|
| G0″ (I-283): `wrj` with case 197's 8 alphabets / 62 pairs on K4, both families, L 1–17 | **pass**: identical to case 197 (bank: 0 to L 16, L 17 2 = rows 146,519/146,520, key VZPDQUJHTMQUNEMYP; all: L 16 2 = 83,548/83,549, key RQUJZFIIHHHHUATR; L 17 4) |
| Dev equivalence (disclosed in PREREG): `wrj` vs `wrq` on one shuffled K4, bank q ≡ 3 (mod 20), L 1–20 | H, P and all 880 S lines identical |
| Plants: case 197's 12 (seed 209214) + 8 new (seed 209218; X, Y from the 136 alphabets outside the 8 words; L 8–16; 3 with BERLINCLOCK indices wrapping mod L) | **20 / 20** recovered at the true (row, dir, X, Y, form, L, seg, o1, o2, key) → PASS (bar ≥ 19/20; Clopper–Pearson 95 % 0.83–1) |
| Nulls: 20 shuffled K4 (seed 209219), each on a disjoint tenth (one null-equivalent per family) | see per-batch table |

## Results (K4, full families, survivor cells; inverse twins counted separately)
| L | analytic E per family | bank K4 | bank null-equivalent: pooled (per batch) | all.bin K4 | all.bin null-equivalent: pooled (per batch) | label |
|---|---|---|---|---|---|---|
| 1–12 | < 2·10⁻⁴ | **0** | 0 (all 0) | **0** | 0 (all 0) | `EXCLUDED (exact)`, discriminating |
| 13 | 0.003 | **0** | 0 (all 0) | **0** | 0 (all 0) | `EXCLUDED (exact)`, discriminating |
| 14 | 0.069 | **0** | 0 (all 0) | **0** | **1** (0,0,0,0,0,0,0,0,1,0) | bank `UNRESOLVED` (E inside the I-281 band); all.bin `zero, not discriminating` |
| 15 | 1.6 | **0** | 0 (all 0) | **2** = 1 configuration | 0 (all 0) | bank `zero, not discriminating` (E > 0.1); all.bin `NO-SIGNAL` |
| 16 | 36 | 40 | 40 (1, 19, 3, 2, 2, 4, 3, 2, 2, 2) | 34 | 25 (2, 0, 4, 2, 1, 2, 4, 2, 5, 3) | `NO-DISCRIMINATION` both |

**Survivor split (the obligation agreed with the Voynich desk).** *Identical input* (pairs inside case 197's 8-word slice, same family files,
same solver semantics as G0″): **all.bin L 16, 2 cells (rows 83,548/83,549)**, which is exactly case 197's NO-SIGNAL configuration. Bank: 0. *Changed input*
(the new pairs): bank L 16 40; all.bin L 15 2, L 16 32. **No bar moved:** every label uses the rule and the E values written in PREREG212 before the K4 run.
**Data change:** only the alphabet list (8 → 144); the families, segmentations and K4 text are unchanged.

**Read-out** ([`survivor_readout.txt`](../data/cycle212/survivor_readout.txt); upper case = letters forced by the configuration, lower case =
heuristic continuation of the last crib word):
- **L 15, all.bin 125,900 dir 0** (twin 125,901), X = WONDERFUL/Z, Y = A–Z (a Quagmire I), Beaufort, EASTNORTHEAST + BERLIN|CLOCK, o1 0,
  o2 11, key HYYWRQXIDKIFCPU. It needs a word "HPVIJVBAZRWBERLIN", which is gibberish → `NO-SIGNAL` (heuristic). E ≈ 1.6 at L 15, so one configuration is at chance level.
- **L 16:** 8 distinct (pair, key) configurations on the bank and 14 on all.bin. Rows come in near-equivalent clusters: for example,
  ANTIPODES/INTERPAU with key JLGWAHAHMIFDPXPG sits on 24 bank cells over 12 rows. Every forced prefix is gibberish, for example
  "DUSAIYOF·EAST", "MNTY·EAST", "HBDXTCX·EAST", "…JQEURBMD·BERLIN". The null per-batch range scaled to a full family (0–190) contains both
  K4 counts → `NO-DISCRIMINATION`.

## Part B — I-287 audit: 10 blind wrapped-offset plants behind the bank (Voynich desk)
- **Input (her encoder, her seed 11784):** W01–W10. R1 on AZ/KA × Vig/Beau, L 16, bank rows drawn uniformly from the non-identity rows,
  BERLINCLOCK unsplit with **o2 ∈ {6, 7, 8}** (key indices wrap mod 16), o1 0–8, English filler. Ciphertexts sha256 1d970041…; sealed truths
  sha256 c0e20249… (**checked on opening: match**).
- **Blind run:** `wrbank.c` **unchanged** (sha256 1001272d…) on the full bank, L 16, all survivors printed, 4.7 s. Results sha256 4fb86603…, committed
  in `fe71b46` before opening.
- **Scored:** **10 / 10 recovered** at the true (perm, dir, tm, L 16, segE, BERLINCLOCK, o1, o2) with the planted key → **gate PASS** (≥ 9/10;
  Clopper–Pearson 95 % 0.69–1). Undetermined key indices per true line: 0–2 (a *count*).
- **Line classes** (the stricter accounting the desk asked for): other than the true row, lines fall on the inverse twin (same map), on **crib-equivalent**
  rows (maps equal on all 24 crib positions; agreement over 97 positions 48–73) or on **other** rows. Other rows appear for W02 (12 rows / 36 lines),
  W05 (432 / 8,220) and W09 (240 / 240). Every one of them is a **near-equivalent** row whose map agrees with the true map on **19–23 of the 24 crib
  positions**. None is a random false survivor. The bank's row neighbourhoods are dense (I-291).
- **Reading:** the case 193 bank exclusion (L ≤ 16) is now plant-validated on wrapped BERLINCLOCK offsets too (10/10, independent encoder).
  Credit: the plant design, encoder and sealed truths are the Voynich desk's (box-local `voynich/kryptos-audits/case194-wrapped-plants/`).

## Verdict
- **EXCLUDED (exact, under these assumptions), L 1–13, both families:** R1 word-restart key of length 1–13 on any two-keyword Quagmire tableau
  from the 144 themed alphabets (all 20,734 ordered pairs other than AZ/AZ and KA/KA; Quagmire I–IV), Vigenère/variant or Beaufort, behind any
  of the 165,065 bank transpositions or the 165,782 K3-law decimations/routes, either direction, every case 190 segmentation and offset.
  Discriminating: analytic E ≤ 0.003 per family, and one null-equivalent per family had 0 cells. Power: plants 20/20, at L 8–16.
- **L 14:** K4 0 in both families; bank `UNRESOLVED` (E 0.07), all.bin `zero, not discriminating` (1 null cell).
- **L 15:** bank zero, not discriminating; all.bin 1 configuration, gibberish (`NO-SIGNAL`).
- **L 16:** `NO-DISCRIMINATION` (K4 40 / 34 vs nulls 40 / 25).
- **Not tested:** vocabulary alphabets (10,056 words; the join makes X from vocabulary × Y themed about 70× this run per family, I-290), L ≥ 17,
  one wrong crib letter, and restarts other than word starts.
- **Compute:** part A 6 min 41 s wall (G0″ 14 s, plants 4 s, K4 bank 92 s, K4 all 95 s, nulls 196 s); part B 5 s. Total ≈ 6.8 min.

**No solution; K4 status unchanged.**

## Addendum 1 (cycle 214) — L 15 Poisson tail (Voynich desk, credit)
The desk computed the chance of case 198's one all.bin L 15 line (2 cells = 1 inverse-twin configuration, key HYYWRQXIDKIFCPU) in
`kryptos-audits/case198-L15-poisson/` (own code, no solver rerun; null shuffles and per-tenth counts reproduced exactly). Under the
preregistered analytic E = 1.6134 cells: P(N_cells ≥ 2) = 0.479, P(N_config ≥ 1) = 0.554; calibrated to the L 16 null/E ratio:
0.308 / 0.428. Zero null cells in 10 tenths only bound the rate (λ_U 3.0 at 95 %), they do not make one line rare. Caveats: inverse
twins cannot re-form across tenths, and bank L 16 tenths are overdispersed. **Reading: the L 15 line is at chance; `NO-SIGNAL`
stands.** Verified here only by re-reading her inputs and hashes, not by recomputation.
