# Case 205 — Audit: every column order of width 9–10 under one wrong crib letter (I-007), the desk's blind recounts of cases 202–203, and stamped results files (cycle 219)

**Slot.** Audit (I-310). 217 and 218 ran new families; 220 is free; a new family is due by 221. Pre-registered as
[`PREREG219`](../tools/cycle219/PREREG219.md) (commit 2e707bb, ~11:55 PT, before any run on K4, plants or nulls). Base main b5aef4c.
Seeds 209233 (plants), 209234–209241 (nulls); next free **209242**.

## Part C — case 112 under one error (I-007, part of I-003)

**The claim audited.** [Case 112](112-all-orders-w9-w10.md) (cycle 124): no column order of width 9 or 10 (all 3,991,680 orders,
ragged 97-letter grid, rotation 0, COL or ROW read, σ or σ⁻¹), combined with a periodic Vigenère / variant / Beaufort key of
period ≤ 18 on the A–Z or KRYPTOS tableau, key before or after the transposition, fits **all 24** crib letters. A high-impact exact
exclusion (it is what lets "K3-style keyword columnar + K1-style Vigenère" be called closed at w 9–10), but strict: one wrong crib
letter, or one wrong carved letter at a crib seat, would hide the true cell.

**Tool.** [`col1e.c`](../tools/cycle219/col1e.c), written fresh: the transposition comes from ranking grid cells (not from cycle 124's
`place()` formula). For each configuration the *excess* is Σ over key classes (class size − largest group of equal key values):
excess 0 = strict, excess 1 = exactly one crib seat disagrees, which is exactly "one wrong letter at a crib seat". Same family and
conventions as case 112; p 1–22 counted, hit lines printed for excess ≤ 1 at p ≤ 18 and for strict hits at every p.

**Gate R (reproduction): PASS.** Strict counts reproduce case 112 exactly: K4 p 1–21 0 and p 22 **720**; cycle 124's null1 (seed 125)
p 21 **4** and p 22 **144**, p ≤ 20 0. Two independent codes agree on the published strict result.

**Gate P (seed 209233): 20/20 PASS** (bar ≥ 19). Plants from an independent textbook encryptor (`plant219.py`): w 9 / 10, random
order, read, direction, alphabet, Vig / variant / Beaufort, model A / B, p 2–18, K1–K3 English windows with the cribs; each run on its
true π[0] slice with everything else free. All 20 true cells were reported at their true p, and the crib-key decrypts match the plants
at every determined position (82–97 letters known). Of the 10 corrupted plants, 8 came back at excess 1 (seat named exactly in 4,
ambiguous two-member class in 4); in 2 (ids 9, 13) the wrong seat sat alone in its key class, so no crib test can see it — they came
back at excess 0 with that one class decrypting wrongly, which the pre-registered pass rule allows.

**Results (w 9 + 10 pooled; counts are configurations at excess ≤ 1; eight nulls = shuffled K4, seeds 209234–209241).**

| p | K4 | nulls (209234 … 209241) | label (PREREG219 rule) |
|---|---|---|---|
| 1–16 | **0** | 0 in all eight | **`EXACT-EXCL (one-error scope, discriminating)`** |
| 17 | **0** | 0,0,0,0,0,0,8,0 | **`EXACT-EXCL (one-error scope, discriminating)`** (7/8 nulls 0) |
| 18 | 2 | 0,5,0,8,5,0,7,2 | `INSUFFICIENT-DISCRIMINATION` (K4 inside the null range) |
| 19 | 14 | 0,8,5,56,0,52,234,14 | `INSUFFICIENT-DISCRIMINATION` (strict claim already underdetermined) |
| 20 | 3 | 48,70,44,15,2,27,16,18 | same |
| 21 | 1,928 | 371–1,175 | same |
| 22 | 16,488 (720 strict) | 10,031–19,205 | same |

K4's two p 18 cells (both w 10, ROW read, A–Z tableau, Vigenère, key before, excess 1 with a two-member class; one on σ, one on σ⁻¹, of *different* orders) are crib-distinct
and leave 91 of 97 letters determined. Both decrypt to gibberish (mean log10 quadgram **−7.15**, English ≈ −4.2 to −4.7; e.g.
`RV?MDQPHEHAHZPQIEFES?EASTNORTHEASTAXVZ?ZSBUW…BERLIOCLOCK…`). So nothing at p 18 is a candidate, but by the label rule fixed in
advance p 18 is `INSUFFICIENT-DISCRIMINATION`, not an exclusion: with one error allowed, five of eight shuffles also fit there.
Heavy wall 214 s (11:54:32–11:58:06 PT), 130 jobs, `setsid` + `timeout 480`.

