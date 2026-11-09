# Case file 163 — Two slips and Hill 4×4 behind K3's decimation law (cycle 175)

**Status:** negative. **Type:** audit/variant (cycle 174 was a new family). IDEAS [I-111](../IDEAS.md) (two slips: one dropped or extra carved
letter **and** one wrong crib letter, the plant case 161 missed by design), with [I-113](../IDEAS.md) (Hill n 4) as the add-on. The grid uses
the [I-115](../IDEAS.md) correction and the [I-117](../IDEAS.md) two-sided report. Smoke runs followed the [I-116](../IDEAS.md) reserved-text rule.
Pre-registered in [`tools/cycle175/PREREG175.md`](../tools/cycle175/PREREG175.md) (commit 824e435, ~05:52 PT) before any K4 or null run.

**Result in one line:** with one dropped letter plus one wrong crib letter behind each of the 170,258 K3-law decimations (n 98), **no periodic
key on the A–Z/KRYPTOS tableaux fits at p ≤ 15** (summed chance 0.07). With one extra letter plus one wrong crib letter (168,858 decimations,
n 96), **none fits at p ≤ 16** (summed chance 0.34). Both are `EXACT-EXCL`. Above that the test has no power (`LOW-POWER`), and every decode is
gibberish, inside the nulls (`NO-SIGNAL`). **Hill 4×4 linear, behind the 165,782 decimations/routes: 0 consistent → `EXACT-EXCL`.** Affine 4×4
is `LOW-POWER`. In the plaintext-first order it gave 3 consistent configs against 2.9 expected, and none of them has an invertible matrix.
In the transposition-first order all 175 invertible fits are vacuous. Grid: p⁺ 0.30, p⁻ 0.40. **No solution.**

## 1. Why this, and what is new
- Queue: cycle 174's pointer (I-118) named I-111 or I-099 for this audit slot, with I-113 as a cheap extra. I-111 won because case 161's
  plant 11 (a dropped letter plus a changed crib letter) was the one model the strict test was built to miss. I-099 needs about three
  chunked cycles.
- Overlap: case 161 ran each anomaly alone. Kryptosbot (Sept 2026 status) lists one-letter anomalies combined with grid rearrangements and
  says two-character differences were never run. Our earlier note (cycle 125) said two-letter differences should be tried only where a text
  source anchors them. This run is **not archive-anchored**. It is a structured model (one indel plus one wrong crib letter) inside one
  family, and it is reported that way.
- Hill: case 162 ran n 2–3 behind these perms. n 4 is new here. The new solver re-ran n 2–3 on K4 as a known-answer check: 0 consistent, and
  the config totals (2,652,512 and 3,978,768) are identical to case 162.

## 2. Models (exact; cycle 173 / case 23 conventions)
- **delx** ([`slip175.c`](../tools/cycle175/slip175.c)): letter d (0–97) of the 98-letter true ciphertext C′ was left off the copper.
  Then any one used crib letter is dropped from the test (wrong on the copper or in the crib). **insx**: an extra letter was carved at d
  (0–96, C′ 96 letters), plus one dropped crib.
- Periodic key, (PA, CA) ∈ {A–Z, KRYPTOS}², Vigenère (= the variant-Beaufort test) and Beaufort, with the key at the plaintext index or at the
  C′ index, p 1–26. A config is (perm, d, dropped crib, frame, PA, CA, mode, p): 1.65 × 10¹¹ (delx) and 1.64 × 10¹¹ (insx) period-level tests.
- Method: the bad crib pairs are found once per (perm, d, frame, tableau). For each p, the drop candidates are the intersection of {a, b}
  over the bad pairs, so all 24 drops cost about one strict test.
- **Hill n 4** ([`hill175.c`](../tools/cycle175/hill175.c)): same models as `hill174`. The row solver is new: RREF mod 2 and mod 13 gives a
  particular solution plus a kernel basis, the two are combined by CRT, and every invertible key is decoded (up to 64 per config).
- **Information filter (I-115):** checks = equations beyond unknowns. For the periodic key that is (used cribs − residue classes). For Hill it is
  Σ_rows max(0, m_r − u). KMIN = 4. Only the grid uses it.

## 3. Results — K4 on the full families

