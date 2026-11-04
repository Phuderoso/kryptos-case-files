# 41 — The Stehle lag-4 run: preregistered significance and mechanism test (cycle 42)

**The observation (not a hypothesis).** In the A–Z numbering, K4's carved letters 55–63 (0-based; `DIAWINFBN`)
satisfy c[i+4] − c[i] = 5 (mod 26) for i = 55, 56, 57, 58, 59: D→I, I→N, A→F, W→B, I→N. Five equal lag-4
differences in a row. kryptosbot lists it as a weak live anomaly with no mechanism (quoted there as ≈ 1 in 205);
this repo carried it as an open lead since cycle 24. The run ends on carved position 63, the first letter of
BERLINCLOCK (plaintext B).

**Preregistration** (written before any number below was computed, cycle 42):
- T1. How surprising is the run once we account for having looked? Narrow statistic: longest run of equal
  consecutive lag-4 differences, A–Z numbering. Wide statistic: the same maximised over lags 1–24 and both the A–Z and
  KRYPTOS numberings (48 looks). Both against 200,000 shuffles of K4's own letters. Calibrate on K1, K2, K3, whose
  mechanisms are known and contain no such device.
- T2. Mechanisms that would *produce* the run. Any additive key (Vigenère/Beaufort/variant) whose lag-4 key
  difference is constant over 55–63 passes the run straight to the plaintext: period 1, 2 or 4 keys (difference 0),
  a progressive period-4 key (difference s), an arithmetic key (difference 4·b). Then the plaintext itself must
  carry five equal lag-4 differences. Measure how often 97-letter windows of English do that.
- T3. If the run is a property of the key, the key recovered at the 24 crib letters should show runs of equal lag-d
  differences (d 1–12) more than chance. K4 vs 20,000 shuffled-K4 nulls, Vigenère/Beaufort × A–Z/KRYPTOS.
- Decision rule: call the run a *mechanism lead* only if (a) the wide p < 0.001 and K1–K3 do not reach it, and (b) at
  least one mechanism survives the earlier crib exclusions.

## Results ([analysis/cycle42_stehle.txt](../analysis/cycle42_stehle.txt), tool [tools/stehle_mechanism.py](../tools/stehle_mechanism.py))

| Text | narrow (lag 4, A–Z) | p | wide (48 looks) | p |
|---|---|---|---|---|
| **K4** | 5 | 0.0002 | 5 | **0.008** |
| K1 (period-8 KA Vigenère) | 1 | 1.0 | 5 | 0.005 |
| K2 (period-10 KA Vigenère) | 3 | 0.41 | 5 | 0.033 |
| K3 (transposition) | 2 | 1.0 | 4 | 0.60 |

- **T1.** The narrow p ≈ 1/5,000 is the figure you get when you pretend lag 4 and A–Z were chosen in advance. Once
  the 48 looks are counted, p ≈ 0.008 (≈ 1 in 130) — and **K1 scores a run just as long and just as "significant"
  (p ≈ 0.005)** with a mechanism that has nothing to do with lag 4. The run fails decision rule (a).
- **T2.** In 2.87 M letters of English (five Gutenberg novels), 0.17 % of 97-letter windows contain a lag-4 run ≥ 5
  (shuffled English 0.03 %); 80 % of those runs have difference 0 (a repeated 4-letter block such as a doubled
  word), only 2 % have difference 5. So the English-friendly way to make the run is: plaintext repeats a 4-letter
  block across 55–63 and the key steps +5 per lap of 4. That plaintext would read `B???B???B` + ERLINCLOCK, with the
  B's forced by the crib — not English. Every key that makes the run without such plaintext (period 1/2/4,
  progressive period 4, arithmetic key) is already excluded at the cribs: periodic keys directly and behind 165,065
  transpositions (cycles 13, 24, 41), progressive period-4 keys (cycle 41, L = 4), arithmetic/affine progressions
  (cycles 39–40). The transpose-then-substitute versions are excluded in the same cycles. **No surviving mechanism**:
  rule (b) fails.
- **T3.** The key at the cribs shows no regularity: longest run 2 in all four tableaux, at the bottom of the null
  range (p ≈ 0.99). Whatever made the carved run left no trace in the 24 known key letters.
- Side note: the run exists only in the A–Z numbering (KRYPTOS numbering: 5,4,5,11,4). K1–K2 work on the KRYPTOS
  alphabet, so a deliberate device would more naturally show there.

## Verdict
**Negative / downgraded.** The Stehle run is about a 1-in-130 event after correcting for where we looked, of the same
size as a run K1 shows by accident, and every simple mechanism that would produce it is already excluded by crib
tests. It should not steer future work. What stays open: a mechanism that acts *only* on a short stretch (a local
key change at 55–63) cannot be tested from the cribs, which do not overlap that stretch except at position 63.
