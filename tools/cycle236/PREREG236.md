# PREREG236 — Cycle 236 (new family, I-374): compass-point key streams ("boxing the compass")

Filed 2026-11-22 19:41 PT (America/Vancouver, UTC−7), **before** any plant, null or K4 run with `keys236.bin`. Base: origin/main **a60b1f7** (c235 published by Firefly). Case file 222.
Slots: 235 audit (case 221), so **236 must be a new family** (I-373); 237 free; 238 audit. Seeds: plants **209672**, nulls **209673–209678**; next free after this cycle **209679**.

## Disclosed before filing
- `gn217.c` unchanged (sha 97bae55f…d792), rebuilt `gcc -O3 -fopenmp -march=native`. `keys236.py` run once to build the list (no search).
- **Timing smoke** (no new seed): the already-published case 220 null text (seed 209646, `null234.txt`) through `keys236.bin`, direct at Y stride 20 (offset 7) and bank at row stride 100 (offset 50): ≈ 1 s each, 0 hits. Used only to size the run; not part of any result.
- Frozen list: `keys236.bin` sha256 **6707dda27020d88ef99ee62f721ad49f3b93f70b99f04d4df6acdc18f24946cc** (8,792 windows after dropping duplicates of the keys217 / 218 / 221 / 233 / 234 lists; `keys236.tsv` sha cf796d12…c29f lists family / variant / offset / conversion). `keys236.py` sha 059f0735…60d1.

## Idea (I-374, `[speculation]`)
The first crib, EASTNORTHEAST, is literally one of the 32 points of the mariner's compass, the sculpture site has a compass rose and lodestone (case 10), and K2 ends on a bearing. A K1–K3-style
"plain-sight" key would be the **boxed compass itself**: the ordered list of point names (NORTH, NORTHBYEAST, NORTHNORTHEAST, …) used as a running key, or its numeric shadows (bearings in degrees,
letters per name). A repo grep (cycle 236) finds no "boxing the compass", NORTHBYEAST or compass-point stream anywhere; COMPASS / NORTHEAST appear only as single keywords (periodic, already covered).

**Streams:** R32 / R16 / R8 full names, A32 / A16 abbreviations; clockwise, anticlockwise and reversed letter string; cyclic, every character offset; letter → value by A=0, A=1, KRYPTOS-alphabet index, index+1.
D32 bearings (⌊11.25 n⌋°, cw and 360 − d), L32 / L16 letter counts of the names; cyclic, every offset, c ∈ {0, 1}.

## Model and commands (as cases 219 / 220)
`gn217` model Q: layer letter at plaintext position i carved at S[i] (S = family row / inverse; identity for direct); c = Y[x(p) + k] (Vig), Y[x(p) − k] (variant), Y[k − x(p)] (Beaufort), mod 26;
key at plaintext index (ix 0) or carved index (ix 1). Hit = ≥ 23 / 24 crib seats (EASTNORTHEAST 1-based 22–34, BERLINCLOCK 64–74). Scopes: direct (86,731² `alpha.bin`, contains A–Z and the KRYPTOS
alphabet), bank (165,065 K3-style transpositions) and all.bin (165,782 K3-law decimations / routes), 144² `themed144.bin`.
`runA.sh`: K4 direct / bank / all.bin at full scale; 6 fresh nulls (`mknull236.py`, seeds 209673–209678) direct full, bank and all.bin at row stride 10. `runP.sh`: gate P. Heavy runs in their own process group (`setsid timeout`).

## Gates and labels
- **P:** 20 plants (`plant236.py`, seed 209672; 0–7 direct, 8–13 bank, 14–19 all.bin; odd ids one corrupted crib letter); pass ≥ 19/20 recovered with the planted (w, form, X, Y, perm), Wilson reported.
- **T:** `check236.py` (= `check234.py`, docstring only) re-derives agreement for every H line and decrypts all 97 letters; mismatches must be 0.
- **I-342 NC bar** for any decrypted H line: bar(nq, N) = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² − 0.0192 nq + 0.879, N = max(10, H lines in scope); candidate only if NC ≥ bar **and** the 97 letters read as English.
- **Nulls:** six shuffled K4 texts. The 24-seat filter predicts ≪ 1 chance hit per text; the nulls check that the machinery does not produce hits on non-K4 text of the same letter counts (calibration of the false-hit rate, not power). A null hit count > K4's is reported as such.
- **Labels:** K4 0 hits with P passing → `EXACT-EXCL` within the frozen list and the model; hits failing the bar and null-like → `NO-SIGNAL`; P failing → `INSUFFICIENT-DISCRIMINATION`.

## Honesty clause
Any plain-English decrypt with both cribs at the official positions and NC ≥ bar is reported prominently and reproduced independently before being called a solution. Nothing is submitted anywhere.
