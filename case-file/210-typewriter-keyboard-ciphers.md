# Case 210 — Typewriter keyboard ciphers (cycle 224, new family I-323)

> *Sanborn typed. Every typist owns a second alphabet, three rows deep, QWERTY on top. Nobody in this office had ever asked K4 whether it was written on one. Tonight I asked it with the cribs, four keyboards, three ways to move a finger, and twenty-four periods. It said no wherever the question could be heard.*

**Slot:** new family (222 free, 223 audit; I-319 / I-321). Pre-registered in [PREREG224](../tools/cycle224/PREREG224.md)
(local commit 3d252b5, 07:46 PT 2026-11-20) before any K4, plant or null run (first run 07:48 PT). Two corrections to the
filed text, made in the results commit: its header said "~08:05 PT" by a typo (the commit time is 07:46 PT), and its "next free seed
209437" became 209537 because of the post hoc 100-null check below (seeds 209437–209536). Code: [`tools/cycle224/`](../tools/cycle224/)
(`layouts224.py`, `kb224.c`, `plant224.py`, `gate224.py`, `run224.sh`, `summarize224.py`); results: [`data/cycle224/`](../data/cycle224/)
(`SHA256SUMS`, `MANIFEST.txt`, `labels224.json`).

## Why new
No case file mentions a keyboard / QWERTY, and none of the 86,731 alphabets of `alpha.bin` or the 144 of `themed144.bin` is a keyboard
order (QWERTY, QWERTZ, AZERTY, Dvorak rows or columns, or their reversals: all absent, checked before the prereg). The idea is
geometric (which key sits next to which), not another key stream on the existing alphabets.

## What was tested
Four layouts (US QWERTY, QWERTZ, AZERTY, Dvorak; letters only, physical key index per row). One crib error tolerated everywhere
(hit = at most one of the 24 crib seats has to be dropped; exact = 24/24). Transposition model as cases 200–209 (layer letter at
plaintext position i carved at S[i], S = row or its inverse), key index on plaintext (ix 0) or carved (ix 1) position.

| model | what it covers | per transposition |
|---|---|---|
| **G** | any substitution that keeps a letter in its keyboard **row**, its **column** (colA: same key index) or its column read with the opposite half-key stagger (colB), with **any key** (periodic, progressive, running, random): keyboard row-shift / column-shift ciphers of every kind | 12 (4 layouts × 3 partitions) |
| **V** | keyboard vector shift: (row, column) on a 3 × 10 torus moved by a key vector (dr, dc), periodic p 1–24 | 4 layouts × 2 ix |
| **Q** | tableau on keyboard alphabets: 16 keyboard alphabets (rows L→R, rows R→L, columns down, columns up, per layout) + A–Z / KA, all 320 ordered pairs except the four A–Z / KA ones, Vig / variant / Beaufort, any periodic key p 1–24 | 960 × 2 ix |

Scopes: direct; behind the 165,065 bank and the 165,782 K3-law decimations / routes (`all.bin`), both directions.
Q behind the bank alone is 6.3 × 10⁸ configuration-forms × 24 periods.

## Gates
- **Gate P (seed 209416): 20/20 PASS** (6 G, 4 V, 10 Q; 7 direct, 7 bank, 6 all.bin; odd ids with one wrong carved crib letter;
  periods 7–20). Re-run with the final binary (which only adds decrypt scoring): identical, 20/20.
- **Counts invariance:** the scored binary reproduces the S / T lines of the heavy run byte for byte (direct, bank, all.bin).

## Results (K4 vs shuffled-K4 nulls)
Nulls: 20 shuffles (seeds 209417–209436) direct (G / V / Q) and bank + all.bin (G, every row); 209417–209419 bank + all.bin V / Q on
every 10th row; 209418–209419 also on every row.