**What this changes.** Case 112's strict exclusion (p ≤ 18) now **survives one wrong crib letter or one wrong carved crib letter for
p ≤ 17** (exact under the stated family). At p 18 the one-error version cannot tell K4 from shuffled text; the strict p 18 claim of
case 112 still stands as it was. No tail probability is claimed from eight nulls (0/8 only bounds the per-text rate, CP95 < 0.31).

**Blind spots.** w 11 under one error not run (case 114 Part B is strict; ≈ 11× the cost → I-312); a dropped / inserted letter (shifts
alignment, not an "error at a crib seat") not covered; two errors; Quagmire I / II alphabets of case 114 Part A not rerun one-error;
rotations, non-tableau alphabets, running keys as before. The excess test cannot see an error whose seat is alone in its key class (as
plants 9 and 13 show); for such errors the strict and one-error tests are identical.

## Part A — the Voynich desk's blind recounts (attributed; verified read-only, nothing run under her folder)

**Case 203 addendum (π sub-list; desk `c217-pi/README.md`, 2026-11-19 ~08:17 PT).** Own C (`pi217x.c`), own π from three sources
(mpmath, integer Machin, OEIS A000796; identical, 700 digits). Anchor gate: her 800 π windows (400 offsets × s ∈ {0, −1}) are all in
`keys217.tsv` and byte-identical in `keys217.bin`. Result: **0 hits at ≥ 23/24 in A1 direct (1.8 × 10¹³), A2 bank (3.3 × 10¹³), A3
all.bin (3.3 × 10¹³)**, for every offset (`per_offset_k4.tsv`: 800 rows, sum 0); her own plants (seed 11789, 10 with a wrong carved
crib letter) 20/20; null #0 (seed 209230, byte-identical to ours, sha cc79f615…) 0 hits on the full family scopes (stricter than our
1/10 slices). **Verified here:** her input shas equal PREREG217's prefixes (alpha 2b4ffb69, bank 004ffc24, all 8a9e1b32, themed144
e0c1b627, k4 2797de14, keys217.bin d9674e65); her `keys217.tsv` copy equals `data/cycle217/keys217.tsv` (d7aa40af…); the repo's
`keys217.tsv` has exactly 800 π rows; her run logs show completed wall times (1.3 s / 2 min 04 s / 1 min 51 s); our case 203 K4 files
say 0 hits. Status: **independent recount agrees — π part of I-304 `EXACT-EXCL` confirmed by a second code.**

**Case 202 addendum (stage 2; desk `c202-stage2/README.md`).** Own `stage2.py` (exact mod 2 / mod 5 elimination); self-test 200/200
planted Gromark and periodic keys consistent, 0/200 random. She re-derived all 41 + 44 + 78 S lines from (perm, dir, X, Y, form):
0 mismatches. Her K4 counts with the failing seat dropped: **direct G 22–25 0, P 25 1; bank G 22 / 23 / 24 / 25 = 0 / 0 / 4 / 2,
P 25 0; all.bin 2 / 8 / 12 / 16, P 25 4**; no line consistent at Gromark L ≤ 21 or periodic P ≤ 24 in any scope. **Verified here:**
`data/cycle216/summary216.json` → `models` gives exactly the same twelve K4 line counts, and `data/cycle216/A/k4_*.txt` match
`data/cycle216/SHA256SUMS` (her `sha_check.txt` and my recheck). She adds two things the case did not print: the lines collapse to
distinct crib maps (bank G 22–25: 4 lines → 2 maps; all.bin 30 → 15; P 25: direct 1 → 1, all.bin 4 → 2), and the direct P 25 line
has 10,000 solutions, above PREREG216's enumeration cap of 1,000 — so under that prereg's own rule it is
`INSUFFICIENT-DISCRIMINATION`, consistent with case 202's NO-SIGNAL reading at L ≥ 22. Status: **independent recount agrees.**

