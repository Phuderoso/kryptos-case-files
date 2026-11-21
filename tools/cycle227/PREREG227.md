# PREREG227 — Cycle 227 (new family, I-327 chunk 1): the wider keyboard family

Filed 2026-11-20 19:49 PT, before any K4, plant or null run of this cycle. Base: origin/main 137ef5f (c226 published).
Slot: new family (I-333: 227 must be a new family among I-299, I-313 calibration-first, I-327). Case file 213.

## Why I-327 (and not I-299 / I-313)
- **I-327** opens geometries and alphabets the house has never fed to K4: the Blickensderfer "Scientific" keyboard (DHIATENSOR,
  1892 — an English-frequency layout from the typewriter era Sanborn's references point to), QWERTY-shaped keyboards filled with
  the K1–K3 keywords (KRYPTOS, PALIMPSEST, ABSCISSA: the K1–K3 "meaningful keyword + keyed alphabet" habit, moved onto a keyboard
  grid), and a stagger-aware finger move. `layouts227.py` checks novelty: 18 of the 22 candidate keyboard alphabets are absent from
  `alpha.bin` (86,731), `themed144.bin` and `kb224.bin` (the four dropped are the plain keyed rows, already in `alpha.bin`, and one
  duplicate). Infrastructure exists (`kb226.c`), so the cycle fits the 8-minute budget with plants and nulls.
- **I-299** (other digit bases) is a parameter sweep of the case 200 filter whose null rate grows as (b/26)²⁴ for b > 10 — low value,
  and b < 10 is a subset of the base-10 keys already excluded. Stays queued.
- **I-313** needs the PK8 / PK9 texts verified from primary sources before use, and is a calibration, not a K4 test. Stays queued.

## Geometries (`geo227a.txt`, `geo227b.txt`; kb224 format: letter → row, colA, colB)
| name | rows (key index) | source |
|---|---|---|
| DHIA-W | `PWFULCMY` (1–8) / `DHIATENSOR` (0–9) / `ZXKGBVQJ` (0–7) | keyboard wiki (wiki.themk.org "DHIATENSOR"), ANSI mapping |
| DHIA-M | `ZXKG`\|`BVQJ` (1–8) / `PWFU`\|`LCMY` (1–8) / `DHIAT`\|`ENSOR` (0–9) | Blickensderfer No. 5 instruction manual (split "between G U T and B L E") |
| KRYPTOS-QW, PALIMPSEST-QW, ABSCISSA-QW | keyed alphabet in the QWERTY key slots 10 / 9 / 7, row 2 colB = colA + 1 | K1–K3 keywords |
| QWERTY-S, QWERTZ-S, AZERTY-S | case 210 layouts with colA := colB (row 2 moved half a key: stagger-aware torus for V) | geo224 |
colB = colA on DHIA (no stagger information), so G partition 2 duplicates partition 1 there. G on the -S layouts repeats case 210
(same partitions) and is printed but not labelled.

## Models (unchanged from case 210, `kb227.c` = `kb226.c` + the two rules below)
G (row / column preserving substitution, any key), V (vector shift on the 3 × 10 torus, periodic p 1–24, ix 0 / 1),
Q (Vig / variant / Beaufort tableau on the 20 alphabets of `kb227.bin` = 18 new + AZ + KA, all ordered pairs except AZ/KA–AZ/KA,
periodic p 1–24, ix 0 / 1). One crib error tolerated (hit ⇔ ≤ 1 of 24 crib seats dissents). Scopes: direct; behind the 165,065
bank rows and the 165,782 `all.bin` rows, both directions. Q only with geo227a (Q does not depend on geometry).

## Decrypt reading (pre-registered)
- **(a) I-330 house bar:** a hit is a decrypt candidate iff known ≥ 49, ≥ 10 non-crib quadgrams, and **NC ≥ −6.0** (NC = mean
  log10 quadgram over quadgrams with no '?' and no crib position, `qg.bin` sha256 4a02ba4e…). Per (model, p) the null NC maximum
  is printed beside K4's count and best NC.
- **(b) New house rule — ties read '?':** a residue class whose crib-seat key values tie for the top multiplicity reads '?' and
  enters neither `known` nor any NC quadgram (kb226 took the first seat's value). `KB_TIE_FIRST=1` restores the old rule for audit.

## Gates
- **Gate T:** `kb227` S / T lines equal `kb226`'s on `geo224.txt` + `kb224.bin` (K4, bank, every 10th row) byte for byte.
- **Gate P (seed 209548):** 20 plants (`plant227.py`: G 4, V 7, Q 9; new geometries / alphabets only; p 3–24; direct / bank /
  all.bin; odd ids one wrong carved crib letter). PASS ⇔ ≥ 19/20 planted cells found on their true row (`gate227.py`). Reported:
  share of found V / Q plants with NC ≥ −6.0 (target ≥ 90 %).

## Nulls and labels
The 20 published case 210 shuffles (`nulls224.tsv`, seeds 209417–209436): direct GVQ / GV and G at full scale behind bank and
all.bin; the first 12 behind bank / all.bin for V / Q on every 10th row (rowstride 10, offset 0). No new null seeds.
Per (model, geometry, scope, p) cell, K4 is compared on the same rows (perm % 10 == 0 for the r10 cells):
- K4 0 and all nulls 0 → **EXACT-EXCL** (under the stated assumptions; scale caveat printed when only r10 nulls exist);
- K4 > 0 with nulls > 0 at that cell → **INSUFFICIENT-DISCRIMINATION** (count level) with rank p_up = (1 + #nulls ≥ K4)/(n+1),
  occupancy and D2 distinct-crib-test counts (case 209 rule) printed;
- K4 > 0 with nulls 0 → manual read + decrypt bar; **NO-SIGNAL** unless a decrypt passes (a) and reads as coherent English.
Decrypt level: K4 NC passes vs null NC passes / max per cell.

## Budget, seeds
`run227.sh` inside `setsid timeout 600` (own process group), ≈ 6–7 min. Seeds: 209548 plants. Next free seed: **209549**.

## Not in scope
IBM Selectric (keyboard is QWERTY, already covered; the typeball tilt / rotate code needs a primary source → follow-up),
keyboard Polybius with digit keys, numeric row, non-periodic keys for V / Q, more than one crib error.
