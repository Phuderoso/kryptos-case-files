# Case 222 — Compass-point key streams: "boxing the compass" as key material (cycle 236)

**Slot:** new family (235 audit → 236 had to be new; I-373). Idea **I-374** (tested here); new **I-375–I-378**.
Pre-registered as [PREREG236](../tools/cycle236/PREREG236.md) (local commit 16dc3ee, 2026-11-22 19:41 PT, before any plant, null or K4 run). Code and window list: [`tools/cycle236/`](../tools/cycle236/)
(`keys236.py`, `keys236.tsv`, `plant236.py`, `check236.py`, `mknull236.py`, `runA.sh`, `runP.sh`, `HASHES236.txt`); tool `gn217` **unchanged** (source sha 97bae55f…d792); raw results (stamped, rule 5): [`data/cycle236/`](../data/cycle236/).
**Verdict: no solution.** K4 has 0 hits (0 exact, 0 with one wrong crib letter) in all three scopes: `EXACT-EXCL` within the frozen 8,792-window list and model Q (gate P 20/20).

## The idea (and why it is not in the repo yet)
The first crib, **EASTNORTHEAST**, is not just a direction: it is the 7th of the 32 named points of the mariner's compass. The site has a compass rose and a lodestone ([case 10](10-style-profile.md)), and K2 ends on a
bearing. A K1–K3-style "plain-sight" key would be the **boxed compass itself** — the ordered recital NORTH, NORTH BY EAST, NORTH-NORTHEAST, NORTHEAST BY NORTH, … that every sailor learned — used as a running key,
or its numeric shadows (bearings in degrees, letters per point name). A repo grep before filing found no "boxing the compass", NORTHBYEAST or point-sequence stream; COMPASS / NORTHEAST appear only as single
keywords, which the periodic tests ([case 12](12-strips-and-periodic-keys.md)) already cover. `[speculation]`: no public source says Sanborn used the compass recital as a key.

## Method
`gn217` model Q (as cases 203 / 219 / 220): layer letter at plaintext position i carved at S[i] (S = transposition row or its inverse; identity for direct); Vig c = Y[x(p) + k], variant Y[x(p) − k],
Beaufort Y[k − x(p)], mod 26; key on the plaintext index or the carved index. Streams (`keys236.py`):

| family | source | readings | value map | windows |
|---|---|---|---|---|
| R32 | 32 full point names (NORTH … NORTHBYWEST, 374 letters) | cw, acw, reversed string; cyclic, every offset | A=0, A=1, KRYPTOS index, index+1 | 4,488 |
| R16 / R8 | 16- and 8-point roses (162 / 54 letters) | same | same | 1,944 / 648 |
| A32 / A16 | standard abbreviations (N, NBE, NNE, NEBN, …; 92 letters for A32) | same | same | 1,104 / 432 |
| D32 | bearings ⌊11.25 n⌋° (cw) and 360 − d (acw) | cyclic, every offset, + c ∈ {0, 1} | value mod 26 | 128 |
| L32 / L16 | letters per point name | same | value mod 26 | 32 / 16 |

8,792 windows after dropping duplicates of the keys217 / 218 / 221 / 233 / 234 lists; 3 forms; direct 86,731² `alpha.bin` (contains A–Z and the KRYPTOS alphabet), bank and all.bin 144² `themed144.bin` (also
contains both) behind 165,065 K3-style transpositions and 165,782 K3-law decimations / routes; hit = ≥ 23 / 24 crib seats (EASTNORTHEAST 1-based 22–34, BERLINCLOCK 64–74).

| scope | permutation rows | window-pair-forms | K4 hits (24 / 23) | 6 fresh nulls 209673–209678 | time |
|---|---|---|---|---|---|
| direct | 1 | 1.98 × 10¹⁴ | 0 / 0 | 0 / 0 each (full) | 5 s |
| bank | 165,065 | 3.61 × 10¹⁴ | 0 / 0 | 0 / 0 each (rows ÷ 10) | 102 s |
| all.bin | 165,782 | 3.63 × 10¹⁴ | 0 / 0 | 0 / 0 each (rows ÷ 10) | 103 s |

Total 373 s wall (K4 210 s, nulls ≈ 27 s each), one process group (`setsid timeout 480`).

**Gate P (seed 209672):** 20 / 20 plants recovered with the planted (window, form, X, Y, permutation) (Wilson 0.84–1.00; 10 one-error plants included; families drawn: R32 8, R16 5, A32 5, A16 1, D32 1 — R8 / L32 / L16 not drawn).
**Gate T:** `check236.py` re-derived all 22 plant H lines, agreement mismatches 0. Plant decrypts NC −3.96 … −4.94, every one far above the I-342 bar (−7.01 at nq 64, N = 10; margin ≥ +2.07).
**Nulls:** six shuffled K4 texts, 0 hits in every scope. As in cases 219–220 this is a machinery check, not a power calibration: the 24-seat filter predicts ≪ 1 chance hit per text at these sizes, so a 0 for K4 says
"no key in the list fits", not "K4 is unlike the nulls".

## Reading
- `EXACT-EXCL` for K4 within the frozen list and model Q (both cribs at the official positions; one wrong crib letter tolerated; plants show the search finds such keys, including one-error ones).
- No H line exists, so there is no decrypt to read and the I-342 NC bar was not exercised on K4 (it was exercised on the plants only, which are English by construction).
- What this closes: the boxed compass (32 / 16 / 8 points, names or abbreviations, either direction, any start) as a K1-style running key on A–Z / KRYPTOS / themed keyed tableaux, directly and behind the house
  transposition banks; its bearing and name-length shadows likewise.

## Blind spots
Spaces / hyphens kept as nulls (NORTH-NORTHEAST with a separator letter), "by" spelled B or omitted; quarter points (128-point rose, "NORTH ¼ EAST"); French / German / Spanish rose names (NORD-NORDOST…);
bearings in mils or as two-digit groups; the compass recital as a *plaintext-side* or *alphabet* (rank order) element rather than a shift stream; compass streams plus a periodic keyword (compound key);
other transpositions. A near-miss profile (best agreement < 23 for K4 vs nulls) was not produced, so the test says nothing about partial fits (I-376).

## Sources
Point names and order: standard 32-point mariner's compass (e.g. N. Bowditch, *The American Practical Navigator*, table of points; also Wikipedia "Points of the compass" `[secondary]`).
