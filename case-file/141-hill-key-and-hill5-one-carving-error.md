# Case file 141 — Hill + key and Hill 5×5 under one carving error (cycle 153)

**Cycle 153, 2026-11-08. Variant / audit** (IDEAS [I-040](../IDEAS.md), part of [I-003](../IDEAS.md); follows [case 139](139-hill-one-carving-error.md)).

## Why
Case 139 showed that plain Hill n = 2–4 stays excluded with one wrong carved letter. Its audit table left the two Hill extensions
strict-only: **Hill + an additive key of independent period** ([case 132](132-hill-plus-periodic-key.md), cycle 144; includes the affine
Hill of [case 131](131-affine-hill.md) as k = n) and **Hill 5×5** ([case 129](129-hill-5x5.md), cycle 141). K1–K3 each carry a one-letter
slip, so a strict "all 24 crib letters" exclusion of these families could have thrown out the true key.

## Model and method (`tools/cycle153/hillk1e.c`)
Decoder `out[t] = D·L_block + e[t mod k] (mod 26)`, k = 0 for plain Hill. Same frames as cycles 141/144/151: direct; behind all 165,065
bank entries in both directions, model Q (transposition undone first) and carved order (Hill + key on the carved text, then transposition);
A–Z and KRYPTOS numbering; every alignment. Cribs at the official positions (EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-based).

- A **substituted** carved letter sits in exactly one Hill block, so only that block's crib equations can break.
- Exact screen without enumeration: per configuration the full system `[A | b]` is reduced once per field (mod 2, mod 13) to its
  left null space H and syndrome s. Dropping the equations E of one block is consistent **iff s ∈ span(H[:,E])**.
- **Exact one-letter repair:** for a passing block, the system without E gives x = x₀ + N·y. Changing carved letter j of the block by δ
  (1–25) turns each dropped equation into `a_t·x + δ·D[r_t][j] = b_t`, which is linear in y; it is checked exactly in both fields for every
  (j, δ). Consistent repairs (`repair_cons`) are enumerated for invertible D (`repair_inv`), decrypted with the repaired letter and scored
  (mean log10 quadgram, English ≈ −4.1, shuffled ≈ −7). Sets above 4,096 solutions are counted, not decoded (`repair_under`, blind spot).
- **One wrong crib letter:** leave one equation out, same syndrome test, survivors enumerated and scored (`eq_inv`, `eq_under`).
- Strict-consistent configurations (`strict`) are counted and skipped: they were handled by cycles 141/144. The strict counts
  reproduce cycle 144 exactly (n 3 k 9: 4; k 10: 22; n 4 k 3: 134; k 4: 224), an implicit regression check.

Scope: Hill + key n = 2 k 1–14, n = 3 k 1–10, n = 4 k 1–4 (2.64, 3.96, 5.28 million configurations per (n,k) and text); Hill 5 (k = 0)
direct exhaustively (solution cap 2,000,000) and behind the bank on every 20th entry, **count only** (no decoding). Texts: K4 and two
shuffled-K4 nulls at the same scale. 494 s wall on 8 processes.

## Controls (`data/cycle153/controls_check.txt`) — 11/11
Nine planted encryptions of the English control text with **one corrupted carved letter** in a crib block (n2 k7 direct, n3 k5 model Q
KRYPTOS, n2 k11 carved, n3 k10 carved inverse entry, n4 k3 model Q, n4 k4 direct KRYPTOS = affine Hill, n2 k14 direct, Hill 5 direct A–Z
and KRYPTOS): all nine fail the strict test and are recovered with the **exact corrupted carved position** and its true letter, decrypting
with 0 wrong letters (−4.04 to −4.13). In ctl3 (n = 2, one crib equation in the block) three repairs satisfy the cribs; the true one is
among them, and quadgram ranking slightly prefers a wrong neighbour (WASKED for WALKED): the repair test is exact, ranking is not.
One uncorrupted control passes strictly; one control with **one wrong crib letter** is recovered by the leave-one-out path (decryption
differs from the crib text only at the planted position). The independent Python checker re-decrypted every control from the printed
D, e and repaired letter without the C code.

## Independent count check (`data/cycle153/independent_check.txt`)
A pure-Python **repair-and-resolve** counter (rebuild all 24 crib equations on each of the n·25 repaired texts per block, plain Gauss
mod 2 and mod 13, no syndrome trick) reproduced `tests`, `strict`, `eqdrop_cfg`, `blockpairs`, `repair_cons` and `repair_cons_cfg`
exactly on **94/94** jobs: all (n,k) direct for K4 and both nulls, plus seven K4 bank slices including the entries of the best survivors.

