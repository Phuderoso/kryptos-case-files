# PREREG220 — cycle 220 pre-registration (filed before anything below is run on K4, the plants or the nulls)

Filed 2026-11-19 15:44 PT (America/Vancouver). Slots: 219 was an audit (case 205); 220 is a **free slot** (I-314: prefer I-312
chunk 1); **221 must be a new family**. Base: main 370fc1b (cycle 219 published by Firefly).
Seeds: next free 209242. Reserved here: **209242** (plants), **209243–209250** (eight shuffled-K4 nulls). Next free after this cycle: **209251**.

## Part A — addendum to case 205 (desk work, no run)
Cite the Voynich desk's blind recount of cycle 219 (voynich-case-files 1d102cc, `audits/kryptos/c219-oneerror/`): every p 1–22
count, label and gate R matches. Record (i) the p18 seat-conflict convention scores (−7.077 '?', −7.153 first seat, −6.970 seat 68,
−6.740 forced crib; all < −6.0, verdict unchanged); (ii) blinding leaks: `data/cycle219/K4.txt` is an output named like an input and
she saw part of it; my request message disclosed p17 = 0 and −7.15. House fix from now on: results files are named `results_*.txt`.

## Part B — I-312 chunk 1: case 114 Part B (all 11! orders, four alphabet pairs, p ≤ 18) under one crib error
**Exclusion audited.** Case 114 Part B (cycle 126): no width-11 column order (COL / ROW read, σ and σ⁻¹) with a periodic
Vigenère / variant / Beaufort key p ≤ 18 on A–Z, KRYPTOS (Quagmire III), Quagmire I or Quagmire II, key before or after the
transposition, fits all 24 crib letters. Strict claim. **This cycle covers the chunk π[0] ∈ {0, 1}** (2 × 10! = 7,257,600 orders,
2/11 of the space). Chunks π[0] ∈ {2..10} follow in later free slots; no label for the whole of w 11 until all chunks are done.

**Tool.** `col1e4.c` = cycle 219's `col1e.c` with a minimal diff: NAL = 4 adds Quagmire I (keyed PT alphabet, straight CT) and
Quagmire II (straight PT, keyed CT); optional SECOND fixes π[1] so work splits into resumable sub-slices of 9! orders.
"One error" = excess ≤ 1 (one crib seat dissents), same definition and blind spots as case 205 (no alignment shifts, no two errors).

**Gate T (tool identity, already run as a smoke test before filing, disclosed):** `col1e4 … NAL=2` on K4 w10 π[0]=3 is byte-identical
to cycle 219's `out/K4/w10_f3.raw`. **Gate S:** the nine π[1] sub-slices of that slice sum to the same per-p strict / one-error
counts. **Gate R (weak, consistency only):** K4 strict count is 0 at every p ≤ 18 in the chunk (case 114 Part B: 0 survivors).
If any gate fails: stop, diagnose, no label.

**Gate P (plants, seed 209242, `plant220.py`, independent textbook encryptor).** 20 plants, all w 11, alphabet pair = pid mod 4
(five per pair), random order / read / direction / form / model, p 1–18, random key, 97-letter K1–K3 English window with the
cribs; odd ids have one carved crib letter changed. Each plant runs on its true (π[0], π[1]) sub-slice, all other parameters free.
**Pass** iff the true configuration is reported at its true p with excess ≤ 1 and the crib-key decrypt matches the plant at every
key-determined position (outside the corrupted seat's key class). **Bar ≥ 19/20.** A pass validates recovery in this scope only.

**Nulls.** Eight shuffled K4 (seeds 209243–209250) over the same chunk. No tail claims from eight nulls.

**Labels per p (chunk scope, same rule as case 205):** K4 count 0 and ≥ 6/8 nulls also 0 → EXACT-EXCL (one-error, discriminating);
0 but nulls saturated → EXACT-EXCL (exact but saturated-null); K4 > 0: any distinct cell with ≥ 49 key-determined letters and
quadgram mean ≥ −6.0 → CANDIDATE (manual read); else K4 ≤ max null → INSUFFICIENT-DISCRIMINATION; else NO-SIGNAL.

**Budget.** ~8 min wall on 8 cores, `setsid` + `timeout 540`, own process group only. Sub-slices that do not finish are not
counted and are reported as incomplete (resumable next free slot).
