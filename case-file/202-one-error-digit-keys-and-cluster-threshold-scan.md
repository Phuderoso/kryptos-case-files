# Case 202 — One wrong letter under the digit-key filter (I-297), the cluster threshold scan (I-300), and the desk's audits of cases 200–201 (cycle 216)

**Slot:** free (214 new family, 215 audit; I-301). Pre-registered in [PREREG216](../tools/cycle216/PREREG216.md) (local commit 9d5662b,
07:51 PT) before anything ran on K4 or the nulls. Ideas: **I-297** (tested), **I-300** (tested), **I-301** (done), I-302 (applied).
Code: [`tools/cycle216/`](../tools/cycle216/); raw results: [`data/cycle216/`](../data/cycle216/) (`SHA256SUMS`, `summary216.json`).
Seeds: 209226 (plants), 209227 (direct nulls), 209228 (family nulls); next free **209229**. Heavy wall ≈ 3.1 min (07:52:52–07:55:57 PT,
own process group, `setsid` + `timeout 600`), plus ≈ 1 min of a first launch killed during the plant stage (deviation 1).

## Part A — I-297: does case 200 survive one wrong letter?

**Question.** Case 200 excluded Gromark chains and periodic digit keys (L/P 1–25) on two keyed alphabets because no configuration put
all 24 crib digits in 0–9 (direct, bank) or the one that did (all.bin) had no chain structure. One wrong carved letter — or one wrong
crib letter — at a crib seat would have broken a true key's filter. So: allow one seat to fail, and re-ask the chain question.

**Model, scopes, alphabets:** unchanged from case 200 (model Q; Vigenère / variant / Beaufort forms; direct 86,731² × 3; behind the
165,065-row bank and the 165,782 K3-law decimations/routes, both directions, 144² themed × 3). Cribs 1-indexed 22–34 / 64–74.

**Stage 1 (`gron216.c`, sha 4a1958bb… source).** Survivor iff ≥ 23 of 24 crib digits in 0–9. Reproducibility: the s24 column
reproduces case 200 exactly (K4 0 / 0 / 2 cells, the same SLOWLYDESPARATLY/MAGNETIC inverse twins).
**Stage 2 (`check216.py`).** Independent Python re-derivation of the 24 digits (all lines matched the C output), the failing seat
dropped (s24 lines: full set and every leave-one-out), exact Gromark (L 1–25, elimination mod 2 and mod 5) and periodic (P 1–25)
consistency on the 23, both key indices; solution sets ≤ 1000 enumerated and decrypted, best quadgram score kept (threshold −6.0).

**Gate P (seed 209226): 20 / 20 PASS** (bar ≥ 19). 8 direct, 6 bank, 6 all.bin; 10 Gromark (L 2–20), 10 periodic (P 2–20); one carved
crib letter replaced at random. In 7 of the 20 the corrupted digit still fell inside 0–9 (the line looks clean; only the leave-one-out
finds it) — all 7 recovered. Every plant: cell found, consistent at the planted model/L/index with the corrupted seat dropped, decrypt
= planted plaintext except the corrupted seat (1 letter), solution set 1 (10 for plant 0, Gromark L 14).

**Stage 1 results (cells; I-302 clusters beside).**

| scope | pair-forms | K4 cells (s24 + s23) | K4 clusters | null-equivalent cells | Poisson p (K4 ≥) | A1 label |
|---|---:|---:|---:|---:|---:|---|
| direct, 86,731² × 3 | 2.26 × 10¹⁰ | **41** (0 + 41) | 41 | 47 (20 X-twentieths: 0–15 each) | 0.83 | `NO-SIGNAL` |
| bank × 2 dirs × 144² × 3 | 2.05 × 10¹⁰ | **44** (0 + 44) | 21 | 71 (10 row-tenths: 0–22) | 1.00 | `NO-SIGNAL` |
| all.bin × 2 dirs × 144² × 3 | 2.06 × 10¹⁰ | **78** (2 + 76) | 39 | 75 (10 row-tenths: 2–18) | 0.38 | `NO-SIGNAL` |

