# Cycle 173 pre-registration (IDEAS I-105 + I-107 + I-104) — written before any K4 or null run of the anomaly models

Committed with the tools, before the K4/null runs. (Only the case-57 baseline `none` was run on K4 before this, as a known-answer check.)

**Family.** K3-law decimations perm[j] = (a + s·j) mod M, gcd(s, M) = 1, all starts, empty slots skipped, both directions,
rebuilt for a true ciphertext of n letters (`decgen173.py`): n = 98 (M 98–113, 170,258 perms), n = 96 (M 96–112, 168,858 perms);
n = 97: the 165,782-entry `all.bin` of cases 156–160 (159,712 decimations + 6,070 spiral/diagonal routes).

**Models** (case 23 / cycle 24 conventions, `anom173.c`): del (n 98, d 0–97), ins (n 96, d 0–96), chg (n 97, one of 24 cribs dropped),
swp (n 97, d 0–95). Tableaux (PA, CA) ∈ {A–Z, KRYPTOS}², Vigenère (= variant) and Beaufort, key at plaintext or true-ciphertext index, p 1–26, exact.

**Texts.** K4 on the full family. 19 shuffled-K4 nulls (seeds 173000–173018, `random.Random(seed).shuffle`) and K4 on every 4th perm of each family.

**Grid (I-107), fixed:** 4 models × p 1–26 = 104 cells; cell statistic = number of consistent configurations (summed over d, tableaux, modes, frames).
Per text X and cell c: upper-tail p_c(X) = #{texts Y among the 20 with count_Y(c) ≥ count_X(c)} / 20. Grid statistic T(X) = min over the 104 cells.
K4's grid rank = #{texts Y with T(Y) ≤ T(K4)} / 20 (floor 1/20 = 0.05, I-094). Only this rank is quoted for "any cell looks high"; no single-cell p.

**Labels.** Cells where the full-family K4 count is 0 and the summed analytic chance expectation is < 1 → `EXACT-EXCL` for that model × p.
Cells with chance expectation ≥ 1 → `LOW-POWER`; their decodes (p ≤ 21) are English-scored against the plants; K4 best vs the nulls' best
on the subset → `NO-SIGNAL` if inside. A real solution needs readable English off the cribs, not a count.

**Add-on I-104:** for the 685 cycle-172 Quagmire IV survivors (p 15–16), test whether the crib-fixed key letters fit a vocabulary word
(word of length p, cyclic shift allowed, '?' wildcards, ≥ 10 fixed letters) for K4, and the same for the 8 cycle-172 nulls' survivors as the reference.