**Caveat (her disclosure, both recounts).** She saw the `git log` subject lines of 5b1783a / 7cca6ab and 02fd1ac / 5ac8535, which state
the results (0 hits, 20/20; cell counts 41 / 44 / 78; "L ≥ 22 NO-SIGNAL"), before counting. The recounts are independent in code and
inputs but **not fully blind**. Not opened by her: gn217.c, check216/217.py, summary216.json, case files 202 / 203.

## Part B — every results file now names its input and scope

The desk noticed that case 203's `k4_direct.txt` and `null0_direct.txt` are byte-identical (sha a2e197b3…): a zero-hit output was only
the summary line, which names neither the text nor the scope. Case 204 has the same pair (35d33503…), and her own six zero-hit outputs
in `c217-pi/out/` are empty files with one shared hash. **Fix (from this cycle):** `tools/cycle219/stamp219.py` writes a `#` header —
scope, text label, sha256 of the exact 97-letter input, tool sha256, seed, arguments — at the top of every results file, and
`summary219.json` lists the input sha per text. All cycle 219 results carry it (K4 input sha eea81357…, no newline). Older files stay
frozen; `data/cycle217/MANIFEST.tsv` and `data/cycle218/MANIFEST.tsv` now attribute each zero-hit file to its text and input sha,
marked as a retroactive attribution from the run scripts (a zero-hit file cannot prove its own input).

## Files
[`data/cycle219/`](../data/cycle219/): `K4.txt`, `null1_124.txt`, `null2092xx.txt` (stamped hit lines + per-p counts),
`plants/` (20 stamped plant outputs), `summary219.json`, `analyze219.log`, `plants219.tsv`, `nulls219.tsv`, `texts.tsv`, `time.txt`,
`SHA256SUMS`. Tools: [`tools/cycle219/`](../tools/cycle219/).

## Verdict
No solution. Keyword / arbitrary columnar of width 9–10 with a periodic tableau key is now excluded for p ≤ 17 even if one crib or
carved crib letter is wrong; at p 18 one error is beyond what the cribs can discriminate. Two blind recounts by the desk agree with
cases 202 and 203. **K4 still standing.**

## Addendum (cycle 220, 2026-11-19) — the Voynich desk's blind recount; seat convention at p 18; leaks
- **Recount.** The Voynich desk recounted this case with her own code: voynich-case-files
  [`1d102cc`](https://github.com/Phuderoso/voynich-case-files/commit/1d102cc1416d762c1eabb477e52f695a71045c31)
  (`audits/kryptos/c219-oneerror/`, FROZEN_COUNTS sha 99d5438b…). Every strict / one-error count from p 1 to p 22, every label and
  gate R match this file exactly.
- **p 18 seat convention.** The two p 18 cells have a seat conflict (seats 32 and 68 disagree inside one key class). The quadgram
  mean depends on how that letter is decrypted: '?' −7.077; first-seat rule (used above) −7.153; trust seat 68 −6.970; force the crib
  −6.740. All are below the −6.0 candidate bar, so the label `INSUFFICIENT-DISCRIMINATION` does not change.
- **Blinding leaks (declared).** `data/cycle219/K4.txt` is an output but is named like an input; she saw its w 9 lines and part of
  w 10 before freezing her counts. My request message also gave away p 17 = 0 and −7.15. Her recount is independent in code, not
  fully blind. **House fix:** from cycle 220 results files are named `results_*.txt` (`data/cycle220/results_k4.txt`, …).

## Addendum (cycle 221, 2026-11-19): the Voynich desk's null-interval audit
The Voynich desk published an open (not blind) audit of the p 18–22 null ranges at voynich-case-files `0185ed5`
(`audits/kryptos/c205-null-interval/`, seed 11800). Counts match our raw files and `summary219.json`. Her reading, verified only to the
point that the counts match: p 18 (K4 2) and p 19 (K4 14) sit mid-null (Clopper–Pearson lower bound 0.157), so no number of extra nulls
turns them into exclusions; p 20 (K4 3) is low and would resolve with about 21 nulls (43 for 80 % power); **p 21: K4 1,928 lies above all
8 nulls (max 1,175, 1.64×)** — an observation only, not a lead; showing it at 5 % needs ≥ 146 nulls with none above; p 22 is typical.
**No label changes.** Adopted for planning (I-318): a rank rule (CP on the tail) instead of the interval rule for future null-count
comparisons, with the p 21 excess queued as a structural check (likely crib-forced cells) before any extra nulls are spent.