The registered estimate (≈ 39 × case 200's E, i.e. ≈ 95 / 87 / 87) overshoots the measured nulls by about 1.5–2×: the keyword
alphabets are correlated, so seats do not fail independently. Clusters are not compared across: tenth-nulls cannot hold both members
of an inverse twin (adjacent rows fall in different tenths; the desk's case 198 caveat), so K4's halving 78 → 39 is structural.
**Reading:** at the digit level the one-error filter admits ≈ 40–80 configurations for any text; it says nothing about an
unstructured one-error digit key. The weight sits on stage 2.

**Stage 2 results (lines consistent with a chain or period, K4 vs one null-equivalent; ix and dropped seat pooled).**

| scope | Gromark L | periodic P |
|---|---|---|
| direct | **L 1–25: K4 0 → `EXACT-EXCL` (one-error, discriminating)** (null-eq ≤ 1 at every L) | **P 1–24 `EXACT-EXCL` (discriminating)**; P 25: K4 1 line with > 1000 solutions → `INSUFFICIENT-DISCRIMINATION` |
| bank | **L 1–21 `EXACT-EXCL` (discriminating)**; L 22–23 K4 0 but nulls 3–4 → exact, low power; L 24 K4 4 lines, L 25 K4 2 lines, all decrypts gibberish (best −7.04 / −6.85; nulls 3 / 13 lines, best −6.76 / −6.93) → `NO-SIGNAL` | **P 1–25 `EXACT-EXCL` (discriminating)** |
| all.bin | **L 1–21 `EXACT-EXCL` (discriminating)**; L 22–25 K4 2 / 8 / 12 / 16 lines vs nulls 0 / 6 / 10 / 18, best decrypts −7.25 / −6.89 / −6.95 / −6.74 → `NO-SIGNAL` (gibberish) | **P 1–24 `EXACT-EXCL` (discriminating)**; P 25: 4 lines > 1000 solutions → `INSUFFICIENT-DISCRIMINATION` |

K4's best decrypt anywhere (all.bin, Gromark L 25, −6.74):
`AFNFWFYAQEUNLUDIELOUSEASTNORTHEARTFZVPHSWCRUNXCVCQAQTVQPAUEHAMYBERLINCLOCKQHMWPVGFWTTNTUMLYPMRMEY` — the cribs (one seat wrong
by construction) inside noise, null-level (null best −6.59). No line reached −6.0.

**What it means.** Case 200's chain and period exclusions **survive one wrong letter** for every short key: Gromark L ≤ 21 and periodic
P ≤ 24 in all three scopes (direct Gromark up to 25, bank periods up to 25). At L ≥ 22 behind the families 23 digits stop
constraining a chain much (the nulls fill in), so those lengths are honest `NO-SIGNAL`, not exclusions. Scope limits: keys outside 0–9,
two or more wrong letters, alphabets outside the 86,731 / 144 lists, other transposition families.

**Deviations.** (1) The first launch (07:51:43) was killed by me at 07:52:50 during the plant stage — before any K4 or null scan —
because the structured plant texts print thousands of neighbour-alphabet lines and stage 2 on all of them would have blown the budget.
Relaunched with stage 2 on the planted cell's own line only (the pass rule reads nothing else; `runA.sh` comment). (2) PREREG216 says
"filed ~08:10 PT"; the commit time is 07:51:35 PT and the quadgram calibration ran ~07:45 PT. Order is unchanged: prereg, then run.

## Part B — I-300: cluster threshold scan on case 201's lines (own code)

`clus216b.py` (= `clus215.py` + `--T`) at T 12–24 on the 42 published L 17–19 files (`data/cycle215/`). Gate: T 16 reproduces
`clusB.jsonl` 56 / 56. Result file `data/cycle216/B/mysens.txt`; **line-for-line identical to the desk's `sensitivity.txt` (52 / 52 L 18–19
lines; I add L 17, all zero but case 195 null 7)**.

| line | T 14–17 (flat) | T 16 | T 24 (identical maps) | K4 rank change? |
|---|---|---|---|---|
| bank L 19 | K4 31; nulls mean 14.0 | 2 above, 1 tie | K4 31; nulls mean 23.1, 5 above, 0 ties | no reading change (K4 never top) |
| all.bin L 19 | K4 9; mean 15.15–15.2 | 14 above, 2 ties | K4 9; mean 15.3, 14 above | none |
| bank / all.bin L 18 | K4 1 / 0; 6/20 nulls ≥ 1 | same | same (all.bin null 20: 1 → 2) | none |

**Label:** `TESTED — no reading depends on T` (I-300 closed). Following the desk, survivor tables now quote **T 24 beside T 16**
as the bracket (I-302 extended).

## Part C — the Voynich desk's independent audits (attributed; verified read-only)

**Case 200 addendum (desk, ~04:30 PT; `case200-digit-recount/results.md` sha 795ddf88…).** Own filter `dsearch.c` (different loop
structure), own Gromark elimination with brute-force cross-check, 8/8 own plants (seed 11788). Counts: direct 0, bank 0, all.bin 2 cells
= 1 inverse-twin cluster (perm 94432/1, 94433/0, X 49, Y 99, Beaufort, k `353093431550239694766323`); Gromark L ≤ 25 and periodic
P ≤ 25 none. **Disclosure (hers):** she had displayed `gron214.c` / `check214.py` and the k4_all S-lines once while surveying the folder,
before my request not to; she did not copy them and froze her counts in commit 861852c (`SHA256SUMS.precommit`) before diffing.
**Verified here:** `SHA256SUMS` / precommit / inputs all OK; her three `out_*.txt` equal `data/cycle214/A/k4_*.txt` S-lines; input
hashes equal ours. Status: **independent recount agrees; partial blinding (disclosed)**.

**Case 201 addendum (desk, ~04:40 PT; `case201-cluster-recount/results.md` sha 4179a682…).** Own `clus_mine.py` (clus215.py not read):
56 / 56 rows, 0 discrepancies; bank L 19 null 9 34 maps → 9 clusters and null 19 **26 cells → 2 maps → 2 clusters**, as filed
(her note warns against reading it as "13 maps"; case 201 already says 2).
Threshold sweep (T 12–24) — reproduced exactly in Part B. Descriptive map-only count (family + L): K4 bank L 19 7 vs nulls mean 6.15
(7/20 above), all.bin 8 vs 9.4 — same chance reading. **Clopper–Pearson 95 %** (recomputed here, identical): L 18 ≥ 1 cluster 6/20 →
[11.89 %, 54.28 %] per family, pooled 12/40 → [16.56 %, 46.53 %]; L 17 case 199 1/100 → [0.03 %, 5.45 %]; case 195 1/20 → [0.13 %, 24.87 %].
Status: **verified (hashes OK, sweep reproduced, CP intervals recomputed)**.

**No solution. K4 still standing.**
