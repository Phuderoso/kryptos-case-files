# Case file 201 — Cluster-aware recount of cases 193–198 (audit, I-291 / I-298; partial I-294)

**Cycle 215, 2026-11-14.** Pre-registration [`PREREG215`](../tools/cycle215/PREREG215.md) (commit "Cycle 215 pre-registration"). Script
[`clus215.py`](../tools/cycle215/clus215.py); outputs [`data/cycle215/`](../data/cycle215/) (`clusA.jsonl`, `clusB.jsonl`, regenerated
lines `k4_*_L17-19.txt`, `null_lines_L17-19.tgz`, `runB.sh`). Rule: PREREG214 part C, unchanged (credit: Voynich desk) — cells of one text
are one cluster iff same family, tm/form (+ X, Y pair where present), L, segE, segB, o1, o2, and single-linkage on effective crib maps
(S at 0-idx 21–33, 63–73) agreeing on ≥ 16/24; identical maps (inverse twins) merge. Disclosure: the script was smoke-tested on three
published K4 files while it was written (named in PREREG215); the rule was not changed after that.

## Part B gate R (reproducibility, exact)
Unchanged `wrbank` (binary sha 614082dc…, source 1001272d…) re-run at L 17–19 on K4 and the 20 published nulls of case 193 (seed 206206,
bank, 165,065 rows) and of case 195 (seed 208208, K3-law decimations/routes `all.bin`, 165,782 rows). **42 / 42 files reproduce the
published per-(tableau, L) histograms exactly** (`hist_null_i.txt`, `hist_k4_*`). 108 s wall, 6 processes, own process group.

## Results (cells = printed survivor lines; maps = distinct effective crib maps; clusters = rule above)
| Case / scope | L | K4 cells / maps / clusters | nulls: clusters per null (or per null-equivalent) | Reading |
|---|---|---|---|---|
| 193, R1 behind bank | 18 | 2 / 1 / **1** | 20 nulls: 6 / 20 with ≥ 1; mean 0.40 (cells 0.80) | chance level; `NO-DISCRIMINATION` stands, now measured on lines (feeds I-294) |
| 193, R1 behind bank | 19 | 62 / 31 / **31** | mean 14.0, range 2–50; two nulls above K4, one tied (31) | not significant (K4 rank 3–4 of 21); K4's 31 are all inverse-twin pairs, none merge |
| 195, R1 behind decimations | 17 | 0 | 1 / 20 with ≥ 1 (null 7, 1 cluster) | unchanged (case 199 later measured 0 / 100 on fresh nulls) |
| 195, R1 behind decimations | 18 | 0 | 6 / 20 with ≥ 1; mean 0.40 | K4 zero not discriminating (as filed) |
| 195, R1 behind decimations | 19 | 18 / 9 / **9** | mean 15.2, range 6–32 | below the null median; the case's "8 configurations" are 9 here because one key appears under two segmentations (rule keeps segE apart) |
| 197, two-keyword tableaux, bank | 17 | 2 / 1 / **1** | null-equivalents as filed (cell lines not kept) | as filed: one configuration |
| 197, all.bin | 16 / 17 | 2/1/**1** · 4/2/**2** | as filed | as filed (row 83,548 config, NO-SIGNAL) |
| 198, themed tableaux, bank | 16 | 40 / 9 / **9** | 10 tenths = 1 null-equivalent: **39** clusters (tenth 1 alone 19) | K4 below chance |
| 198, all.bin | 15 / 16 | 2/1/**1** · 34/16/**16** | 1 null-equivalent: **25** clusters (L 16); 1 at L 14 | K4 below chance; the L 15 line stays chance (case 198 addendum 1) |

`--pairblind` sensitivity: identical except case 198 null tenths 12 (3 vs 4 clusters) and 19 (2 vs 3); no K4 count changes.
Cases 194 (plant gate) and 196 (Quagmire IV SAT q) have no survivor-cell tables: not applicable.

## What the recount changes
- **Nothing in any exclusion.** Every `EXCLUDED`/`EXACT-EXCL` in 193–198 rests on K4 zeros; zeros are zeros under any counting.
- **Overdispersion shrinks.** At L 19 the variance-to-mean ratio of null counts falls from 103 (cells) to 15 (clusters) behind the bank and
  from 10.4 to 5.3 behind the decimations; at L 18 from 2.7 / 2.4 to 1.35 / 1.10 (near Poisson). Inverse twins alone halve every count;
  single-linkage on ≥ 16/24 shared crib positions merges up to 34 maps → 9 clusters (bank null 9), and crib-equivalent rows with identical maps collapse 26 cells → 2 maps (bank null 19). Cell-based tail claims in the old
  tables were therefore too wide; future rates should be reported in clusters.
- **Case 198's "8 configurations on the bank" = 9 clusters** (the ANTIPODES/INTERPAU 24 cells over 12 rows carry one crib map: the rows
  are crib-equivalent). K4's cluster counts behind 198's families are below one null-equivalent's (9 vs 39; 16 vs 25): `NO-SIGNAL`, as filed.
- **L 18 frontier (I-294, partial):** with lines, both families show 6 / 20 nulls with a cluster and mean 0.40, so L 18 is not discriminating
  in either (a measured rate with 20 nulls: 30 %, Clopper–Pearson 95 % 12–54 %). 100 nulls are still owed only if a sharper scope
  statement is wanted; the label cannot become an exclusion while K4 itself has a cluster behind the bank.

## Blind spots
Case 197's null lines and case 193/195 nulls at L ≤ 16 were not regenerated (zeros there; nothing to cluster). One null-equivalent per family
for case 198 is a single draw (tenths are overdispersed, I-296 note). The ≥ 16/24 threshold is the desk's; no threshold scan was done
(I-300). **No solution.**
