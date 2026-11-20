# Case 209 — Audit: the case 205 p 21 one-error "excess" under the rank rule and family-collapsed counts (I-318, cycle 223)

**Slot.** Audit (I-320: 221 new family, 222 free, so 223 must be an audit). Pre-registered as
[`PREREG223`](../tools/cycle223/PREREG223.md) (local commit e94bc42, ~03:45 PT, before any run on K4, plants or nulls). Base main
c4f52fd. Seeds 209255 (plants), 209256–209415 (160 shuffled-K4 nulls); next free **209416**.

## The question
[Case 205](205-columnar-w9-w10-one-error-audit.md) ran every column order of width 9–10 × periodic tableau key under one wrong crib
letter. At **p 21** K4 had **1,928** configurations at excess ≤ 1, above all eight nulls (371–1,175). The Voynich desk
(voynich-case-files 0185ed5) flagged it as an observation only: settling it needs ≥ 146 nulls with a rank rule. At **p 20** K4 had 3
(nulls 2–70). The hypothesis registered (`HYPOTHESIS`, structural): the p 21 excess comes from **many column orders that put the 24 crib
seats on the same carved positions** — one crib test counted many times — not from more distinct fits.

## Method
- **Tool.** [`col21.c`](../tools/cycle223/col21.c): `col1e.c` (cycle 219) with enumeration, transposition, key forms, models and the
  excess function copied verbatim; it evaluates only p 20 and 21, prints every excess ≤ 1 cell and appends the carved positions
  j[0..23] of the 24 crib seats. Same family as case 205: all 9! + 10! orders, ragged grid, ROW / COL read, σ / σ⁻¹, A–Z / KRYPTOS
  tableau, Vigenère (= variant) / Beaufort, key on plaintext (A) or carved (B) index.
- **Counts.** R = raw configurations (the case 205 count); **D2** = distinct (alphabet, form, model, p, j[0..23]) = distinct crib
  tests (primary collapsed count); D3 = distinct crib maps (alphabet, form, model, residue and key value per seat), descriptive.
- **Rank rule.** M = 168 nulls (the 8 of cycle 219 + 160 new). p_up = (1 + #{nulls ≥ K4}) / 169; Clopper–Pearson 95 % on the tail.

## Gates
- **Gate T (reproduction): PASS.** col21 reproduces case 205 exactly for K4 (p 20 = 3, p 21 = 1,928) and the eight cycle-219 nulls at
  both periods (`summary223.json` → `gateT`).
- **Gate P (seed 209255): 20/20 PASS** (bar ≥ 19). 16 plants at p 21 and 4 at p 20 by the cycle 219 textbook encryptor (imported
  unchanged); every true cell reported at its true p, crib-key decrypt matching the plant at every determined position (63–92 letters)
  outside the corrupted class, and its D2 key present. Of the 10 corrupted plants, 9 came back at excess 1 and one (id 17) at excess 0
  (its wrong seat alone in its key class — invisible to any crib test, allowed by the rule).

## Results (168 nulls)
| statistic | K4 | null median | null 95th pct | null max | nulls ≥ K4 | p_up | CP95 tail |
|---|---|---|---|---|---|---|---|
| p 21 R (raw) | **1,928** | 911 | 1,709 | 2,849 | 6 | **0.041** | 0.013–0.076 |
| p 21 D2 (distinct crib tests) | **99** | 114 | 235 | 375 | 105 | **0.627** | 0.547–0.698 |
| p 21 D3 (crib maps) | 99 | 114 | 235 | 375 | 105 | 0.627 | — |
| p 20 R | 3 | 14 | 101 | 286 | 138 (≤: 36, p_low 0.219) | 0.82 | — |
| p 20 D2 | 2 | 4 | 13 | 31 | 135 | 0.80 | — |

**Label p 21 (pre-registered rule): `STRUCTURAL MULTIPLICITY`.** The raw count is mildly high (6 of 168 shuffles reach it, p_up 0.041 —
the 8-null "above all" was a small-sample effect, but not pure chance-level either), and it vanishes once identical crib tests are
counted once: K4 has 99 distinct crib tests at p 21, below the null median.

**Label p 20: unchanged `INSUFFICIENT-DISCRIMINATION`** for the exclusion claim; K4's 3 cells (2 distinct) sit low but inside the null
bulk (p_low 0.22), and neither meets the decrypt bar (−6.98, −7.35).

**Decrypt bar.** All 101 distinct K4 cells at p 20 / 21 (84–97 letters determined) score below −6.0 mean log10 quadgram; best −6.48
(`FVEPCESGEBO?THKNIUDLKEASTNORTHEASTOES?AVDEF…`). No candidate.

## Where the multiplicity comes from (descriptive)
- Every p 21 cell, for K4 and for the nulls, is **model B** (key on the carved index) with **one dissenting two-member class**; model A
  never fits at p 21 (its residues pair 21–31 with 63–73, so ten fixed letter pairs must agree). With 24 seats on 21 residues, model B
  leaves most classes with one member: the crib test is nearly vacuous there.
- K4's 1,928 = 52 single cells + 36 doubles + nine families of 48–720 orders (one each of 720, 240, 72; three of 192; four of 48).
  Those nine carry **1,800 / 1,928 (93 %)**. They are COL read with σ⁻¹ at w 10 (K4 1,804 vs null median 756): the crib seats occupy
  only a few column ranks, so the remaining columns permute freely (6! = 720) without moving any crib seat.
  Descriptive check, not pre-registered ([`mult223.py`](../tools/cycle223/mult223.py), `mult223.tsv`): share of R in families ≥ 24 —
  K4 0.93, null median 0.83, 13/168 nulls ≥ K4; a 720-family occurs in 5/168 nulls.
- So the case 205 p 21 number is mostly the size of a few column-order families K4's letters happen to fall into, not a count of
  independent fits.

## What this changes
- Case 205's p 21 "K4 above all 8 nulls" is closed as **structural multiplicity**: no extra nulls are owed (I-318's ≥ 146-null branch is
  done here with 168). No label of case 205 changes.
- **House rule (from cycle 224):** null comparisons of exhaustive-transposition one-error counts are made on **D2 (distinct crib
  tests)** with the rank rule; raw counts are printed but not labelled. I-312 chunks 2–5 adopt it.

## Blind spots
Same family as case 205 (w 9–10; w 11 is I-312; no rotations, non-tableau alphabets, running keys, dropped / inserted letters, two
errors). Ranks are empirical with resolution 1/169; six rank tests reported, primary p 21 R / D2. The mechanism paragraph is descriptive.

## Files
[`data/cycle223/`](../data/cycle223/): `results_K4.txt` and `results_null20923[4–9]/2092[40–41].txt` (stamped, every p 20 / 21 hit line with
crib-seat positions), `counts223.tsv` (R / D2 / D3 for all 169 texts with input sha), `summary223.json` (gates, ranks, structural
tables, K4 decrypts), `mult223.tsv`, `plants223.tsv`, `nulls223.tsv`, `texts.tsv`, `analyze223.log`, `time.txt`, `SHA256SUMS`,
`SHA256SUMS_all_results.txt` (all 169 results files; the 160 new-null files are not committed — `run223.sh` regenerates them in
~5 min and the sums check them). Tools: [`tools/cycle223/`](../tools/cycle223/). Heavy wall 305 s (03:45:30–03:50:34 PT).

## Verdict
No solution. The p 21 excess of case 205 is the same few crib tests counted across large families of column orders; counted once,
K4 is below the null median. **K4 still standing.**
