# Case 216 — Bounded-shift keys: a window of W consecutive shifts, or at most D distinct shifts, on two keyed alphabets (cycle 230)

**Slot:** new family (228 free, 229 audit, so 230 is new; I-334 / I-341). Pre-registered in
[PREREG230](../tools/cycle230/PREREG230.md) (local commit, 07:48 PT, filed before the registered run; one timestamp-text amend at 07:50
changed no threshold). Ideas: **I-299** (generalised, tested here for ranges), **I-341** (done), new **I-344–I-349**.
Code: [`tools/cycle230/`](../tools/cycle230/) (`bsk230.c` source sha 580159e6…, binary 52c8d591…); raw results: [`data/cycle230/`](../data/cycle230/).

## Why this family
Case 200 asked for key digits 0…9. I-299 queued other bases. Two observations make the queue item sharper:
1. A base-b digit key anchored at 0 with b ≤ 10 is a subset of case 200's range: **bases 5–9 were already excluded wherever case 200 was
   `EXACT-EXCL`** (direct, bank). Only b ≥ 11 and *offsets* are new.
2. The natural generalisations of "a small numeric key" are a **window of W consecutive shifts at any offset** (digits 1–9, a base-b
   key with the cipher alphabet slid, anything ≤ W values wide) and a **key alphabet of ≤ D distinct shifts at arbitrary values**
   (binary / ternary keys, a short keyword's letters reused in any pattern). Both constrain only the *range* of the key stream, so they
   cover periodic, Gromark, autokey and running-key structures at once. The coverage table fixes structure everywhere; range alone was
   never tested.

## Method
Model Q exactly as case 200 / `gron214.c`: shift k per letter on plain alphabet X, cipher alphabet Y; Vigenère, variant, Beaufort
forms; layer letter i carved at S[i] (family row, or its inverse). The 24 crib shifts are order-free. A (S, X, Y, form) **survives**
iff the 24 shifts fit one circular window of ≤ W values (primary W ≤ 9) or take ≤ D distinct values (primary D ≤ 6). `bsk230` lists
survivors with W ≤ 10 or D ≤ 6 and prints width and number of distinct values, so W ≤ 8 and D ≤ 5 are sub-counts of the same run.
Scopes: A1 direct (86,731 × 86,731 × 3 = 2.26·10¹⁰ pair-forms); A2 bank and A3 all.bin (165,065 / 165,782 rows × 2 dirs, 144 × 144
themed alphabets × 3 forms, ≈ 2.05–2.06·10¹⁰). Walls: K4 direct 90 s, bank 112 s (282 s mark), all.bin 110 s; whole run 482 s.
Nulls: 10 fresh shuffled K4 (seeds 209577–209586) at **1/20 scale** (X ≡ i mod 20 for direct; every 20th row from offset 2i for the
families); "null-equivalent" = (sum over the 10 nulls) × 20 / 10, i.e. the mean full-scale count. Disclosed in PREREG230: a K4 direct
smoke run was started by mistake before filing and killed unread (only its line count, 53, was seen).

## Gates
- **P (plants, seed 209576):** 20 plants (10 direct, 10 behind a random bank / all.bin row; window W 5–9 or D 3–6 value sets; i.i.d.
  key streams; K1–K3 English filler + cribs): the true (row, dir, X, Y, form) is a survivor in **20 / 20** (Wilson 95 % 0.839–1.000,
  bar ≥ 19/20) → **PASS**. Survivor lines per plant 2–111 (`analyze230.log`).
- **R (recount):** an independent Python re-derivation of width, distinct count and all 24 shifts of **every** K4 and null survivor line
  at the registered thresholds (decode230.py asserts): 0 mismatches. A loosened-threshold slice test (X = 7623, all Y, WMAX 14 / DMAX
  12) agrees exactly at the registered thresholds (6 / 6 cells) but **C and Python disagree at widths ≥ 14**: the tool measures width on
  signed offsets from k₀, which is only exact for arcs ≤ 13 values wide. Registered range (W ≤ 10) is unaffected; the tool must not be
  reused for W ≥ 14 unchanged (I-346).

## Results (K4 full scale; nulls 1/20 scale ×2 = null-equivalent)
| scope | criterion | K4 cells (clusters) | null counts, 10 nulls (1/20) | null-equivalent cells (clusters) | label |
|---|---|---:|---|---:|---|
| A1 direct | W ≤ 9 | 3 (2) | 0 0 2 0 0 2 0 0 0 0 | 8 (4) | `NO-SIGNAL` |
| A1 direct | W ≤ 8 | 0 | same cells (W 8) | 8 (4) | `EXACT-EXCL` (discriminating) |
| A1 direct | D ≤ 6 (and D ≤ 5) | 0 | all 0 | 0 | `INSUFFICIENT-DISCRIMINATION` |
| A2 bank | W ≤ 9 | **0** | 0 0 0 0 0 0 4 0 0 10 | 28 (4) | `EXACT-EXCL` (discriminating; nulls overdispersed: 2 of 10 texts) |
| A2 bank | D ≤ 6 | 4 (1; inverse twins, width 14) | 0 … 2 (one text) | 4 (2) | `NO-SIGNAL` |
| A3 all.bin | W ≤ 9 | 6 (2) | 0 0 2 0 0 0 0 2 2 0 | 12 (6) | `NO-SIGNAL` |
| A3 all.bin | W ≤ 8 | 0 | 0 0 2 0 0 0 0 0 0 0 | 4 (2) | `EXACT-EXCL`, thin (one null text) |
| A3 all.bin | D ≤ 6 | 0 | all 0 | 0 | `INSUFFICIENT-DISCRIMINATION` |
| all three | W ≤ 10 (descriptive) | 47 / 44 / 48 (22 / 8 / 20) | see `analyze230.log` | 22 / 68 / 58 (10 / 30 / 38) | descriptive; direct 22 vs 10 clusters is not separable with 5 null events (Poisson 95 % band for the null-equivalent ≈ 3–23) → `NO-SIGNAL`, replicate at full scale (I-344) |

(Cluster counts use the rule in `clus230.py`: same X and ≥ 16/24 shift agreement, direct or mirrored, or same X, Y, form; an
approximation of I-291's rule. Cells with the same X and near-identical Y alphabets, and inverse row twins, merge.)
A D ≤ 6 zero in the null runs says nothing about power: the chance rate for D ≤ 5 / 6 on the structured lists is below what 10 nulls at
1/20 scale can see, hence `INSUFFICIENT-DISCRIMINATION` as registered, not an exclusion.

**What is excluded.** Within the listed alphabets, a key stream confined to a window of ≤ 9 consecutive shifts (any offset, any
structure, plaintext- or carved-index) is excluded behind the 165,065-row bank (K4 0, null-equivalent 28 cells / 4 clusters); direct
and all.bin exclude W ≤ 8 only (direct discriminating, all.bin thin). **Every digit key with b ≤ 9 at any offset** is therefore
excluded in those scopes, and bank-scope digit keys up to 9 consecutive values. Nothing is said about alphabets outside the lists,
about one wrong crib letter, or about D ≤ 6 (no power measurement).

## Decode level (optimised, not the I-330 bar)
The key is *not* determined by the filter (only its range is), so the NC bar does not apply. For each survivor a free-key beam search
(width 3000, allowed set = covering window, or the observed shifts for D; cribs fixed) reports the best mean log10 quadgram:
- **K4** W ≤ 9 clusters: −3.456 (direct, X 7623 / Y 60126 / 60128), −3.436 and −3.446 (all.bin); D ≤ 6 bank cluster −3.929 (window 14).
  Best texts are quadgram-optimised gibberish ("THEASTSOMENTANTHERSTHEFARATIONSWHENBERLINCLOCK…").
- **Nulls** (15 survivor row-sets over the 10 nulls, W 8–9 or D 6): −3.50 … −3.94. **Plants:** the beam score exceeds the true plaintext's NC in 20 / 20
  (true −3.79 … −4.93) and reproduces the plaintext at only 23–88 % of the non-crib positions (0 / 20 at ≥ 90 %), so free-key decode is
  **not discriminating**: `decode-read 20/20` in `analyze230.log` holds only through the "score ≥ truth" clause and must not be quoted
  as a recovery rate.
- **Window calibration (post hoc, seed 209587, `winctl230.log`):** the K4 clusters' beam scores are not elevated: with 40 *random*
  width-9 windows (same rows, X, Y, form) the beam reaches ≥ the K4 value in 6 / 40, 13 / 40 and 14 / 40 cases (medians −3.53, −3.49,
  −3.49). The K4 values sit above the null texts (−3.50 … −3.72), but random windows on the same
  rows and alphabet pairs reach them as often, so the score reflects the pair, not the crib-consistent window; not a signal.
→ decode level `NO-SIGNAL` (K4 survivors are gibberish; K4 not above random windows).

## Voynich desk and notes
- Voynich desk, since 04:56 PT 2026-11-21: nothing addressed to Kryptos in `voynich-case-files` (only K096 khipu work; no C124 draft
  visible there; the C123 verdict, 734c50a, is not ours). Her **c229 recount** (`audits/kryptos/c229-nq-vs-search-size/`, frozen 04:52 PT,
  commits c2cec1c … 3046cd3, **not previously integrated here**): her per-nq table matches ours with 0 differences, the 8 hits / 4 distinct
  nulls match (nq 12, 13, 13, 19; none at nq 10–11), K4 0 passes. Her own fit: nq explains the null max better than ln N (R² 0.647 vs
  0.098; both 0.732); at N ≥ 100 / ≥ 1000 `NQ-DOMINATES`. This **refines I-342**: a bar indexed to nq (not total search size) is
  the better first design. The ln N regression is hers alone (open recount, not fully blind). **Not independently re-run by us.**
- Our side still owes: the blind review of her C124 draft (not visible) and the joint ZL3b vs IT2a word-split audit.

## News check (secondary / community; none changes the case)
- Paradigm's Kryptos page (dated 06.12.2026 on the page; WIRED, Steven Levy, 12 Jun 2026): Paradigm holds Sanborn's archive and runs a
  $1-per-guess hash verifier plus ten $1,000 CTF puzzles; Kobek stated the plaintext will never be published by him. K4 unsolved
  (kryptosbot.com FAQ, status 29 Sep 2026). Community: r/KryptosK4_AI (e.g. a 23 Oct 2026 "branching factorial model", Zenodo, a
  self-described algebraic reduction, no verified plaintext); akaalias/k4 (Claude-driven autoresearch loop, 198 experiments to
  2026-10-18, no champion); kryptosbot.com lists "Gromark with keyed alphabets on both sides" as partly tested and notes unanalysed
  circled letters on an archive tableau (physical lead). All unverified by us. Nothing new on K5, no auction news.

## Blind spots
Only the 86,731 and 144 themed lists; both layer orders collapsed by the filter; one wrong crib letter not covered (a one-error
version is I-345); D ≤ 6 has no measured power; W ≥ 14 untested (tool limit); 10 nulls at 1/20 scale are thin (bank W ≤ 9: 2 of 10
texts carry all null cells); cluster counts are approximate; a bounded range is a necessary condition only, so a surviving cell would
still need a structured key and a readable decrypt.

## Verdict
**No solution.** Bank W ≤ 9, direct W ≤ 8 (and thinly all.bin W ≤ 8) are `EXACT-EXCL`; the other cells are `NO-SIGNAL` or
`INSUFFICIENT-DISCRIMINATION`. Next free seed **209588**.