| model | scope | K4 | nulls | label |
|---|---|---|---|---|
| G (all 12 layout × partition cells) | direct / bank / all.bin | **0** | 0 in all 20 nulls, every cell | **EXACT-EXCL** (36/36 cells) |
| V | direct | 0, p 1–24 | 0 | **EXACT-EXCL p 1–24** |
| Q | direct | 0, p 1–24 | 0 | **EXACT-EXCL p 1–24** |
| V | bank | 0 at p 1–19 | 0 (full-scale nulls 0 at p ≤ 19) | **EXACT-EXCL p 1–19** |
| V | bank | p 20: 8, 21: 70, 22: 408, 23: 5,986, 24: 7,278 | full nulls p 20: 0 / 4; p 21: 56 / 42; 1/10 × 10: 400–7,210 at p 22–24 | INSUFFICIENT-DISCRIMINATION p 20–24 |
| V | all.bin | 0 at p 1–18 | 0 | **EXACT-EXCL p 1–18** |
| V | all.bin | **p 19: 4** | 0 in 2 full + 3 tenth-row nulls | see below (post hoc: `NO-SIGNAL`) |
| V | all.bin | p 20: 0, 21: 48, 22: 1,620, 23: 5,616, 24: 25,932 | full p 20: 12 / 6, p 21: 30 / 24; tenths alike | INSUFFICIENT-DISCRIMINATION p 20–24 |
| Q | bank | 0 at p 1–17 | 0 (full nulls 0 at p ≤ 17) | **EXACT-EXCL p 1–17** |
| Q | bank | p 18: 0, 19: 462, 20: 962, 21: 13,024, 22–24: 1.2 × 10⁵–1.8 × 10⁶ | full p 18: 2 / 4, p 19: 298 / 228, p 20: 920 / 784, p 21: 17,630 / 12,210 | INSUFFICIENT-DISCRIMINATION p 18–24 |
| Q | all.bin | 0 at p 1–16 | 0 | **EXACT-EXCL p 1–16** |
| Q | all.bin | p 17: 2, 18: 36, 19: 184, 20: 2,774, 21: 14,066, 22–24 up to 6.2 × 10⁶ | full p 17: 2 / 4, p 18: 36 / 8, p 19: 172 / 118, p 20: 2,422 / 2,232 | INSUFFICIENT-DISCRIMINATION p 17–24 |

**Resolution caveat (stated, not hidden):** the PREREG224 rule asks for an expected null count < 0.05 per text. At the edge periods
(V bank p 17–19, V all.bin p 16–18, Q bank p 15–17, Q all.bin p 14–16) only 2 full-scale nulls (+ 3 at 1/10) were run, so "null 0"
there bounds the rate only loosely; the next period up is already non-zero in the nulls. The edge cells are `EXACT-EXCL` by the
pre-registered rule but should be read as marginally discriminating; below the edge the null counts keep falling (they grow ≈ 5–15× per period step from p 17 to p 20 in
Q all.bin), so the lower periods are well inside the discriminating range.

### The one K4-only cell: V, all.bin, p 19 (post hoc check)
4 hits = one crib test: `all.bin` rows 8314 / 8315 (the same carving order, read in its two directions) × QWERTY / QWERTZ (same
geometry except Y ↔ Z, neither involved), ix 1, one dissenting seat. Its crib-key decrypt (88 known letters) scores −6.99 / −7.21
(gibberish, e.g. `MFJM?RTJIXAFKWZYZGAH?EASTNORTHEASTCOZYV…`). Post hoc (not pre-registered; flagged as such), 100 more shuffles
(seeds 209437–209536) on V all.bin: at p 19, 89 nulls have 0 hits, 8 have 2, **3 have 4** → raw rank p = 4/101 = 0.040; counted as
distinct crib tests (the duplication above is structural, two rows × two layouts) **11/100 nulls have ≥ 1 test** → p ≈ 0.12, and
this is one cell out of 2 models × 3 scopes × 24 periods. Label: **`NO-SIGNAL`** (chance level after the D2-style collapse, decrypt
far below the bar).

### Decrypts (pre-registered bar: ≥ 49 known letters and mean log10 quadgram ≥ −6.0)
Every V / Q hit was decrypted in C (`kb224.c` with `qg.bin`, sha256 4a02ba4e…). The bar is passed by **270** K4 hits behind the bank
and **812** behind all.bin, all at p 21–24, all gibberish by inspection (best −5.21, V p 24: `KRJ?PKR?HWELW?W?WEAJ?EASTNORTHEAST?IQKYP…`).
The same bar on null 209417 (1/10 rows) gives 27 and 91, i.e. ≈ 270 and ≈ 910 at full scale: **K4 is at the null rate.** The
−6.0 bar, set for case 209's period-20/21 cells, is too loose at p 22–24, where a free key class fits almost anything and the 24 crib
letters lift the mean; no hit is a candidate. Label for p 21–24: `NO-SIGNAL` (and `INSUFFICIENT-DISCRIMINATION` at the count level).

