# 110 — Kryha with one wrong crib letter (cycle 122)

**Question.** Cycles 114–115 ruled out the Kryha cipher machine on K1–K3-style keyword alphabets for any V1 wheel (n ≤ 48, teeth 1–9) and any V2 hole setting, directly and (for keyword pairs) behind the 165,065-permutation bank. Those tests trust all 24 crib letters. If exactly one crib letter is wrong — a carving slip under a crib, or a wrong assumed plaintext letter — do the exclusions still hold?

**Code.** [`tools/cycle122/`](../tools/cycle122/): `b1_loo122.c` (V1 any-wheel soft), `v2_loo122.c` (V2 any-holes soft), `run122.py` (driver + planted controls + Test A). Soft adjacent-step logic for B1 ignores merged two-step constraints across a dropped middle letter (cycle-119 lower-bound spirit). Outputs in [`data/cycle122/`](../data/cycle122/); large raw pair dumps live under `/home/box/kryptos_support_backup/cycle122/` (not committed).

**Metrics.** For each of the 2,356 keyword alphabet pairs × 2 senses:
- **strict** — consistent with all 24 cribs (cycle 114's test)
- **soft_only** — fails strict, but consistent after dropping exactly one crib

Cribs: EASTNORTHEAST at 21–33 and BERLINCLOCK at 63–73 (0-based), same as cycle 114.

**Controls.** Clean planted Kryha V1 (`ctl1_clean`) and V2 (`ctl2_clean`) recover with strict > 0 at their true (pair, sense). The same plants with one crib ciphertext letter flipped (`ctl1_flip` drop 5, `ctl2_flip` drop 7): strict = 0, soft_only recovers (B1 at the true drop and period; B2 at the true drop). So the leave-one-out score finds a real one-error Kryha when one is there, and does not invent soft survivors for a clean plant. Five shuffled-ciphertext nulls run at the same scope.

## Results

| Test | Text | strict (pairs) | soft_only (pairs) |
|---|---|---|---|
| B1 any V1 wheel n 1–48 | K4 | **0** | **0** |
| B1 | null 0..4 | 0,0,0,0,0 | 0,0,0,0,0 |
| B1 | ctl1_clean / ctl1_flip | 2 / 0 (true pair) | — / recovers |
| B2 V2 any holes | K4 | **0** | **0** |
| B2 | null 0..4 | 0,0,0,0,0 | 0,0,0,0,0 |
| B2 | ctl2_clean / ctl2_flip | recovers / strict 0 soft recovers | — |
| A published wheels, free alphabets | K4 | 0 / 184 | **2** |
| A | null 0..4 | 0,44,0,2,0 | 14,84,0,114,68 |

Test A was already a weak exclusion in cycle 114 (45 % of shuffles also give strict 0). K4's soft_only = 2 sits well below the null soft_only range (0–114); free alphabets remain underdetermined and are not a signal.

Wall time ≈ 2.6 minutes (B2 dominates; B1 and A are sub-second to a second).

## Verdict

- **B1 (any V1 wheel, keyword alphabets): still excluded under one wrong crib letter.** K4 soft_only = 0; nulls 0; controls pass. Does **not** soften cycle 114.
- **B2 (V2 any holes, keyword alphabets): still excluded under one wrong crib letter.** Same pattern. Does **not** soften cycle 114.
- **A (published wheels, free alphabets): no new signal.** soft_only = 2 for K4 is noise against the nulls; cycle 114's weak reading stands.

Contrast with cycle 119 (stepping-disk |S| ≤ 5 behind the bank *did* soften) and agreement with cycle 120 (Quagmire soft_only = 0).

**Negative for the powered Kryha exclusions (B1, B2). Does not soften cycles 114–115.**
