# PREREG226 — Cycle 226 (audit slot, I-326): a decrypt bar calibrated by period and known letters

Filed 2026-11-20 15:50 PT, before any K4, plant or null run of this cycle. Base: origin/main a8d2789 (c225 published).
Slot: audit (I-328: 226 must be an audit; I-326 preferred). Case file 212.

## Question
Cases 209 / 210 used one decrypt bar: ≥ 49 known letters and mean log10 quadgram ≥ −6.0 over all known letters. Case 210 found
that ≈ 1,080 gibberish K4 hits (and the nulls at the same rate) pass it at p 21–24: the 24 crib letters lift the mean and the bar does
not depend on how many letters are known. I-326 asks for a bar calibrated per (period, known letters), scoring non-crib letters only,
with plants that must clear it, and a re-read of the case 209 / 210 cells (case 209 = the case 205 p 20 / 21 cells).

## Statistic
**NC** = mean log10 quadgram (`qg.bin`, sha256 4a02ba4e…, unchanged) over quadgrams with no '?' and **no crib position**
(0-based 21–33, 63–73); undefined if fewer than 10 such quadgrams (an undefined NC never passes).
Known-letter bins: kbin 0 = known < 49 (no bar, as before), kbin k = 1 + (known − 49) div 8 (49–56, 57–64, …, 97).

## Bar (frozen rule)
English oracle: 16 English 97-letter texts with the cribs inserted (`mkoracle226.py`, seed **209546**: 8 windows of the K1–K3
plaintext, 8 of the Jane Eyre body, Gutenberg #1260, box copy). For every hit, NC is also computed for 4 of the oracle texts **under
the hit's own '?' mask** (o1 = config hash mod 16, o1 + 4, + 8, + 12). This is what the decrypt would score if the configuration
and key classes were right and the plaintext were English.
- Stratum s = (p, kbin ≥ 1). Oracle sample O_s = oracle scores from **null-text hits only** (K4 does not set its own bar).
- **bar_s = 5th percentile of O_s** (undefined oracle scores count as failures). Stratum is *barred* only if |O_s| ≥ 400 and
  ≤ 5 % of O_s are undefined; otherwise its hits are `INSUFFICIENT-DISCRIMINATION` at the decrypt level.
- Oracle power is 0.95 per barred stratum by construction; the real plants check it.
- Null false-pass rate f_s = share of null hits in s with NC ≥ bar_s (reported).

## Part A — case 210 cells (V / Q, bank and all.bin, every period)
`kb226.c` = `kb224.c` verbatim + NC / oracle / histograms / 'P' lines (NC ≥ −6.0 printed, cap 200,000 per run).
K4 at full scale (direct GVQ, bank GVQ, all.bin GVQ); nulls = the 20 case 210 shuffles (`nulls224.tsv`, seeds 209417–209436,
already published texts) on every 10th row (rowstride 10, offset 0), V / Q, bank and all.bin. `run226.sh` inside
`setsid timeout 600`. No new null seeds.
- **Gate T (counting invariance):** the S, N and T lines of K4 bank / all.bin / direct and of null 209417 r10 equal the published
  `data/cycle224/RS/` files byte for byte; the C lines equal as sorted sets (B lines are thread-order dependent and are not compared).
- **Gate P (seed 209547, bar):** 20 plants (`plant226.py` = `plant224.py` with seed 209547, V 8 / Q 12, p 17–24, direct / bank /
  all.bin, odd ids one wrong carved crib letter, plaintext K1–K3 or Jane Eyre). Run on their true row (`gate226.py`). PASS needs
  ≥ 19/20 planted cells found, and among the found plants whose cell is in a barred stratum, **≥ 90 % with NC ≥ bar_s**.
  Plants in kbin 0 or unbarred strata are reported as such (that is the method's blind spot, not a failure to hide).
- **Labels per (model, scope, p) cell:** K4 passes = K4 hits with NC ≥ bar_s. Comparison on the same scale: K4 hits on rows with
  perm % 10 == 0 vs the 20 nulls (rank p_up = (1 + #nulls ≥ K4) / 21; occupancy = nulls with ≥ 1 pass).
  - K4 passes 0 in all barred strata of the cell → `NO-SIGNAL` at the decrypt level, stated with the share of the cell's K4 hits
    that sit in barred strata (an English solution among them would pass with ≈ 0.95); the unbarred share stays
    `INSUFFICIENT-DISCRIMINATION`.
  - K4 passes > 0 → manual read of the top decrypts; `NO-SIGNAL` unless coherent English (and p_up ≤ 0.05 is still not a lead on
    its own); a coherent 97-letter English text would be reported as a candidate.
  - Count-level labels of case 210 are not changed by this audit; only the decrypt-level reading of the p ≥ 17 cells.
- Old bar check: the C counts (old −6.0 bar) are reprinted next to the new pass counts.

## Part B — case 209 cells (case 205 p 20 / 21, col21)
`reread209_226.py`: the cycle 223 raw outputs (K4 + 168 nulls, `/workspace/k4c223/w/out`, hashes in `data/cycle223`), decrypted
with `analyze223.py`'s `decrypt` (verbatim copy), D2-collapsed, NC + 4 oracle scores per D2 cell. Bars per (p, kbin) from the 168
nulls' oracle samples (same rule). K4 passes vs per-null passes (rank, occupancy). Same labels.
- Gate for part B: K4 D2 counts at p 20 / 21 equal case 209 (2 and 99).

## Budget
Heavy compute ≈ 5 min (K4 full scored ≈ 2 min, 40 null r10 runs ≈ 3 min); part B ≈ 1 min Python. Own process group, timeout 600 s.

## Seeds
209546 oracle windows; 209547 plants. Next free seed after this cycle: **209548**.

## Not in scope
Case 211 p 18 cells (Quagmire, `col1e4.c`) — follow-up if the bar is adopted; case 205 p 18 / 19 / 22 cells; non-periodic keys.
