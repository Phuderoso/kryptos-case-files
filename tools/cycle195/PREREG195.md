# PREREG195 — Sandwich compound key with a keyword columnar between the passes (IDEAS I-209 via pointer I-208)

Written and pushed **before** any K4 or registered-null run (~17:55 PT). Timing only on the reserved shuffle seed 9191 (I-116) under **I-180**.

## Novelty (prior-coverage grep, done first)
- `grep -il columnar case-file/*.md` (48 files) + README + IDEAS. Case 50 (cycle 52): the same 1,837 keyword column orders, single and double,
  with **one** periodic/progressive key on **one** side. Case 119 (cycle 131, model M = this sandwich's S1): **named** themed keyword pairs only,
  behind the 165,065 bank (keyword columnar there stops at width 8; long keywords were never behind it, case 111 audit). Cases 176–181: two
  **arbitrary** periodic keys, but only behind the 165,782 K3-law decimations/routes. **0 of the 3,674 single columnar rows are in all.bin**
  (6 of 16,928 double rows are; kept, flagged in `col2_index.txt`). Nothing tested two arbitrary periodic keys around a keyword columnar.

## Model (unchanged solver)
`cmp193.c` (case 180) **unchanged**; only the permutation bank changes. S1: z = s2·σ(s1·x + a[i mod m]) + b[C(i) mod n] with C the keyword
columnar (plaintext i carved at C(i)); S2 the reverse index assignment. tab4 (A–Z>KRYPTOS, KRYPTOS>A–Z, A–Z>A–Z, KRYPTOS>KRYPTOS), forms VV VB
BV BB, 625 ordered pairs 2 ≤ m, n ≤ 26 incl. m = n. Exact bijection-graph test; chance E_config = Π 26^(1−r_c) per config (I-193).
- **Banks** (`gen195.py`, from `data/cycle52/orders.txt`; `sub195.py`): col1.bin = 1,837 orders × {enc, inv} = 3,674 rows; col2.bin = ordered
  pairs of the 92 themed orders (incl. the same word twice, K3-style double), × {enc, inv}, minus col1 rows = 16,928; col1_th.bin = 184 themed
  rows of col1; ctl195.bin = 7 control rows. SHA-256 in [`sha195.txt`](sha195.txt). The keyword columnar is re-derived literally in `plant195.py`
  and asserted equal to the bank rows.

## Checks done before this file (disclosed)
- **I-180 probe** (reserved shuffle 9191): col1 2.9 s, col2 13.1 s on tab4. Full-power cells (cell E ≤ 0.05; text-independent): col1 5,792 of
  20,000, col2 5,760 of 20,000.
- **Meter (I-193, split by tableau type per I-205)**, 40 uniform texts seeds 19540–19579 on col1_s8 (460 rows) and col2_s32 (529 rows), tab2 and
  tab1s separately ([output](meter195_out.txt)): two-tableau at chance (col1 bands 0–5 z +1.74, +0.26, +1.25, −2.31, −0.63, +1.01; col2 +1.19,
  −0.65, −0.16, −0.90, +0.84; band 5 0 vs 0.87). One-tableau lumpy as in case 180 (col1 40 texts z −3.87/−5.26/−2.60 in bands 1–3); on 400 more
  texts (19580–19979) bands 0–3 z +0.93, −2.90, −1.89, −0.68 and band 5 one event (text 19580+270 = u19850, one 26-bundle in 4 equivalent cells,
  104 sols vs E 7.7). Huge |z| printed where E ≈ 0 and SD ≈ 1e−17 is a float artefact of meter193.py (z n/a).
- **Recount pre-K4:** `recount195.py` (= recount193.py) vs cmp193 on a uniform text (seed 19540), ctl195 rows 0–6, tab4: 40,550 fits identical.
- **Controls 14/14** ([output](controls195.txt), [plants](plants195.txt), seed 19500): P1–P9 positives on single, width-14, inverse and double
  columnar rows; **P5 = PALIMPSEST (A–Z Vig) → KRYPTOS keyed columnar → ABSCISSA (KRYPTOS Vig): found as the only fit at its row in all 3,674
  rows of col1, both keywords and all 97 letters recovered**; P6 found at its row in all of col2; negatives N1 three passes, N2 random key, N3 =
  P1 with one wrong carved crib letter (slot 3), N4 a case-178 compound key, **N5 a K3-route sandwich (all.bin 12345): no fit at any columnar
  row** (found at its own route row). **Rehearsal fix (disclosed):** the control run first printed only E_config ≤ 1e−4, which hid P4
  (width-14 ALEXANDERPLATZ, KA>AZ VB 6 × 19, E_config 0.0015; the solver did find it). The control print threshold was set to the registered
  0.002; negatives still judged at ≤ 1e−4.

## Registered run ([`run_cycle195.sh`](run_cycle195.sh))
- **C1** K4, tab4, all of col1 (3,674), S1 + S2, 625 pairs; print E_config ≤ 0.002.
- **C2** K4, tab4, all of col2 (16,928).
- **Grid** K4 + 19 shuffles (seeds 19511–19529, [`nulls195.txt`](nulls195.txt)) on **all of col1**, tab4.
- **C3** K4, 572 themed × {A–Z, KRYPTOS} tableau pairs (tp_c3) on col1_th (184 themed rows), H summed over tableau pairs (`agg193`).
- **Recount** recount195 vs cmp193 on ctl195 rows 0–6, tab4, texts K4, P1, P5, P6, n19511.

## Decision rules (as cycles 193–194)
Full-power cell (cell E ≤ 0.05): every fit decoded with `decode195.py`; a fit is a solution only if the 97-letter decryption is coherent English
with EASTNORTHEAST and BERLINCLOCK at the official positions, reproducible; fits that decode to gibberish at or near the chance rate →
**`EXACT-EXCL`** (chance fits decoded and rejected). Cell E > 0.05 → **`LOW-POWER`** (totals vs E, two-tableau and one-tableau apart, I-205; K4
vs shuffles: p⁺ = (1 + #nulls ≥ K4)/20, rank flag only; a flag goes to a pooled reference, I-182/I-203). Strongest low-power fits
(E_config ≤ 1e−6) decoded descriptively.

## Not covered (stated in advance)
One wrong crib letter (next audit); double columnar beyond the themed × themed pairs (3.4 M pairs); themed alphabets behind non-themed
columnar orders; disrupted/Myszkowski columnars; m or n = 1 or > 26; three passes.
