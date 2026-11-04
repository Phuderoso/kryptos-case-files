# 24 — Two carving anomalies, direct periodic keys (cycle 25)

**Question.** Cycle 24 tested one bad letter. kryptosbot lists *two-character differences* as untested. If the copper carries two slips (a missing letter, an extra letter, a changed letter under a crib, in any combination), could a plain KRYPTOS-tableau periodic key still decrypt K4 directly?

**Why it's exhaustive, not sampled.** The 24 crib letters sit in two blocks (positions 22–34 and 64–74). A missing or extra letter only matters through *which crib letters shift and by how much*, and a changed letter only matters if it sits under a crib. So every placement of two anomalies collapses to one of **4,913 distinct constraint patterns** (both crib conventions: cribs at the official carved positions, or at the official true-text positions). Testing those 4,913 patterns covers every pair of anomalies anywhere in the text.

**Test.** [`tools/two_anomaly_direct.py`](../tools/two_anomaly_direct.py). Plaintext and cipher alphabets each AZ or KA (KRYPTOSABCDEFGHIJLMNQUVWXZ); Vigenère-type (also covers variant Beaufort) and Beaufort; periods 1–26. Exact crib consistency; every consistent configuration is decoded and scored by English quadgrams.

**Controls.** Three planted texts (period 7 or 8, KA/AZ mixes, one dropped letter plus one junk letter). In each, the planted pattern (or its exact equivalent) is consistent at the true period. Reports: [`analysis/two_anomaly_direct_report.txt`](../analysis/two_anomaly_direct_report.txt).

**Result on K4.** **Zero** consistent configurations at every period 1–24. Only periods 25 (8 configs) and 26 (9,312) survive, which is where the 24 cribs stop constraining anything. Twenty shuffled-K4 nulls give the same picture (P ≤ 24: 0 in all 20; P = 25: 2–968). K4's best English score among survivors (−6.377) ranks 6th of 21 against the nulls (range −6.523 to −6.052), i.e. noise. Nulls: [`analysis/two_anomaly_direct_nulls.txt`](../analysis/two_anomaly_direct_nulls.txt).

**Verdict.** Two carving slips do not rescue a direct KA/AZ periodic key with period ≤ 24. This extends cycle 24's single-anomaly negative. It says nothing about two anomalies *behind a transposition* or with arbitrary alphabets (open).

**Limits.** Swaps were not combined (a swap is itself a two-letter change and was covered alone in cycle 24). Changed letters outside the cribs don't affect consistency and were ignored.