## Results (`data/cycle153/results.txt`)
Counts are configurations with at least one consistent one-letter repair (`rc`) / with an invertible D (`ri`); best = best repaired decryption.

| n | k | K4 rc / ri | null1 rc / ri | null2 rc / ri | K4 best | nulls best | label |
|---|---|---|---|---|---|---|---|
| 2 | 1–14 | 0 / 0 | 0 / 0 (k 14: 4 / 0) | 0 / 0 | — | — | **EXACT-EXCL** |
| 3 | 1–6 | 0 / 0 | 0 / 0 | 0 / 0 | — | — | **EXACT-EXCL** |
| 3 | 7 | 0 / 0 | 2 / 2 | 2 / 0 | — | −8.25 | **EXACT-EXCL** |
| 3 | 8 | 24 / 4 | 10 / 6 | 10 / 10 | −8.19 | −7.70 / −7.93 | NO-SIGNAL (exhaustive decode) |
| 3 | 9 | 140 / 32 | 112 / 60 | 84 / 38 | −7.47 | −7.55 / −7.37 | NO-SIGNAL (exhaustive) |
| 3 | 10 | 3,308 / 1,342 | 4,214 / 1,592 | 2,938 / 1,402 | −7.15 | −7.20 / −7.14 | NO-SIGNAL (exhaustive) |
| 4 | 1 | 78 / 26 | 86 / 26 | 88 / 44 | −7.79 | −7.55 / −7.58 | NO-SIGNAL (exhaustive) |
| 4 | 2 | 620 / 324 | 580 / 330 | 616 / 374 | −7.35 | −7.07 / −7.36 | NO-SIGNAL (exhaustive) |
| 4 | 3 | 6,500 / 4,014 | 7,048 / 4,182 | 6,080 / 3,720 | −6.76 | −6.98 / −6.91 | NO-SIGNAL (2 null pairs undecoded) |
| 4 | 4 | 8,720 / 5,462 | 7,766 / 5,160 | 8,124 / 5,236 | −6.75 | −6.87 / −6.79 | NO-SIGNAL (K4 212 repair + 90 crib-error pairs undecoded) |
| 5 | 0 direct | 8 / 6 | 9 / 7 | 7 / 6 | −6.94 | −7.10 / −7.07 | NO-SIGNAL (exhaustive, 10 configs) |
| 5 | 0 bank 1/20 | 153,409 of 330,160 | 153,142 | 151,693 | not decoded | — | **LOW-POWER** |

One wrong crib letter: K4 0 survivors for n = 2 (all k) and n = 3 k ≤ 6; elsewhere K4's counts sit inside the null range and every
enumerable survivor decodes to gibberish (best −6.90; nulls −6.78 / −6.83). No decryption of any text scored above −6.7, against ≈ −4.1
for English and −4.04 to −4.13 for the planted controls; no `S` line crossed the print threshold (−5.0) for K4 or either null.

## Verdict
**Negative.** Hill + additive key (n 2 k ≤ 14, n 3 k ≤ 7) is **excluded exactly even with one wrong carved letter or one wrong crib
letter** (`EXACT-EXCL`), direct and on either side of the 165k bank, A–Z/KRYPTOS. For n 3 k 8–10 and n 4 k 1–4 (affine Hill included)
the one-error screen alone cannot tell K4 from shuffled text, but every consistent invertible solution was decrypted (apart from the
counted blind spots) and none is within 2.6 log units of English: `NO-SIGNAL` with an exhaustive decode. Hill 5 direct: `NO-SIGNAL`,
exhaustive. Hill 5 behind the bank under one error: **`LOW-POWER`** — almost half of all configurations of K4 and of the nulls admit a
repair, and they were not decoded; that corner is open.

## Scope and blind spots
- Only a **substituted** letter; a dropped or extra carved letter (block shift) is IDEAS I-039.
- n = 4 k = 4: 212 consistent repairs and 90 one-wrong-crib sets of K4 exceeded the 4,096-solution cap and were not decoded
  (nulls 502 / 298 and 148 / 168); n = 4 k = 3: 4 crib-error sets.
- Hill 5 behind the bank: count-only, every 20th entry (16,508 of 330,130 directional entries), no decoding; affine Hill n = 5 (k = 5)
  under one error not run.
- Numbering A–Z / KRYPTOS only; transpositions only from the 165k bank; key periods as in cycle 144; key on the ciphertext side (I-012) untested; two errors untested.
- A wrong carved letter **outside** every crib block does not break the strict test, so the strict cycle 141/144 runs already cover it.

## Community check (2026-11-08)
Quick search: no new public K4 development (still unsolved; Paradigm's verifier and CTF unchanged; K5 not released).
