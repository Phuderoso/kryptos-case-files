# Case file 159 — One error: Porta behind decimations/routes, and named running keys behind the bank (cycle 171)

**Status:** negative. **Type:** audit/variant (cycle 170 was a new family). IDEAS **I-096** (Porta one-error) + **I-091**, bank part
(one-error running keys behind the 165,065-perm bank). Both earlier results ([case 158](158-porta-behind-decimations-and-routes.md),
cases [34](34-k3-source-book-as-running-key.md)/[35](35-plain-sight-running-keys-and-hex.md) and cycle 36) were **strict**: one wrong carved
letter or one wrong crib letter at a crib position would have hidden the true configuration. This case closes that gap for both.

**Result in one line:** with one error allowed, K4 has **0** periodic Porta keys at L 1–23 (key by ciphertext position, V1A/V2A) and
L 1–18 (key by plaintext position, V1B/V2B), **0** one-error Porta running-key fits (all 1,539 error-anywhere survivors; forced-error
survivors on a 1/8 slice), and **0** named running-key fits at ≥ 23/24 behind the bank (2.65 × 10¹³ placements) → **`EXACT-EXCL`** in those cells.
Porta V1B/V2B at L 19–23 and every L 24–26 cell are **`LOW-POWER`** (fits at the chance rate, all gibberish).

## 1. Choice (IDEAS reconciliation)
Options handed over: I-091 (one-error running keys behind the bank and rail/AMSCO, ~7 min) and I-096 (one-error Porta, cheap).
I-096 turned out cheap (key-free stage ~1 min for the whole family), so both fit one cycle: I-096 in full except the forced-error
running keys (1/8 slice), and I-091's bank part in full. The rail/Redefence/AMSCO part of I-091 (1.87 M perms, ~11× the bank) stays queued.
Checked before running: no other case file handles one error for Porta (cases 31, 158 strict) or for named running keys behind the bank
(cases 34, 35, cycle 36 strict; case 157 one-error covers decimations/routes only). I-078 check: the run folders `/workspace/k4c169/run`,
`/workspace/k4c170/run` hold finished outputs only (every chunk ends with its terminal line); nothing orphaned.

## 2. Porta one-error model ([`tools/cycle171/porta171.c`](../tools/cycle171/porta171.c))
Same model as case 158: 165,782 decimations/routes (`all.bin`), 173,431 orderings from the 86,731-alphabet bank (halves F first/last 13,
E even/odd), V1/V2, model A (key index j, substitute then transpose) and B (key index perm[j]).
One error = one of the 24 crib pairs (PT[j], CT[perm[j]]) is arbitrary.
- **Key-free stage (exact):** a half-split passes iff **at most one** crib pair fails to cross halves. If exactly one fails, that pair is
  the forced error d. Self-mapped pairs (PT = CT) can never cross: two of them kill the perm (45,083 perms), one forces d.
- **Periodic L 1–26:** d forced → the other 23 key values must be consistent per residue class. d free → consistent after removing at
  most one value (only one residue class may hold one dissenting value). Exact counts.
- **Running keys:** the 36 named texts of case 156, 16 letter→key conventions (f = A–Z index/2 or ordering index/2, s = ±1, c free). At most
  one of the 24 equations fails (d forced: the other 23 hold). c is tried from each of the first two usable equations, so a wrong first
  equation cannot hide a fit.
- **Expectation beside each count (I-097):** for every survivor and (variant, order, L), the chance pass probability: 13^−c (d forced,
  c = checks among 23), or 13^−c + Σᵢ 13^−c(i) (d free, union bound over the removed value). Summed per cell.

## 3. Porta results (full family, 16 checkpointed chunks; [`summary171.txt`](../data/cycle171/summary171.txt))
Key-free survivors: d free **1,539** (identical to case 158's strict survivors, a built-in consistency check) + d forced **36,642**.

| Cell | K4 observed / analytic expectation | Verdict |
|---|---|---|
| V1A, V2A periodic L 1–23 | **0 / 0.03** (each L ≤ 0.0095) | `EXACT-EXCL` |
| V1B, V2B periodic L 1–18 | **0 / ≤ 0.009 per L** | `EXACT-EXCL` |
| V1B L19, L20, L21, L22, L23 | 1/0.08, 4/0.39, 0/2.5, 30/15, 19/34 | `LOW-POWER` (chance rate) |
| V2B L19–23 | 0/0.08, 0/0.39, 1/2.5, 15/15, 30/34 | `LOW-POWER` |
| L 24–26 (all four) | e.g. V1A L26 7,554 / 7,500; V2B L25 168 / 150 | `LOW-POWER` |
| Running keys, d-free survivors (1,539 × 36 texts × 16 conventions) | **0 / < 10⁻¹⁵** | `EXACT-EXCL` |
| Running keys, d-forced survivors, slice p ≡ 0 mod 8 (20,723 perms; 4,583 forced + 174 free orderings) | **0 / < 10⁻¹⁴** | `EXACT-EXCL` on the slice; the other 7/8 → I-098 |
| Arbitrary key (key-free survivors, slice) | 4,757 vs 40 nulls 3,780/4,897/6,122 (min/median/max); rank p 0.61 (high) / 0.41 (low), floor 1/41 = 0.024 | `LOW-POWER` |

The 90 fit lines at L 19–23 decrypt (string level, [`k4_decodes.txt`](../data/cycle171/k4_decodes.txt)) to gibberish: best mean log10 quadgram
outside the cribs −7.54, median −8.11; one-error English plants score −4.13 ([`english171.txt`](../data/cycle171/english171.txt)).

**Clustering note.** On the 1/8 null slice, V1B L22 shows K4 16 vs null median 1 (rank p 0.049). Of K4's 30 V1B L22 fits in the whole family,
19 come from **one** permutation (perm 36112, in the slice) with 19 related orderings that share the same half-split. The fits are not
independent, so the cell's count is one cluster, at chance per permutation, and it is one of ~40 cells compared (no correction would keep
it). The same holds at V1B L20: its 4 fits (expectation 0.39) are **one** decryption, given by two near-identical decimations
(perms 89254, 161502) × an ordering and its mirror image; V1B L19's single fit (expectation 0.08) is gibberish too. Logged as I-101:
rank count cells by distinct decryptions / permutations.