| model | p | K4 configs | chance expectation | nulls on 1/8 (19) min/med/max | verdict |
|---|---|---|---|---|---|
| delx | 1–15 | **0** | 0.072 summed | 0 | `EXACT-EXCL` |
| delx | 16 | 2 (one perm, 96794, d 94, drops 0/19) | 1.46 | 0/0/4 | `LOW-POWER`; decodes −8.17/−8.27, gibberish |
| delx | 17 / 18 / 19 / 20 | 22 / 20 / 285 / 6,624 | 27.9 / 70.5 / 424 / 6,982 | 0/2/18, 0/6/43, 17/49/224, 487/805/1,273 | `LOW-POWER` |
| insx | 1–16 | **0** | 0.36 summed | 0 | `EXACT-EXCL` |
| insx | 17 / 18 | 0 / 0 | 6.7 / 18.1 | 0/0/0, 0/0/18 | `LOW-POWER` (see §6) |
| insx | 19 / 20 | 64 / 2,602 | 158 / 2,030 | 0/12/68, 48/252/856 | `LOW-POWER` |
| both | 21–26 | within 9 % of the analytic line | — | inside the nulls | `LOW-POWER` |

Full per-p table: [`summary175.txt`](../data/cycle175/summary175.txt).
- **Decodes (p ≤ 20).** K4 full: 6,953 delx and 2,666 insx decodes, best −7.27 and −7.54 per quadgram. K4 on 1/8: best −7.28 (delx, 4th of
  20 texts, tied with a null) and −7.55 (insx, 9th of 20). The 19 nulls' best values are −7.17 … −7.49 (delx) and −7.15 … −7.98 (insx). The planted English reads
  −4.08 … −4.34. → `NO-SIGNAL` ([`decodes175.txt`](../data/cycle175/decodes175.txt)).

| Hill (K4, 165,782 perms) | configs | consistent | invertible | chance | verdict |
|---|---|---|---|---|---|
| n 2–3 (re-run, new solver) | 6,631,280 | 0 | 0 | ≤ 10⁻⁸ | `EXACT-EXCL` (= case 162) |
| n 4 linear, ix 0 / ix 1 | 1,326,256 each | **0 / 0** | — | 6 × 10⁻⁶ / 0.07 | `EXACT-EXCL` |
| n 4 affine, ix 0 | 1,326,256 | 3 (KA numbering, perms 52306 off 2, 52316 off 3, 77184 off 1; 4 checks each) | **0** | 2.9 | `LOW-POWER` (on the chance line; none has an invertible key, so nothing to decode) |
| n 4 affine, ix 1 | 1,326,256 | 381 | 175 (3,004 keys decoded) | 1,680 (checks ≥ 4: 1.27) | `LOW-POWER`: every fit has ≤ 3 checks (vacuous); best decode −7.30; K4 on 1/8 −7.48 vs nulls −7.06 … −7.60 → `NO-SIGNAL` |

## 4. Pre-registered grid (on 1/8 of the perms, checks ≥ 4)
| cell | K4 | 19 nulls min/med/max | scored? | K4 z |
|---|---|---|---|---|
| C1 delx p 1–16 | 0 | 0/0/4 | yes | −0.23 |
| C2 insx p 1–16 | 0 | 0/0/0 | **no** (zero null variance; K4 equal) | — |
| C3 delx p 17–26 | 1,330 | 428/987/2,149 | yes | +0.79 |
| C4 insx p 17–26 | 851 | 518/1,066/2,320 | yes | −0.72 |
| C5 Hill n 4 | 1 (perm 77184) | 0/0/1 | yes | +1.88 |

G⁺(K4) = +1.88, **grid p⁺ = 0.30**. G⁻(K4) = −0.72, **grid p⁻ = 0.40** (best attainable 0.05 each). Nothing stands out on either side.
Lesson (→ I-120): C1 and C5 are sparse, with at most 2 non-zero texts. Their leave-one-out z jumps on a single event. One null's z is +∞
because it alone has 4 fits in C1, and K4's maximum comes from its one Hill fit. The I-115 rule drops only cells that are exactly constant.
Sparse cells need an exact count score.

