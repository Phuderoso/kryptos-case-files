# 113 — Digrafid, the 27-symbol digraphic fractionation (cycle 125)

**Why.** The diversity rule asked for a family not yet in the file. Digrafid (ACA; in the Delastelle line next to Bifid and Trifid, which cycles 43 and 117 tested) had never been opened. It is a pencil-and-paper system with two keyword grids, a period and a K3-like "write in rows, read in columns" step on digits, which suits the K1–K3 profile (keywords, a keyed alphabet, a grid transposition).

**Structural facts first.**
- Digrafid works on letter pairs, so its output has even length. **K4 has 97 letters: plain Digrafid cannot produce it.** It survives only with a one-letter anomaly: a carved null, or one cipher letter left off. Both are tested below.
- The grids hold 27 symbols (A–Z + `#`). With random grids, a 97-letter output avoids `#` about 2.6 % of the time ((26/27)⁹⁷); Sanborn could have re-encrypted until it did, so this is weak evidence, not an exclusion.

**What was tested (exact, `tools/cycle125/digrafid.c`).**
- Grid 1 row-filled 3 × 9; grid 2 9 × 3 filled down columns (ACA) or across rows; `#` last.
- Periods p = 1–48 pairs (48 = the whole text as one block).
- Model A: every carved position d (outside the cribs) as a null. Model B: a missing cipher letter before every carved position d = 0–97; blocks with the gap skipped, ≥ 12 crib letters still checked.
- Keys: the same keyword alphabet in both grids (9,401 alphabets), themed × themed (11,130 ordered pairs), themed × 9,295-word vocabulary both ways (1.97 M pairs). About 3.2 × 10¹⁰ crib tests on K4.

**Controls.** An independent Python ACA encryptor planted four messages (both fills, both length models, p 5–12). **4/4 recovered** from the full key lists with their true keywords, fill and period, and no other key pair survived. The null position comes back as a range (dropping any letter inside a crib-free block gives the same crib check), and the true position is always inside it.

**Results.** K4: **0 survivors** in every run (same key, themed pairs, cross pairs). Three shuffled-K4 nulls: 0 (same-key and themed runs). At 12–24 checked letters a chance survivor has probability ≤ 27⁻¹², so zero for both K4 and nulls is expected unless the structure is right.

**Verdict (fact, for this family).** Digrafid with keyword grids from the themed list or the 9.3k vocabulary (same key, themed pair, or themed × vocabulary), either grid-2 fill, any period 1–48, plus one carved null or one missing cipher letter anywhere, does **not** produce K4. Plain Digrafid is excluded by length parity.

**Still open.** Arbitrary (non-keyword) grids: crib-underdetermined, needs SAT; `#` placed elsewhere than last; Digrafid behind a transposition or under a periodic key; two vocabulary words (88 M pairs, feasible over a few cycles).

Data: [`data/cycle125/`](../data/cycle125/). Journal: [cycle 125](../journal/2026-11-08-cycle125.md).
