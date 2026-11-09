# Cycle 175 pre-registration (IDEAS I-111 + I-113, grid with the I-115 correction, I-116 smoke rule, I-117 two-sided report)

Written and pushed **before** any K4 or registered-null run of the models below. Date: 2026-11-09, ~05:58 PT.
Smoke/benchmark runs so far (I-116): only on the reserved shuffle `random.Random(9175).shuffle(list(K4))`
(`ODAQWOFVOH…`), never on K4 or a registered null: `slip175` delx on perms 0–9,999 of `dec98.bin` (2.7 s, 8 threads) and
`hill175` n 2–4 on perms 0–4,999 of `all.bin` (0.9 s). Nothing below was changed because of their counts.

## Families and models
1. **I-111, two slips behind K3-law decimations** (`slip175.c`, built on `tools/cycle173/anom173.c`, same conventions):
   - **delx**: one letter of the true ciphertext C′ (98 letters, index d = 0..97) was left off the copper **and** one carved letter under
     a crib is wrong (any one of the used cribs is dropped from the test). Perms: the 170,258 K3-law decimations for n = 98 (`dec98.bin`).
   - **insx**: one extra letter carved at carved index d (0..96, C′ 96 letters) **and** one wrong crib letter. Perms: 168,858 (`dec96.bin`).
   - Periodic key, tableaux (PA, CA) ∈ {A–Z, KRYPTOS}², Vigenère (= variant-Beaufort test) and Beaufort, key at plaintext index (pt) or at
     C′ index (ct), p = 1..26, exact on the remaining 23 (or 22) crib letters. A configuration = (perm, d, dropped crib, frame, PA, CA, mode, p).
   - This is a superset of cycle 173's del/ins (every strict fit appears once per droppable crib); cycle 173 found none at p ≤ 18/19.
2. **I-113, Hill n = 4** (`hill175.c`; same models as `hill174.c`, new kernel-basis solver mod 2 and mod 13 with CRT): linear P = D·Z and
   affine P = D·Z + e, numbering A–Z and KRYPTOS, block offsets 0–3, both orders, behind the 165,782 decimations/routes of `all.bin`.
   K4 is also re-run at n = 2–3 with the new solver as a known-answer check against case 162 (must give 0 consistent, same config counts).

## Texts
- K4 (97 letters) on the full families (the exact verdicts).
- 19 nulls: `random.Random(seed).shuffle(list(K4))`, seeds **175000–175018**, on every 8th perm (`dec98_s8`, `dec96_s8`, `all_s8` = `P[::8]`);
  K4 is also run on the same `_s8` files so the grid compares like with like. (1/8 instead of cycle 173's 1/4 for the budget.)

## Information filter (I-115) — fixed now
checks(config) = number of equations beyond unknowns: for the periodic key, (#crib letters used) − (#residue classes they occupy);
for Hill, Σ_rows max(0, m_r − u). **KMIN = 4.** Only configs with checks ≥ 4 enter the grid.
Full counts (all configs) are still reported, beside the analytic chance expectation of each model × p.

## Grid (I-110 rule with the I-115 correction and the I-117 two-sided report) — fixed now
Five cells (≤ N/4 with N = 19 nulls), statistic per text on the `_s8` files:

| cell | statistic |
|---|---|
| C1 | delx, p 1–16, consistent configs with checks ≥ 4 |
| C2 | insx, p 1–16, same |
| C3 | delx, p 17–26, same |
| C4 | insx, p 17–26, same |
| C5 | Hill n 4 (linear + affine, both numberings, both orders, all offsets), consistent configs with checks ≥ 4 |

- Per cell, leave-one-out z (x − mean of the other 19) / sd of the other 19.
- **I-115:** a cell whose **19 nulls all have the same value** (zero null variance) is reported but **not scored**. If K4 differs from that
  common value in such a cell, this is reported as a flag (and is decided by the exact count and the decodes, not by the grid).
- Upper grid statistic G⁺ = max z over scored cells; **grid p⁺ = (1 + #{nulls with G⁺ ≥ G⁺_K4}) / 20** (null's own z also leave-one-out
  among the 20 texts). Best attainable 0.05.
- **I-117 two-sided:** G⁻ = min z over scored cells; p⁻ = (1 + #{nulls with G⁻ ≤ G⁻_K4}) / 20. A deficit (p⁻ = 0.05) is reported as
  "K4 fits less often than chance in cell X", which would point at a model/convention mismatch to audit, never at a solution.
- No scored cell → "grid not informative" (stated as such). No single-cell rank is quoted as evidence.

## Verdict labels
- Per model × p: K4 full-family count 0 and summed analytic chance expectation < 1 → **EXACT-EXCL** (under the stated perms, tableaux, frames).
- Expectation ≥ 1 → **LOW-POWER** for that p; hits at p ≤ 20 are decoded (crib-fixed key, '?' elsewhere) and scored (mean log10 quadgram,
  off-crib windows), K4's best vs the nulls' best → **NO-SIGNAL** if inside.
- Hill n 4 per sub-cell (aff × ix): K4 consistent 0 and expectation < 1 → EXACT-EXCL; expectation ≥ 1 → LOW-POWER, decodes scored as above.
- A solution claim needs a readable decode outside the cribs **and** a count/score beyond every null.

## Controls (`plant175.py`, independent string-level encryptor, no code shared with the C tools)
- 6 two-slip plants (3 delx, 3 insx; p ≤ 16; mixed tableaux, modes, frames), each hidden in a 200-perm slice at slot 100: must be found
  at the planted (t, d, dropped crib, PA, CA, mode, frame, p) with crib-fixed key letters equal to the key.
- 1 strict-del plant (no crib change): must be found (superset).
- 1 negative: del + **two** changed crib letters: must be MISSED at the planted configuration.
- Replay: cycle 173's plant ctl10 (`plant173.py` seed 173100; del + one changed crib letter, missed by design in case 161) must now be FOUND
  with crib 5 (plaintext position 26) dropped.
- Hill n 4: 4 plants (linear/affine, A–Z/KA, ix 0/1, offsets 0–3) must be found at the planted perm and sub-cell and decode to the plaintext;
  1 negative (one carved crib letter altered) must be missed.

## Independent recount
- `recount175.py` (numpy, different formulation: a drop is consistent iff every conflicting pair touches it, counted from the full
  conflict matrix): HIST/HISTK/EXPECT per p on K4 perm slices of both families, a null slice and the plant slices; must match exactly.
- Hill: brute force over all row vectors mod 2 and mod 13 (2^u and 13^u, CRT) on sampled configs and on every K4 consistent config;
  solvability and solution counts compared per row.

## Budget
≈ 8 min of heavy computation in total; resumable chunks (files with `END` are skipped).
