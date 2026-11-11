# PREREG200 — serial-dependence ("rhythm") fingerprint of K4: a calibrated lag panel, plus a two-sided test of the SAT-open periods

Written 2026-11-11 ~15:49 PT, before any statistic of K4's letter **order** was computed. Run so far: two timing/power probes that use
only K4's letter **multiset** (shuffles) and English plants (seed base 90000, `meter200_probe.txt`); a K2 reference check (seeds 91/92:
PHI8 z 5.5, p 0.0005); and `recount200.py`, which compared the two implementations on K4 and printed only the mismatch count (0).

## Why (new family, I-236 → I-233b)
The case files test K4 almost only through the 24 crib letters. No case file asks whether K4's ciphertext *order* carries a serial
structure of its own (coincidences at a lag, repeated key steps, one-alphabet runs). The Voynich agent's C103 journal proposed a rhythm
test of K4 vs K1–K3 under a permutation null (I-233b, attributed, unverified). This cycle frames it as a discriminating test with power.
Its one place of real value: **periodic substitution with arbitrary (non-tableau) alphabets**, where the SAT runs of cycle 11b left
**P = 8, 13, 16, 19, 20, 23, 24, 26 open**. A coincidence count at the period is alphabet-agnostic, so it reaches those cells statistically.
`[speculation]` that K4 is any of these; K1/K2 (periodic, KRYPTOS tableau) are the style anchor `[sourced, case 02]`.

## Design disclosed from the probes (not a result about K4)
- A first 159-statistic panel (single lags 1–48 for A/BAZ/BKA + windows) had **power at chance** for every family (look-elsewhere
  swamps 97 letters). It was replaced, before registration, by the 64-statistic panel below.
- The low-direction meter check (I-230) cannot use the panel minimum: single-lag counts have means ≈ 3, so z ≥ −2 by construction.
  The low plant is therefore judged on SA16 alone.

## Statistics (`lib200.py`; lags on the contiguous carved text, so nominal lag = true pair distance — Voynich C104 lesson)
A(d) = #{i : c_i = c_{i+d}}. **PHI(p) = Σ_k A(kp), kp ≤ 48, p 4–26** (23); **BAZ(p), BKA(p), p 4–16** = Σ_v C(m_v,2) over the lag-p
difference sequence (c_{i+p} − c_i) mod 26 in A–Z / KRYPTOS numbering (26; progressive keys); **SA(L) = A(1)+…+A(L), L 2–16** (15;
"one alphabet per column" after a periodic-then-columnar layering, case 97 shape). 64 statistics, all one-sided upward.
z = (stat − mean) / sd under the **permutation null** (K4's own letters shuffled; within-segment = whole text): calibration set
10,000 (seed 20001); held-out set 10,000 (seed 20002) for the max / min distributions (I-233a: critical values never from the set that
standardises).

## Tests and classification (registered)
1. **Global:** K4's Zmax over the 64; p from the held-out Zmax distribution. p < 0.01 → `SIGNAL candidate` (follow-up next cycle, no
   claim); otherwise no signal. Each family's **power** = share of 150 plants (own-text null, 300 shuffles, seeds 20000+100+f and
   30000+f·1000+k) with Zmax ≥ the K4 α 0.05 critical value. Family label: power ≥ 0.80 → `NO-SIGNAL (high power)`, 0.50–0.80 →
   `NO-SIGNAL (moderate power)`, < 0.50 → `LOW-POWER`. Families (`plant200.py`, English windows from Jane Eyre with both cribs written
   in at 22–34 / 64–74): P1 KRYPTOS-tableau Vigenère p 4–12; P2 Beaufort A–Z p 4–12; P3 progressive keyword (p 5–10, any step, A–Z/KA);
   P4 Vig p7 then columnar w14; P4b Vig p7 then w7; P5 columnar w 7–14 then Vig p 4–12; P6 Vig p 4–12 then columnar w 5–14; P7 PT autokey
   L 1–10; P8 English running key; P11 arbitrary alphabets p ∈ {8,13,16}; gates P9 uniform letters, P10 shuffled English.
2. **Targeted, two-sided, per open period P ∈ {8, 13, 16, 19, 20, 23, 24, 26}** (H_P = P arbitrary alphabets, direct, no
   transposition): z_K4 = z(PHI_P). (a) signal: p_sig from 10,000 shuffles (seed 20009), Bonferroni 0.05/8; (b) reverse:
   q_rev = share of 300 H_P plants (seeds 20300+P, 50000+P·1000+k) with z ≤ z_K4. **q_rev < 0.05 → `STAT-DISFAVOURED` (α 0.05, a
   statistical — not exact — exclusion under the stated model)**; neither → `LOW-POWER` (inconclusive) for that cell.
   Probe powers (single stat, α 0.05): P8 0.63, P13 0.58, P16 0.62, P19 0.39, P20 0.31, P23 0.43, P24 0.37, P26 0.37.
3. Descriptive: the same panel on K1, K2, K3 (own nulls 3,000 + 3,000, seeds 20006/20007).

## Gates (all must pass, else the run is reported as broken, no verdict)
G1 false calls at α 0.05: P9 and P10 ≤ 0.10 each (150 plants). G2 broken meter both ways (I-230): a high plant (K4's multiset greedily
rearranged to maximise Zmax, seed 20003) above the α 0.01 Zmax critical value; a low plant (rearranged to minimise SA16, seed 20004) below
the SA16 1 % null quantile (seed 20008). G3 known positive: K2's Zmax p < 0.01 with PHI8 or PHI16 among its top 3. G4 `recount200.py`
0 mismatches. Held-out false-call check on K4's winning statistic (fresh 10,000 shuffles, seed 20005) is reported beside the verdict.

## Crib letters and readability
The test does not decrypt, so there is no plaintext to read; the 24 crib letters enter the plants (written into every English window).
A `SIGNAL candidate` would be followed up next cycle by a crib-constrained solve at the flagged period/lag, never claimed here.

## Run
`run_cycle200.sh`: own process group (`setsid`), hard timeout 480 s, then kill only that group. Expected ≈ 3–4 min.

## Blind spots (registered)
Transposition before the substitution hides PHI (only SA catches the w = multiple-of-p shape); a period-P key with fewer than ~2 laps in
48 (P ≥ 25) has one or two lags only; plaintext unlike Jane Eyre English (K4's own style, X separators) changes power; the permutation
null treats K4 as one segment (a drift of letter frequencies between halves is not modelled); H_P plants are not conditioned on being
crib-consistent with K4's actual letters.
