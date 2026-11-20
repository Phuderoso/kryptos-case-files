# PREREG225 — cycle 225 pre-registration (filed before anything below is run on K4, the plants or the nulls)

Filed 2026-11-20 11:43 PT (America/Vancouver). Slot: **free** (I-324: 224 was a new family, 226 must be an audit, 227 a new
family). Base: main db63ac3 (cycle 224 published by Firefly). Seeds: next free 209537. Reserved here: **209537** (plants),
**209538–209545** (eight shuffled-K4 nulls). Next free after this cycle: **209546**.

## Part A — addendum to case 210 (desk work, no run)
Cite the Voynich desk's open recount of the case 210 V all.bin p 19 cell (voynich-case-files b0793db + 0128be8,
`audits/kryptos/c210-v-recount/`; FROZEN.txt sha256 5a65fbe8…85fed, RULE.md 3b94f944…40d24). Verified here before filing:
the published files hash to the values her README states, and K4 carries **Z** at carved positions 46 and 78 (0-indexed; Z also
at 47 and 70). Record: occupancy 11/100 (p 12/101 ≈ 0.12), raw rank 4/101 ≈ 0.040, K4 4 raw hits = **2 distinct tests**
(8314/8315 inverse pairs collapse; QWERTY and QWERTZ do **not**: their decrypts differ in 16/97 letters because two seats fall on
carved Z); correct case 210's "Y/Z not involved" sentence; label `NO-SIGNAL` stands on occupancy; rank on distinct tests is 0.040
if layouts stay distinct, 0.12 if forced together. Leaks as in her LEAKS.md.

## Part B — I-312 chunk 2: width-11 columnar, π[0] ∈ {2, 3}, four alphabet pairs, one crib error
Same exclusion audited as case 206 (case 114 Part B, strict) with the same tool, run on the next chunk:
**π[0] ∈ {2, 3}** = 2 × 10! = 7,257,600 orders (chunks done after this: 4/11). No label for all of w 11 until every chunk is done.

**Tool.** `tools/cycle220/col1e4.c` **verbatim** (sha256 de865865…e573f), `analyze225.py` = `analyze220.py` with the chunk
changed, gate S replaced by gate T, and a D2 rank column added.
Family as case 206: ragged 97-letter grid of width 11, COL / ROW read, σ and σ⁻¹, Vigenère (= variant) or Beaufort, key before
(model A) or after (model B) the transposition, p 1–18, A–Z, KRYPTOS (Quagmire III), Quagmire I, Quagmire II. One error =
excess ≤ 1 (one crib seat dissents). Binary formats: none new (text in, text out; `.raw` lines H / C as in cycle 220).

**Gate T (tool identity):** rerun K4, w 11, π[0] = 0, π[1] = 1 and require a byte-identical `.raw` to cycle 220's
(`/workspace/k4c220/w/out/K4/w11_f0_s1.raw`). **Gate R (weak):** K4 strict count 0 at every p ≤ 18 in the chunk.
**Gate P (plants, seed 209537, `plant225.py` = plant220.py with π[0] drawn from {2, 3}):** 20 w 11 plants, five per alphabet pair,
odd ids with one corrupted carved crib letter, each on its true (π[0], π[1]) sub-slice; pass iff the true configuration is reported
at its true p with excess ≤ 1 and the crib-key decrypt matches outside the corrupted key class. **Bar ≥ 19/20.**
Invariance pre-check (house rule): plant 0's statistic is non-zero, null shuffles move K4's counts (shown by the null spread).
If any gate fails: stop, no label.

**Nulls.** Eight shuffled K4 (seeds 209538–209545) over the same chunk (shuffle = random.Random(seed).shuffle of K4's letters).

**Labels per p (chunk scope, case 206 rule):** K4 count 0 and ≥ 6/8 nulls 0 → `EXACT-EXCL (one-error, discriminating)`; 0 but
nulls saturated → `EXACT-EXCL (exact but saturated-null)`; K4 > 0: any distinct cell with ≥ 49 key-determined letters and quadgram
mean ≥ −6.0 → `CANDIDATE (manual read)`; else K4 ≤ max null → `INSUFFICIENT-DISCRIMINATION`; else `NO-SIGNAL`.
**D2 + rank rule (I-322):** beside each K4 > 0 cell print D2 (distinct crib tests) and p_up = (1 + #nulls with D2 ≥ K4)/9.
With 8 nulls p_up ≥ 0.11, so no excess claim is possible this cycle; a cell with K4 D2 > every null is flagged for ≥ 40 nulls.
Null occupancy (nulls with ≥ 1 cell) is printed beside every exclusion.

**Budget.** ~8 min wall on 8 cores, `setsid` + `timeout 600`, own process group only; resumable sub-slices (a `.raw` is complete
iff it ends with a C line). Incomplete sub-slices are reported, not counted.

**Blind spots (stated in advance).** Only π[0] ∈ {2, 3}; one error only (no insertions / deletions / two errors); p ≤ 18;
rotation 0, short last row = leftmost columns; tableau alphabets only (no Quagmire IV); eight nulls give a scale, not a tail.
