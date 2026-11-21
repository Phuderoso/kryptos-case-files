# Case 213 — The wider keyboard family: DHIATENSOR, keyword keyboards, stagger moves (cycle 227, new family I-327 chunk 1)

> *Case 210 asked K4 about the four keyboards everybody owns. Tonight I asked about the one hardly anybody owned — Blickensderfer's
> "Scientific" board, DHIATENSOR on the home row — and about a QWERTY board re-lettered with KRYPTOS, PALIMPSEST and ABSCISSA, the
> way K1–K3 re-letter an alphabet. The plants all came home. K4 didn't answer.*

**Slot:** new family (I-333: 226 audit, so 227 must be a new family among I-299, I-313, I-327). Pre-registered in
[PREREG227](../tools/cycle227/PREREG227.md) (local commit, 19:49 PT 2026-11-20) before any K4, plant or null run. Code:
[`tools/cycle227/`](../tools/cycle227/) (`layouts227.py`, `kb227.c`, `plant227.py`, `gate227.py`, `run227.sh`, `run227b.sh`,
`summarize227.py`); results: [`data/cycle227/`](../data/cycle227/) (`SHA256SUMS`, `MANIFEST.txt`, `summary227.json`).

## Why this family, and why now
I-327 was the case 210 blind-spot list: no typewriter-era layout beyond the four modern ones, no keyword-mixed keyboard, one torus
convention. It is chosen over I-299 (other digit bases: a parameter sweep of case 200 whose null rate explodes for b > 10, while
b < 10 is a subset of the base-10 keys already excluded) and I-313 (PK8 / PK9 calibration: a tool check, not a K4 test, and its
sources still need verification). The K1–K3 habit — a meaningful keyword re-ordering an alphabet — is moved onto a keyboard grid.

**Novelty check (`layouts227.py`):** 22 candidate keyboard alphabets; 4 dropped (the plain keyed rows KRYPTOS / PALIMPSEST /
ABSCISSA are already in `alpha.bin`; one DHIATENSOR column read is a duplicate). The 18 kept are in none of `alpha.bin` (86,731),
`themed144.bin`, `kb224.bin`. The eight geometries are new to the repo.

## What was tested
| geometry | rows (key index) | source |
|---|---|---|
| DHIA-W | `PWFULCMY` (1–8) / `DHIATENSOR` (0–9) / `ZXKGBVQJ` (0–7) | keyboard wiki, "DHIATENSOR" (ANSI mapping) |
| DHIA-M | `ZXKGBVQJ` (1–8) / `PWFULCMY` (1–8) / `DHIATENSOR` (0–9) | Blickensderfer No. 5 manual: split "between G U T and B L E" |
| KRYPTOS-QW, PALIMPSEST-QW, ABSCISSA-QW | keyed alphabet in the QWERTY slots 10 / 9 / 7 | K1–K3 keywords |
| QWERTY-S, QWERTZ-S, AZERTY-S | case 210 layouts, column = staggered column (row 2 half a key right) | stagger-aware finger move |

Models as case 210 (`kb227.c` = `kb226.c` + the tie rule; counting byte-identical): **G** row / column keeping substitution with
any key; **V** periodic vector shift on the 3 × 10 torus (p 1–24, key on plaintext or carved index); **Q** Vig / variant / Beaufort
tableau on the 20 alphabets of `kb227.bin` (18 new + A–Z + KA; 396 ordered pairs), periodic p 1–24. One crib error tolerated.
Scopes: direct, behind the 165,065 bank rows and the 165,782 `all.bin` rows, both directions.

## Gates
- **Gate T: PASS.** `kb227` and `kb226` give byte-identical S / T lines on `geo224` + `kb224` (K4, bank, every 10th row).
- **Gate P (seed 209548): 20/20 PASS** (G 4, V 7, Q 9; 7 direct, 7 bank, 6 all.bin; 10 with one wrong carved crib letter; p 3–24).
  Decrypt bar: **16/16** found V / Q plants have NC ≥ −6.0 under tie = '?' (range −3.83 to −4.89; known 69–97). G hits have no
  decrypt (any key), as in case 210.