## 5. Controls and recount
- **Planted controls 14/14** ([`controls175.txt`](../data/cycle175/controls175.txt)), from an independent string-level encryptor
  ([`plant175.py`](../tools/cycle175/plant175.py)):
  - 6 two-slip plants (3 delx, 3 insx; p 6–16; mixed tableaux, modes and frames) were found at the planted slot, d and dropped crib, with the
    key letters equal to the key.
  - One strict-del plant was found, with all 24 drops.
  - One plant with del plus **two** changed crib letters was missed, as designed.
  - Cycle 173's ctl10 (seed 173100, the plant case 161 missed) was regenerated byte for byte and **found**, with crib 5 dropped and key COMPASS.
  - 4 Hill n 4 plants (linear/affine, A–Z/KA, both orders, offsets 0–3) were found and decoded to the plaintext. One Hill plant with an altered
    crib letter was missed.
- **Recount** ([`recount175.txt`](../data/cycle175/recount175.txt)). `recount175.py` is numpy with a different formulation: a drop is
  consistent iff every conflicting pair touches it. On 9 slices it gave HIST, HISTK and EXPECT per p identical to the tool. The slices were
  4 K4 slices in both families, 2 null slices, 2 plant slices, and K4's p-16 perm 96794. `hillrecount175.py` brute-forces every row vector mod 2
  and mod 13 on 63 perms: 30 with K4 decodes, 30 random, and the 3 affine ix-0 fits. That is 2,016 sub-cell configs, **0 mismatches**.

## 6. Honesty notes
- The pre-registration text says "~05:58 PT"; the push was at ~05:52 PT (commit 824e435). The text was not changed.
- After that push, and before any K4 or null run, `hill175.c` was changed to decode **every** invertible key, not only the first.
  Two Hill plants showed that the planted key is not always first (hctl0: 8 keys, hctl1: 48). The consistency test and every count are
  unchanged. The change was pushed in e350f42 before the run.
- Smoke runs used only the reserved shuffle (seed 9175).
- insx p 17–18: K4 has 0 against an analytic 6.7 / 18.1, but 18 of 19 nulls also have 0 at p 17–18 on 1/8. The analytic mean is carried by rare,
  clustered configs, so K4's 0 is not a deficit. The label stays `LOW-POWER`, as pre-registered (→ I-122).
- I-111 had estimated "p ≤ 17 informative". The measured exact bound is p ≤ 15 (delx) and p ≤ 16 (insx).
- hctl0 (linear n 4, 8 nominal checks) still had 8 invertible keys, because the crib vectors are dependent mod 2. The checks count overstates
  information when that happens (→ I-121).
- Heavy compute: the main run took 5 min 03 s wall (63 jobs, 3 at a time, box shared with browsers). Locating the 3 Hill fits by chunks and
  single perms took about 2.5 min, and the recounts and decodes about 1.5 min (light). Total ≈ 8 min.

## 7. Limits (what stays open)
Two slips of other kinds behind the decimations: swap + wrong crib, two dropped letters (n 99), two wrong crib letters (I-123 / I-100).
Themed or vocabulary alphabets under two slips. Spiral/diagonal routes rebuilt for 96/98 letters (I-109). The `LOW-POWER` band p ≥ 16–17.
Hill 4×4 affine (no power; a keyword-built matrix would restore checks → I-124). Hill under one error behind the decimations. Hill n ≥ 5
behind the decimations.

## Reproduce
From a work dir holding `support/` (`all.bin` from cycle 168; `dec96.bin`/`dec98.bin` from `tools/cycle173/decgen173.py`, md5 in
[`inputs175.txt`](../data/cycle175/inputs175.txt); `_s8` = `P[::8]`; `quadgrams.json`) and `run/k4.txt`, `run/nulls175.txt`:
build `slip175` (`gcc -O3 -march=native -fopenmp slip175.c -o run/slip175 -lm`) and `hill175` (`gcc -O3 -march=native hill175.c -o run/hill175 -lm`).
Then run `python3 tools/plant175.py run/ctl 175175`, `python3 tools/checkctl175.py run/ctl run`, `tools/run_cycle175.sh`,
`python3 tools/summarize175.py run/out`, `decode175.py` and the two recount scripts (usage lines in each file).
Raw outputs: [`data/cycle175/`](../data/cycle175/).