Nulls: 40 shuffled K4s (seed 171000+i), periodic one-error on the slice. 39/40 have some periodic fit at L ≤ 23, all in the B cells
L 19–23 that are `LOW-POWER` anyway (expected).

## 4. I-091 bank part: one-error named running keys behind the 165,065-perm bank
Tool unchanged: `bookrk1e` ([case 157](157-one-error-running-keys-behind-decimations.md), cycle 169), 29 substitutions (24 additive tableaux + 5 XOR
codes), models A/B, the 36 texts of case 156 (a superset of cycle 36's: carved texts cyclic, Carter vol. I, Smith 1923, KJV John and NT, Reagan 1987, NSA 1947,
each forward and reversed). 16 checkpointed chunks of `perms97.bin`.

| Quantity | Value |
|---|---|
| configs (perm × model × mode × text) | 289,329,048 → **2.65 × 10¹³ key placements** |
| K4 FULL (24/24) / FIT23 (exactly 23/24) | **0 / 0** |
| analytic expectation of ≥ 23/24 chance fits | 1.8 × 10⁻¹⁸ (uniform); 1.4 × 10⁻⁶ worst case (every needed key letter at p = 0.127) |
| best one-error prefix depth / best strict depth | 12 (one config, KJV NT, model B) / 9 |
| null lineup, 500-perm slice, 40 shuffles | K4 best1 9; nulls 8/9/10; nulls ≥ K4 37/40, p = 0.93 (floor 0.024); 0/40 nulls with any ≥ 23/24 fit → Clopper–Pearson 95 % upper bound 7.2 % |

Verdict: named running keys behind the bank with one wrong letter **`EXACT-EXCL`**. The bank's depth of 12 is over 330× more configurations than
the slice; it is not a tail claim, and nothing near 23 exists.

## 5. Controls and recounts
- **Porta, 12 planted controls** ([`controls171_porta_planted.txt`](../data/cycle171/controls171_porta_planted.txt),
  [`ctl_verify171_porta.txt`](../data/cycle171/ctl_verify171_porta.txt)), independent string-level encryptor `ctl171.py`: 7 periodic (L 3–12) and
  3 running-key plants with exactly one error (even: wrong carved letter, odd: wrong crib letter re-encrypted), plus 2 two-error plants.
  **12/12**: all 10 one-error plants found at the planted (slot, ordering, variant, order, L / text offset). Periodic ones decrypt 96/97 (the one
  letter is the error) or 87/88 when key slots are blank. Both forced-d and free-d paths were exercised. Both two-error plants absent.
- **Bank, 14 controls** (`ctl171b.py`, [`ctl_verify171_bank.txt`](../data/cycle171/ctl_verify171_bank.txt); plants and raw outputs in [`controls171_outputs.txt`](../data/cycle171/controls171_outputs.txt)): 8 one-error (carved / crib) → FIT23 with the
  right missed index, no FULL; 2 non-crib errors → FULL; 2 two-error → absent; 2 clean → FULL. **14/14**.
- **Independent recounts** ([`recounts171.txt`](../data/cycle171/recounts171.txt)): numpy/python `recount171.py` (own ordering build, half test,
  one-dissent periodic test) vs `porta171` on 3,316 perms (stride 50): survivors 36 + 681 and all 104 periodic cells **identical**.
  `verify169.py depth` (numpy) vs `bookrk1e` on 40 random bank perms × 36 texts × 24 additive modes (69,120 configs): strict and one-error
  depth histograms **identical**.

## 6. What this does not exclude
Two or more errors; an inserted/dropped carved letter (I-093); Porta d-forced running keys on 7/8 of the family (I-098);
one-error running keys behind rail/Redefence/AMSCO (rest of I-091); Porta with unlisted books, other half-splits (KRYPTOS-tableau rows),
the 98-symbol `?` circle (rest of I-096); arbitrary-key Porta (no power).

Raw outputs: [`outputs_k4.txt`](../data/cycle171/outputs_k4.txt), [`nulls_outputs.txt`](../data/cycle171/nulls_outputs.txt); inputs: [`inputs_provenance.txt`](../data/cycle171/inputs_provenance.txt).

## 7. Reproduce
`tools/cycle171/run_cycle171.sh` (needs `/workspace/k4c168/run/all.bin` + `texts.txt`, `kryptos_support_backup/alpha.bin`, `perms97.bin`), then
`python3 tools/cycle171/summarize171.py RUN`; `verify171.py porta ctl/plants.txt`; `verify171.py bank ctl171b/planted.txt`;
`verify171.py decode K4 all.bin out/k4p.c*`; `recount171.py K4 all.bin alpha.bin 50 0` vs `NORK=1 porta171 K4 all.bin alpha.bin texts.txt 50 0`.
Wall time 03:19–03:35 PDT (~15.5 min, CPU shared with other jobs on the box; load average up to 16).