## Results (K4 vs shuffled-K4 nulls)
Nulls: the 20 published case 210 shuffles (209417–209436): direct (GVQ / GV) and G behind bank / all.bin at full scale; the first 12
behind bank / all.bin for V / Q on every 10th row, compared with K4 on the same rows. No new null seeds.

| model | geometries | scope | K4 | nulls | label |
|---|---|---|---|---|---|
| G | DHIA-W, DHIA-M, KRYPTOS-QW, PALIMPSEST-QW, ABSCISSA-QW (× row / colA / colB) | direct / bank / all.bin | **0** | 0 in all 20, every cell | **EXACT-EXCL** (45/45 cells) |
| V | geo a (DHIA-W/M, KRYPTOS-QW, PALIMPSEST-QW) | direct | 0, p 1–24 | 0 | **EXACT-EXCL p 1–24** |
| V | geo b (ABSCISSA-QW, QWERTY-S, QWERTZ-S, AZERTY-S) | direct | 0, p 1–24 | 0 | **EXACT-EXCL p 1–24** |
| Q | 18 new alphabets + AZ / KA | direct | 0, p 1–24 | 0 | **EXACT-EXCL p 1–24** |
| V | geo a | bank | 0 at p 1–18 | 0 (r10) | **EXACT-EXCL p 1–18** |
| V | geo a | bank | p 19: 2, p 20: 2 (r10: 0, 0) | 0 / 12 at r10 | K4-only, see below → `NO-SIGNAL` |
| V | geo a | bank | p 21–24 (r10 1, 33, 663, 705) | occupancy 11–12 / 12, p_up 0.54–0.92 | INSUFFICIENT-DISCRIMINATION |
| V | geo b | bank | 0 at p 1–19 | 0 (r10) | **EXACT-EXCL p 1–19** |
| V | geo b | bank | p 20–24 | p 20 occ 2/12; p 21–24 occ 10–12 | INSUFFICIENT-DISCRIMINATION |
| Q | kb227 | bank | 0 at p 1–16 | 0 (r10) | **EXACT-EXCL p 1–16** |
| Q | kb227 | bank | p 17–24 (r10 0, 9, 52, 73, 1,931, …) | occ 4–12 / 12; p 18 p_up 0.077 | INSUFFICIENT-DISCRIMINATION |
| V | geo a | all.bin | 0 at p 1–19 | 0 at p ≤ 18; p 19 one null hit | **EXACT-EXCL p 1–18**; p 19 K4 0 (no claim beyond K4 0) |
| V | geo a | all.bin | p 20–24 | occ 9–12 / 12 | INSUFFICIENT-DISCRIMINATION |
| V | geo b | all.bin | 0 at p 1–19 | 0 (r10) | **EXACT-EXCL p 1–19** |
| V | geo b | all.bin | p 20–24 | occ 2–12 / 12 | INSUFFICIENT-DISCRIMINATION |
| Q | kb227 | all.bin | 0 at p 1–15 | 0 (r10) | **EXACT-EXCL p 1–15** |
| Q | kb227 | all.bin | p 16: 4 (r10 0) | 0 / 12 at r10 | K4-only, see below → `NO-SIGNAL` |
| Q | kb227 | all.bin | p 17–24 | occ 7–12 / 12, p_up ≥ 0.15 | INSUFFICIENT-DISCRIMINATION |

G on the three -S layouts repeats case 210's partitions (printed, not labelled; K4 0 there too).

**Scale caveat (stated, as in case 210):** behind bank / all.bin the V / Q nulls are 12 tenth-row runs (≈ 1.2 full-null
equivalents), so "null 0" in the top two or three periods of each EXACT-EXCL range behind bank / all.bin bounds the null
rate only loosely; the next period up is already non-zero. Edge cells are `EXACT-EXCL` by the registered rule but marginally
discriminating; below them the null counts keep falling.