Heavy wall: 94 s (K4 + 20 nulls) + 85 s (scored K4 + scored null) + 141 s (two full-scale nulls) + 89 s (post hoc 100 nulls, V
only) ≈ 6.8 min, inside `setsid timeout` process groups (07:48–08:00 PT).

## Labels
- **G — keyboard row / column preserving substitutions with any key: `EXACT-EXCL`** direct, behind the bank and behind all.bin,
  four layouts, one crib error tolerated (needs ≥ 23 of 24 crib seats in the crib letter's row / column; K4 meets this nowhere).
- **V — keyboard vector shift, periodic: `EXACT-EXCL`** direct p 1–24, bank p 1–19, all.bin p 1–18; above that
  `INSUFFICIENT-DISCRIMINATION`; all.bin p 19 `NO-SIGNAL` (post hoc rank above).
- **Q — periodic tableau on keyboard alphabets: `EXACT-EXCL`** direct p 1–24, bank p 1–17, all.bin p 1–16; above that
  `INSUFFICIENT-DISCRIMINATION` / `NO-SIGNAL`.

## Blind spots
Only these four layouts (no typewriter-specific layouts such as the 1980s IBM Selectric or Blickensderfer, no numeric-row letters,
no shifted symbols); only the stated 16 keyboard alphabets (no keyword-mixed keyboard alphabets, no diagonal reads); V uses one
torus convention (3 × 10, colA) — other "move the finger" rules (stagger-aware diagonals, row wrap into the next row) are only
covered when they keep the row or column (G) or equal a keyboard-alphabet Caesar step (Q with R1 = row-wrapping shift); periodic
keys only for V / Q; same two transposition families; one error at most.

## Verdict
No solution. K4 was not typed through a keyboard-geometry substitution in any of the discriminating scopes above.

## Voynich exchange (this cycle)
The Voynich desk's independent D2 / D3 recount of case 209 (voynich-case-files b15523f…41a3ad8, frozen 04:44:52 PT) reproduced all
170 result files and every count (K4 99 vs null median 114, p_up 0.627; raw p 0.0414) and answered I-322: D3 adds nothing, and no
collapse changes the zero / non-zero null pattern at p 17–19 (null occupancy 27 % / 54 % / 60 % for w 9–10). Integrated into IDEAS
I-322 as `[external audit]`, not re-run by us.

## Addendum (cycle 225, 2026-11-20): the Voynich desk's open recount of the V all.bin p 19 cell
The Voynich desk published an open recount at voynich-case-files `b0793db` + `0128be8` (`audits/kryptos/c210-v-recount/`,
2026-11-20 08:12–08:15 PT; rule `RULE.md` sha256 3b94f944…40d24 and counts `FROZEN.txt` 5a65fbe8…85fed hashed before she opened our
labels, journal, case file or `summarize224.py`). She reran the 100 post hoc nulls (209437–209536) with her own printer
`kb224_p19.c`: all 100 published `S V p=19` lines match. Her counts: occupancy **11/100** (p 12/101 ≈ 0.12), raw rank 4/101 ≈ 0.040,
and K4's 4 raw hits are **2 distinct tests**, not one: rows 8314 / 8315 are exact inverses and collapse, but **QWERTY and QWERTZ do
not** — their K4 decrypts differ in 16 of 97 letters, because crib seats 14 and 21 sit on carved **Z** (K4 positions 46 and 78).
**Correction:** the sentence above "same geometry except Y ↔ Z, neither involved" is wrong; Z is involved (our own scores −6.99 vs
−7.21 for the two layouts already showed the decrypts differ). Null 209438 has two independent families; only nulls 209501 and 209530
show K4's layout-pair pattern.
**Verified here (cycle 225):** the published files hash to the values her README states; K4 carries Z at 46, 47, 70, 78 (0-indexed).
The 16/97 letter difference is taken from her recount, not recomputed. **Label:** `NO-SIGNAL` stands, on occupancy 11/100 (which does
not depend on the layout collapse). The rank on distinct tests is 0.040 if the layouts stay distinct, 0.12 if they are forced
together; either way one cell out of 2 models × 3 scopes × 24 periods, decrypt gibberish. Leaks as in her `LEAKS.md` (our message had
already given raw p 0.040 and occupancy 11/100). **No label changes.**
