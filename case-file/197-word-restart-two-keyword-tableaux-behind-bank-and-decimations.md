# 197 — Word restart on two-keyword Quagmire tableaux, behind the bank and behind the K3-law decimations (cycle 210)

> *Cases 193 and 195 put the word-restart clerk behind both closets, but only with the two drawers everybody owns, the straight alphabet and the KRYPTOS one. K1 and K2 were built from words. So tonight I gave him eight words to cut his alphabets from: the keys of K1 and K2, the misspelled IQLUSION, the last words of K2, the clock. Sixty-two pairs of drawers, two ways to turn the tableau, two closets. Nothing fits below sixteen letters of key. At sixteen, one configuration fits behind a decimation, and its plaintext reads like a typewriter falling down the stairs.*

**IDEAS:** I-270 + I-276 (pointer I-282; new-family slot). **Pre-registration:** [`tools/cycle210/PREREG210.md`](../tools/cycle210/PREREG210.md),
local commit `a187f23` (2026-11-13 07:53 PT; sha256 5853f316…), before any registered run.
**Code:** [`wrq.c`](../tools/cycle210/wrq.c) (OpenMP C, generalises cycle 206's `wrbank.c`), [`plant210.py`](../tools/cycle210/plant210.py)
(independent encoder), [`run210.sh`](../tools/cycle210/run210.sh), [`run210_plantfix.sh`](../tools/cycle210/run210_plantfix.sh),
[`check_plants.py`](../tools/cycle210/check_plants.py), [`supp210.sh`](../tools/cycle210/supp210.sh) (descriptive supplement).
**Results:** [`data/cycle210/`](../data/cycle210/) (`results210_family.json` sha256 f803a1d2…, K4 survivor lines, plant check, survivor read-out).

## Why this (labelled)
- **Fact:** [case 193](193-word-restart-two-alphabets-and-behind-bank.md) and [case 195](195-word-restart-behind-decimations.md) excluded R1
  (key index = position inside the plaintext word, mod L) behind the 165,065 bank and behind the 165,782 K3-law decimations/routes at
  L ≤ 16, but only on the A–Z and KRYPTOS tableaux. Two different alphabets were tested only directly, by SAT, where the cribs
  run out of strength at L 5–11.
- **Inference (style, [case 10](10-style-profile.md) §5):** K1 and K2 key their tableau with a word, and K3 shuffles with a grid. "Word-keyed
  tableau + word-restart key + K3-style shuffle" is a three-ingredient K1–K3 composite. Keyword alphabets turn the SAT problem into an
  exact table check per pair. [Case 12](12-strips-and-periodic-keys.md)'s correction stands: nothing here rests on the strips.

## Model and scope
Plaintext enciphered on a Quagmire tableau (plain alphabet X, cipher alphabet Y, each a keyword then the rest of A–Z), Vigenère form
c = Y[x(p)+k] (variant has the same consistency and is counted once) or Beaufort form c = Y[k − x(p)]. Key index = position in the
plaintext word mod L, using case 190's 4 × 2 crib segmentations with free offsets o1, o2. Then model Q: layer letter i is carved at S[i], with S a bank
row or an `all.bin` row, both directions. **Alphabets (8):** AZ, KA, PALIMPSEST, ABSCISSA, SHADOW, IQLUSION, LAYERTWO, BERLINCLOCK.
**Pairs:** 62 ordered (X, Y), all except AZ/AZ and KA/KA (cases 193/195), × 2 forms = 124 tableau-forms (31× case 193's four).
Quagmire I (Y = AZ), II (X = AZ), III (X = Y keyed) and IV (X ≠ Y) are all included. **L 1–17.**

## Gates and controls
| Gate / control | Result |
|---|---|
| G0′: wrq with AZ/AZ + KA/KA reproduces `wrbank.c` on K4 behind the bank, L 1–20, per tableau-form | **pass**: identical (L 18 / 19 / 20 = 2 / 62 / 540; per-form 2·44·158 / 12·170 / 84 / 6·128) |
| Plants (seed 209214): 12 planted R1 Quagmire ciphers, L 12/14/16, 6 behind bank rows + 6 behind `all.bin` rows, 8 with non-zero offsets (o1 ≤ 9, o2 ≤ 14, o2 wrap mod L included), random pair/form/segmentation, independent encoder | **12 / 12 recovered** at the true (row, dir, pair, form, L, seg, o1, o2, key) → PASS (bar ≥ 11/12) |
| Nulls: 20 shuffled K4 (`random.Random(209213)`), each on a disjoint tenth of one family = 1 full-family null-equivalent per family | 0 survivors at every L ≤ 17 in both families |
| Descriptive supplement (not registered; seed 209215): 40 more tenth-nulls at L 15–17 | bank 20/20 tenths done (2 equivalents): L 15 0, L 16 0, **L 17 4**; `all.bin` 15/20 tenths (1.5 equivalents, cut by its 150 s cap): 0 / 0 / 0 |
| **Disclosures** | (1) The registered plant step failed: the slice writer sat in a quoted heredoc, so `$OUT` was not expanded and wrq segfaulted on missing files. The same hashed `plants.tsv` was rerun after the main run with the fix (`run210_plantfix.sh`); the plants were fixed before the run and nothing about them could adapt. (2) One pre-registration timing probe ran K4 on bank rows q ≡ 0 (mod 10), L 1–17: one survivor at L 17. This was disclosed in PREREG210, and those rows are inside the full run. (3) The supplement was decided after the registered run and is descriptive only. |

## Results (K4, full families, survivor cells; inverse twins counted separately)
| L | bank (165,065 × 2) | K3-law decimations/routes (165,782 × 2) | null-equivalents with any survivor |
|---|---|---|---|
| 1–15 | **0** | **0** | 0 (bank 3 eq., all 2.5 eq. at L 15) |
| 16 | **0** | **2** = one configuration (twin rows 83,548 / 83,549) | 0 |
| 17 | 2 = one configuration (twin rows 146,519 / 146,520) | 4 = the L 16 configuration extended (2 offsets × twins) | bank 4 cells in 2 of 3 eq.; all 0 |

**Read-out of the survivors** (letters decryptable without guessing word boundaries; [`survivor_readout.txt`](../data/cycle210/survivor_readout.txt)):
- `all.bin` 83,548 dir 0, X = IQLUSION, Y = BERLINCLOCK, Beaufort, EAST|NORTH|EAST + BERLINCLOCK, o1 2, o2 6, key RQUJZFIIHHHHUATR:
  `…MP·EASTNORTHEAST·ZEEWYOD…`, `…IUEPOC·BERLINCLOCK·DFPCOQL…`. It needs a word "MPEAST" and a word "IUEPOCBERLINCLOCK…". Gibberish.
- bank 146,520 dir 0, X = IQLUSION, Y = ABSCISSA, Beaufort, L 17, key VZPDQUJHTMQUNEMYP: `LEYYOODYBTGQBJ·EAST·NORTHEAST·JVCULOUK…`. Gibberish.

## Verdict
- **EXCLUDED (exact, under these assumptions), L 1–15, both families:** an R1 word-restart key of length 1–15 on any of the 62 two-keyword
  Quagmire tableaux built from the 8 registered words, Vigenère/variant or Beaufort, followed by any of the 165,065 bank transpositions or any
  of the 165,782 K3-law decimations/routes, either direction, for every case-190 segmentation and offset. Power: plants 12/12 (up to L 16); 0 null
  survivors at L ≤ 16 in 5.5 null-equivalents. The false-survivor rate is **extrapolated, not certified**: case 193's single-tableau E ≈ 0.005 at L 16
  × 31 tableau-forms ≈ 0.16 at L 16, and roughly one seventh of that (≈ 0.02) at L 15.
- **Bank, L 16:** K4 0, exact, but **not discriminating** by the registered rule (extrapolated E ≈ 0.16 > 0.05; zero null survivors in 3 equivalents
  does not certify a rate).
- **Decimations/routes, L 16:** **not excluded.** One configuration fits; its decryptable letters are gibberish → `NO-SIGNAL` (heuristic reading).
  K4 has 1 configuration where 2.5 null-equivalents had 0. That is descriptive only (n is small; P(≥ 1 | E ≈ 0.16) ≈ 15 %).
- **L 17:** `NO-DISCRIMINATION` (bank nulls reach 4 cells; K4's survivors gibberish).
- **Not tested:** the other 136 themed alphabets and the 10,056-word vocabulary (cost: ≈ 0.65 s per pair-form per family at L 1–17 on 8 threads, so the
  144² themed pairs × 2 forms × 2 families would take ≈ 15 h → a hash-join design is needed, I-284); keys longer than 17; one wrong crib letter; restarts other than word starts.
- **Compute:** registered run 5 min 33 s (G0′ 12 s, K4 2 × ≈ 80 s, nulls 160 s); plant fix 1 s; supplement 150 s (capped). Together with the case 196
  addendum (37 s), ≈ 8.7 min heavy, slightly over the ≈ 8 min budget because of the supplement.

**No solution; K4 status unchanged.**