### The K4-only cells (manual read, D2)
Each is a pair of exactly inverse rows (n, n + 1 read in the two directions) giving the same decrypt, so D2 counts are half the raw.
- **V bank p 19** (rows 147755 / 147756, KRYPTOS-QW, carved index): **1 distinct test**, NC −7.94 (known 83):
  `IS?GGQ?JTWUPRIHXG?BHCEAS?NORTHEASTBD?JUW?JVSXCXC?P?UJPMQ?E?BGETBERLINCL?CK…`
- **V bank p 20** (rows 147223 / 147224, KRYPTOS-QW, carved index): **1 test**, NC −8.29 (known 86).
- **Q all.bin p 16** (rows 15064 / 15065: X = A–Z, Y = KRYPTOS-QW-R2, Beaufort; rows 134838 / 134839: X = KRYPTOS-QW-R2,
  Y = KRYPTOS-QW-C2, Beaufort): **2 tests**, NC −8.16 / −7.89 (known 91).
All four tests are gibberish and far below the bar. Each cell sits one period below the first period at which the nulls start
hitting; with 12 tenth-row nulls their full-scale rate is unmeasured (follow-up I-337). These involve the KRYPTOS keyboard, so they
are listed by name, but nothing in them reads. Label: **`NO-SIGNAL`**.

### Decrypts — I-330 bar (pre-registered), ties read '?' (new house rule)
Every V / Q hit was decrypted with its crib key (majority per residue class; **a tied class reads '?'** and enters neither known nor
NC). **K4 passes NC ≥ −6.0: 0** in every cell and scope (over 14.25 M scored hits; best K4 NC −6.21, V geo b all.bin p 24;
Q bank p 22 −6.27). Null NC maximum per cell printed beside K4 in `summary227.json`: nulls pass only once — **4 hits = 1 D2 test**
in null 209425, Q all.bin p 24, r10 (row 78680, NC −5.29 with exactly 10 non-crib quadgrams, the minimum:
`UXQI?HT?PF?ZT?M?GS?AC?ASTNORTHEASTIY?FAFTHELING?NSNY?…`). The bar's weakest point is the 10-quadgram floor at p 24 (I-335).
Decrypt level: **`NO-SIGNAL`** everywhere.

Heavy wall: 337 s (`run227.sh`) + 13 s (K4 r10) + 60 s (post-run H-line listing of the K4-only cells) + 1 s (gate P) ≈ 6.9 min,
inside `setsid timeout` process groups (19:49–20:00 PT).

## Labels
- **G — row / column keeping substitution on DHIATENSOR and keyword keyboards, any key: `EXACT-EXCL`** in all scopes (45/45 cells).
- **V — periodic keyboard vector shift on the 8 new geometries: `EXACT-EXCL`** direct p 1–24; bank p 1–18 (geo a) / 1–19 (geo b);
  all.bin p 1–18 / 1–19; above that `INSUFFICIENT-DISCRIMINATION`; V bank p 19 / 20 (geo a) `NO-SIGNAL`.
- **Q — periodic tableau on the 18 new keyboard alphabets: `EXACT-EXCL`** direct p 1–24, bank p 1–16, all.bin p 1–15; above that
  `INSUFFICIENT-DISCRIMINATION`; all.bin p 16 `NO-SIGNAL`.
- Decrypt level (I-330 bar, tie = '?'): `NO-SIGNAL` (K4 0 passes).

## Blind spots
DHIATENSOR geometry in two readings only (wiki ANSI and the No. 5 manual split; punctuation keys not modelled, colB = colA); keyword
keyboards only in QWERTY slot shape and only the three K1–K3 keywords; stagger move only for QWERTY / QWERTZ / AZERTY; no IBM
Selectric typeball code (tilt / rotate) — the Selectric keyboard itself is QWERTY (case 210), the ball code needs a primary source;
no keyboard Polybius with digit keys; periodic keys only for V / Q; one crib error at most; edge cells measured with r10 nulls only.

## Verdict
No solution. K4 was not typed through a Blickensderfer DHIATENSOR board, a KRYPTOS / PALIMPSEST / ABSCISSA-lettered keyboard or a
staggered finger move, in any of the discriminating scopes above.
