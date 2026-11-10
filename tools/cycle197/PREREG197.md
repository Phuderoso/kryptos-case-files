# PREREG197 — compound key with one dropped or extra carved letter (IDEAS I-196 / I-215)

Written 2026-11-09 ~23:59 PT, before any K4 or shuffled-K4 run with these tools. Only the reserved shuffle (seed 19790), uniform random
texts (seeds 19701–19750) and planted texts were run so far.

## Hypothesis
`[speculation]` K4 = a two-layer key in K1/K2 style (two periodic keys on one tableau, case 176; or on two tableaux A–Z/KRYPTOS in either
order, case 178), optionally behind a K3-law decimation, with **one dropped or one extra carved letter** (K2 lost an S on the copper), so
every position after the slip is shifted. Cases 23, 24, 161, 163 had indels with one periodic key; cases 176–183 had two keys but no indel.

## Model (`cmp197.c`)
- `del`: true ciphertext C′ of 98 letters, C′[d] left off (d 0–97). `ins`: C′ of 96 letters, an extra letter carved at carved index d (0–96).
- A **record** per (transposition, d): 24 cribs → key index (plaintext index, model P; C′ index, model C) and carved index (or lost).
  d values giving an identical record are run once (they are the same test on the cribs); decodes try every d of the run.
- **Direct** (no transposition): two crib readings, R1 = official plaintext positions of the 98/96-letter plaintext, R2 = official carved
  positions; `recs197.py`, 101 distinct records (deduplicated over reading/kind/d; includes the indel-free record).
- **Behind decimations:** case 161's families (`decgen173.py`): dec98 170,258 perms (del), dec96 168,858 (ins); crib plaintext positions 21–33, 63–73.
- **Solver A** (one tableau, additive, `cmp189` union-find): vig/beau, pairs 2 ≤ m < n ≤ 26, n mod m ≠ 0.
  Direct: 18,824 alphabets (case 176 C2 list, first two A–Z, KRYPTOS). Decimations: A–Z and KRYPTOS.
- **Solver B** (two tableaux, `cmp191` bijection graph): AZ>KA and KA>AZ, forms VV/VB/BV/BB, ordered pairs m ≠ n, 2–26.
  Direct: all 600 pairs. Decimations: only the M = N subsets (pure decimations of the true length: decM98 4,116 perms, decM96 3,072), because
  B on the whole families is ≈ 700 s (probe), over budget → left open (new idea).
- Pairs behind decimations fixed **text-free** by a structure pass (`select197.py`; E is structure-only) on every 32nd perm (A) / 8th of
  the M = N subsets (B), scaled: pairs with estimated cell E ≤ 0.10 run (A del P 63 / C 50, ins P 70 / C 54; B del P 138 / C 126, ins P 166 / C 144).
- Chance (I-193): A E_config = 26^−excess; B E_config = Π_cyclic 26^(1−r) (exact expected solutions). Cell = (stage, kind, model, alphabet
  class or tableau pair, form, m, n). Print threshold E_config ≤ 0.002 (controls too, I-214). Any fit in a full-power cell with E_config > 0.002
  (A excess 1) is re-run at 0.05 and decoded.

## Classification (registered)
- **Full power**: exact cell E (printed by the run) ≤ 0.05. A cell set is `EXACT-EXCL` (under the stated model) if every fit in its full-power
  cells is decoded under every equivalent d and every consistent key, and none reads as English (both cribs are forced; English = a run
  of ≥ 3 real words off the cribs, judged by reading plus quadgram score against the plants and nulls). The fit total is compared with the
  summed E (bound).
- Cells with E > 0.05 are `LOW-POWER`: the fit counts are reported against E; the 20 strongest fits (smallest E_config) are decoded and
  read; anything English would be flagged, not counted.
- A real solution requires a full 97-letter coherent English decryption with both cribs at official positions, reproducible.

## Controls (rehearsed: 11/11, `controls197_rehearsal.txt`)
P1 direct R1 del d 50, KA vig ABSCISSA+PALIMPSEST; P2 direct R2 ins d 30 (extra letter inside a crib), AZ beau BERLIN+KRYPTOS; P3 direct R1
ins d 5, AZ>KA VV CLOCK+NORTHEAST; P4 direct R2 del d 70, KA>AZ BV ABSCISSA+PALIMPSEST; P9 indel-free plant (found at the trailing-drop
record); P5 dec98 del d 40 model P KA vig ABSCISSA+PALIMPSEST; P6 dec96 ins d 80 model C AZ vig CLOCK+BERLIN; P7 decM98 del d 60 model C
AZ>KA VB TIME+KRYPTOS; P8 decM96 ins d 10 model P KA>AZ VV SHADOW+LIGHT; N1, N2 three-key negatives (CLOCK+KRYPTOS+BERLINCLOCK) must not fit
at the planted record. Checked independently (`checkctl197.py`, `lib197.py`): planted record rebuilt in Python, decode reproduces the
plaintext at every determined position. Rehearsal fixes (checker only, disclosed): decode under every d of an equivalent run; a stale
loop variable for the direct map; the indel-free plant's 98-letter frame.

## Meter (done, `data/cycle197/meter197.txt`)
40 uniform texts on the direct records, 10 on the sample banks; full-power bands: direct A 68 vs E 32.0 (44 from one text, one coincidence
repeated over overlapping records and nested pairs 2×25 ⊂ 10×25; without it z −1.29), direct B solutions 36 vs 46.4, banks A 1 vs 1.03,
B 25 vs 17.6 (z +1.78). Low-power bands are heavy-tailed (products of component counts, overlapping records), so Poisson z is not a test there.

## Nulls and grid
19 shuffled-K4 texts (seeds 19751–19769) on the direct records (A–Z/KRYPTOS + both tableau pairs, all pairs) and on the sample banks
(dec98/96 every 32nd, A; decM every 8th, B). Grid statistic (I-217, cluster-aware): number of distinct clusters (stage, kind, record
cluster = perm or direct, model, alphabet/tableau, form) with a fit at E_config ≤ 26^−3; K4's rank among 20 texts; floor 1/20 = 0.05
(I-216), so the grid is descriptive: rank 1/20 → flag for a pooled follow-up in a later cycle, not a signal.

## Recount
Independent Python recount (`recount197.py`, BFS propagation, not union-find) of every direct cell for K4 (A on A–Z/KRYPTOS, B both pairs)
and of the decimation cells on dec98/dec96 sample perms: fit counts must be identical.

## Budget
Heavy ≈ 8 min wall; every run under `timeout`, own process group. Blind spots fixed in advance: B behind non-M = N decimations; themed
alphabets behind decimations; both an indel and a changed letter; two indels; three keys; m or n > 26; transpositions other than K3-law decimations.
