# PREREG219 — cycle 219 pre-registration (filed before anything below is run on K4, the plants or the nulls)

Filed 2026-11-19 ~11:55 PT (America/Vancouver). Slots: 217 new family (case 203), 218 new family run in a free slot (case 204), so
219 is an **audit** (I-310); 220 is free; a new family is due by **221**. Base: main b5aef4c (cycle 218 published by Firefly).
Seeds: next free 209233. Reserved here: **209233** (plants), **209234–209241** (eight shuffled-K4 nulls). Next free after this
cycle: **209242**.

## Part A — addendum: the Voynich desk's blind recounts (desk work, no K4 run)
File her two recounts (`/workspace/voynich/kryptos-audits/c217-pi`, `.../c202-stage2`, read-only) as addenda to cases 203 and 202,
**after** checking her numbers against the repo myself: input sha256 vs PREREG217 / data SHA256SUMS; the π window list vs
`data/cycle217/keys217.tsv`; her stage-2 table vs `data/cycle216/summary216.json`. Caveat to print: she saw the `git log` subjects
(which state the results) before counting, so her recounts are independent in code but not fully blind.

## Part B — tooling fix: every results / summary file carries its input sha256 and a scope label
Found by the desk: case 203's `k4_direct.txt` and `null0_direct.txt` have the same sha256 because a zero-hit output is only the
summary line, which names neither the input nor the text. From this cycle on, every results file written by a cycle tool starts with
a `#` header (`stamp219.py`): scope label, text label, sha256 of the exact 97-letter input, sha256 of the tool source, arguments,
seed; summaries repeat the per-file input sha. The fix is applied to this cycle's tools; older files stay frozen (not rewritten).

## Part C — audit (I-007, part of I-003): case 112 under one crib error
**Exclusion audited.** Case 112 (cycle 124): no column order of width 9 or 10 (all 9! + 10! = 3,991,680 orders; COL / ROW read;
both directions) with a periodic Vigenère / variant / Beaufort key p ≤ 18 on the A–Z or KRYPTOS tableau, key before or after,
fits all 24 crib letters. That is a **strict** claim (24/24). I-003 asks whether it survives **one** wrong letter.

**What "one error" covers.** One wrong crib letter, or one wrong carved letter at a crib seat (both make exactly one of the 24
equations wrong). A wrong carved letter elsewhere never touched the strict test. **Not covered:** a dropped / inserted letter
(alignment shift), two errors, widths ≥ 11, rotations, non-tableau alphabets.

**Tool.** `col1e.c`, written fresh (transposition built by ranking grid cells, not cycle 124's `place()`); per configuration the
excess = Σ over key classes of (class size − largest equal group); excess 0 = strict, excess 1 = one seat dissents. Counts per p
for p 1–22; hit lines printed for excess ≤ 1 at p ≤ 18 and for strict hits at every p. Same family and conventions as case 112.

**Gate R (reproduction, fixed now).** Strict counts from `col1e` must reproduce case 112's published K4 counts exactly
(w 9 + 10: p 1–21 strict 0, p 22 strict 720) and null1 of cycle 124 (seed 125: p 21 4, p 22 144). If not, stop and diagnose; no label.

**Gate P (plants, seed 209233, `plant219.py`, independent textbook encryptor).** 20 plants (w 9 / 10 alternating in pairs, random
order, read, direction, alphabet, form Vig / variant / Beaufort, model A / B, p 1–18, random key, 97-letter K1–K3 English window with
the cribs); odd ids have one carved crib letter changed. Each plant runs on its true π[0] slice (1/9 or 1/10 of the orders, all
other parameters free). **Pass** iff the true configuration is reported at its true p with excess ≤ 1, and the crib-key decrypt
matches the plant at every key-determined position (corrupted plants: outside the corrupted seat's key class). **Bar ≥ 19/20**,
else no label.

**Nulls (seeds 209234–209241).** Eight shuffled K4 (`random.Random(seed).shuffle`), full scope (all orders, w 9 + 10, p 1–22).
Eight nulls are a calibration of the count scale only; **no tail probability is claimed from them** (with 0 of 8 a rate is only
bounded, CP95 < 0.31 per text).

**Labels (fixed now), per p, over w 9 + 10 (all modes pooled).**
- K4 one-error count 0 → `EXACT-EXCL (one-error scope)`; tagged *discriminating* if ≥ 6 of 8 nulls are also 0, else
  *exact but saturated-null* (the exclusion holds; the nulls show the tolerance admits chance fits at this p).
- K4 count > 0 → each crib-distinct hit is decrypted with the crib-derived key (majority per class, `?` where undetermined) and scored
  by mean log10 quadgram over runs of known letters (`qg.bin`). A hit with ≥ 50 % determined and score ≥ −6.0 → `CANDIDATE`
  (manual read). Otherwise: K4 count within the null range → `INSUFFICIENT-DISCRIMINATION` (one error cannot be excluded at this p;
  the strict case 112 claim still stands); K4 above all eight nulls → `NO-SIGNAL (excess over 8 nulls, gibberish)` with rank only.
- p 19–22: strict claim was already underdetermined; one-error counts reported, no label beyond `INSUFFICIENT-DISCRIMINATION`.

**Budget.** Measured on a cycle-124 public control: one w 10 slice ≈ 12 s → ≈ 17 s wall per text on 8 cores; K4 + 8 nulls + 20 plant
slices + the gate-R null ≈ 4 min. Heavy ≤ 8 min wall, `setsid` + `timeout 480`, own process group.

**Disclosures.** Before filing: `col1e` was compiled and timed on cycle 124's public control ctl1 (slices 4 and 5) to check speed and
that the strict PALIMPSEST / KRYPTOS p 7 cell is found; plants (sha fded53a4…) and null strings (d141133b…) were generated. No run on
K4, the plants or the nulls. `col1e.c` sha 1a602f0e…, `plant219.py` 76a522de….

## Part D — news check (2026), noted in the journal.
