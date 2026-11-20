# PREREG224 — cycle 224 pre-registration (filed before anything below is run on K4, the plants or the nulls)

Filed 2026-11-20 ~08:05 PT (America/Vancouver). Slots: 222 free, 223 audit (case 209), so **224 must be a new family** (I-319 /
I-321). Base: main b304de5 (cycle 223 published by Firefly). Seeds: next free 209416. Reserved here: **209416** (plants),
**209417–209436** (20 shuffled-K4 nulls). Next free after this cycle: **209437**.

## Why this family (I-323, new)
A grep of all 209 case files finds no case built on the **typewriter keyboard**: "keyboard" / "QWERTY" occur nowhere in
`case-file/`, and none of the 86,731 alphabets of `alpha.bin` nor the 144 of `themed144.bin` is a keyboard order (checked:
QWERTYUIOPASDFGHJKLZXCVBNM, QWERTZ…, AZERTY…, QAZWSX…, Dvorak, reversals: all absent). Sanborn typed his drafts (1988–90);
keyboard ciphers (letter → neighbour key, keyboard-order alphabets) are the oldest "hobby" layer a sculptor could pick up with no
crypto library. `[speculation]` motivated, `[repo]` gap verified. The idea is structural (keyboard geometry), not another key
stream on the existing alphabets.

## Layouts and alphabets (fixed now)
Letters only, physical key index per row (0 = leftmost key of the row, punctuation keys counted):
- **QWERTY** top Q0…P9, home A0…L8, bottom Z0…M6. **QWERTZ** = QWERTY with Y/Z swapped. **AZERTY** top A0 Z1 E2 R3 T4 Y5 U6 I7 O8 P9,
  home Q0…L8 M9, bottom W0 X1 C2 V3 B4 N5. **Dvorak** top P3 Y4 F5 G6 C7 R8 L9, home A0 O1 E2 U3 I4 D5 H6 T7 N8 S9, bottom Q1 J2 K3 X4 B5 M6 W7 V8 Z9.
- Columns: **colA** = same key index; **colB** = bottom-row index + 1 (the half-key stagger read the other way).
- Alphabets per layout (4 × 4 = 16 keyboard alphabets): **R1** rows top→bottom, keys left→right; **R2** rows top→bottom, right→left;
  **C1** colA columns left→right, each top→bottom; **C2** colA columns left→right, each bottom→top. (Reversals and rotations are
  absorbed by the three forms and the free periodic key.) Plus A–Z and KA (KRYPTOSABCDEFGHIJLMNQUVWXZ) = **18** alphabets.

## Models (layer letter at plaintext position i is carved at S[i]; S = transposition row, dir 0, or its inverse, dir 1; direct = identity)
- **G (geometry, key-free).** Any substitution that keeps a letter in its keyboard **row** (G-row), its **colA** column (G-colA) or its
  **colB** column (G-colB), with *any* key / any per-position choice (covers keyboard row-shift / column-shift ciphers with periodic,
  progressive, running or random keys). Necessary condition: the carved letter at each crib seat lies in the same class as the crib
  letter. 4 layouts × 3 partitions = 12 tests per transposition.
- **V (keyboard vector shift, periodic).** Coordinates (row r, colA index c) on a 3 × 10 torus; key = vector (dr mod 3, dc mod 10)
  per residue class; periodic p 1–24; key indexed by plaintext position (ix 0) or carved position (ix 1). 4 layouts.
- **Q (keyboard tableau, periodic).** c = Y[x(p)+k] (Vig) / Y[x(p)−k] (variant) / Y[k−x(p)] (Beaufort), X (plain) and Y (cipher) from
  the 18 alphabets, all 18² − 4 = 320 ordered pairs except the four A–Z / KA pairs already covered; periodic key, any values, p 1–24;
  ix 0 / ix 1.
- **Hit** = at most one of the 24 crib seats has to be dropped for the model to be consistent (≥ 23/24; exact = 24/24). For V / Q the
  minimum number of dropped seats is Σ over residue classes (n − max multiplicity of the key value), exactly.

## Scopes
- **direct** (identity), all models.
- **bank** (`bank.bin`, 165,065 rows) and **all.bin** (165,782 rows), × 2 dirs, × 2 ix for V / Q: G, V and Q on every row for K4.

## Gates
- **Gate P (seed 209416, bar ≥ 19/20).** 20 plants from `plant224.py`: plaintext = random 97-letter window of `k123_eng.txt` with the
  cribs written in at the official seats; ids 0–5 model G (random row/col-preserving per-position substitution), 6–9 model V, 10–19 model Q
  (random pair, form, p 4–24, ix); transposition: direct / bank / all.bin rotating; odd ids carry one wrong carved crib letter. Pass =
  the tool reports the planted (scope row, dir, ix, layout/pair, form, p) as a hit.
- **Nulls (seeds 209417–209436).** 20 shuffles of K4 (random.Random(seed).shuffle). All nulls run direct G / V / Q and bank + all.bin G
  (full rows); nulls 209417–209419 also run bank + all.bin V / Q on every 10th row (row offset 0).

## Labels (fixed now)
- Per model × scope × p: K4 hit count vs null hit counts (raw cells and primitive cells = hit at p but not at any divisor of p).
- **EXACT-EXCL** for a (model, scope, p) cell when K4 has 0 hits *and* the cell is discriminating: the expected null count at full scale is
  < 0.05 per text (mean over nulls, ×10 for 1/10-row nulls) — i.e. a real key of this form would have been found and chance would not
  have produced a fit. **INSUFFICIENT-DISCRIMINATION** when nulls hit at ≥ 0.05 per text (K4 hits then compared by rank, D2 not needed).
- Any K4 hit: decrypt with the crib-derived key (unknown classes '?'), score mean log10 quadgram (`quadgrams.json`, floor as file);
  **candidate** only if ≥ 49 known letters and score ≥ −6.0 (case 209 bar); otherwise `NO-SIGNAL` for that hit.
- A solution needs a coherent full 97-letter English decrypt; nothing here is submitted anywhere.

## Budget
Heavy work in one `setsid timeout 480` process group (8 threads). If the full Q bank / all.bin run does not fit, the unrun part is
reported as not run (no extrapolated label).
