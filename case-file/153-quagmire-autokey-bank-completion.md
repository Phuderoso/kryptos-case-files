# Case file 153 — Finishing the two-alphabet Quagmire autokey behind the bank (cycle 165)

**Status:** negative. **Type:** audit/variant (cycle 164 was a new family). IDEAS **I-074** (follow-up of I-015, [case 152](152-quagmire-iv-autokey-two-alphabets.md)).
Themed × themed behind the whole 165,065-entry bank: `EXACT-EXCL`. Themed (plain) × vocabulary (cipher) behind the bank: `EXACT-EXCL`
on a 1/1000 sample only.

## 1. A correction first: the cycle-164 full pass had finished
Case 152 said the full K4 bank pass "was stopped unfinished" and left nothing. That is wrong. Re-reading the run directory of
cycle 164 ([provenance](../data/cycle165/cycle164_fullpass_provenance.txt)):

- all 8 K4 slices exist, each written to `.tmp` and renamed only when `q4ak` exited 0, with mtimes 23:59:56–00:00:04 PDT;
- `done_K4.txt` (written by the script only after the 8 slices) reads 00:00:04 PDT;
- the slice ranges are contiguous over 0..165065 and the test counts add up to **1,205,074,859,520**, exactly
  165,065 entries × 2 directions × 9,506 pairs × 6 (Z, form) × 2 orders × 16 lags × 2 feeds;
- **0 consistent configurations** in every slice, every row.

The stop at 00:00:14 PDT killed the **null** phase that the script starts after K4 (no null slice was written). The full K4 result
was on disk and unreported. Its C/H lines are now published:
[`k4_fullbank_C_H_from_cycle164_run.txt`](../data/cycle165/k4_fullbank_C_H_from_cycle164_run.txt).

So I-074's premise (that the bank pass was memory-bound and needed blocking to finish) was mostly wrong. The tool was 1.4× slow,
not stuck. I still wrote the blocked, checkpointed version, because the job needed an independent re-run and nulls.

## 2. Tool
[`tools/cycle165/q4akb.c`](../tools/cycle165/q4akb.c) = `q4ak` with blocks of 64 entries (tables reused across the block) and
per-slice checkpoints ([`run_cycle165.sh`](../tools/cycle165/run_cycle165.sh)). Model, tests and output format are unchanged (see case 152).
Gain: ~12 % with 8 processes; none single-threaded. Equivalence with `q4ak`
([`equivalence.txt`](../data/cycle165/equivalence.txt)): the cycle-164 1/40 sample reproduces **byte for byte** (K4, null1, null2,
all C/H lines); recount mode, 5 × 5 alphabets, L 1–26: identical (274 consistent configurations); the six cycle-164 plants: identical.

## 3. Runs
| part | entries | K4 | nulls | label |
|---|---|---|---|---|
| themed × themed, full bank (cycle-164 run, recovered) | all 165,065 × 2 dirs, 1.21 × 10¹² tests | **0** consistent | — | — |
| themed × themed, independent re-run (q4akb) | ≡ 3 mod 8 (1/8), 1.51 × 10¹¹ tests | **0** | — | agrees with the full pass |
| themed × themed nulls | null1, null2 on ≡ 5 mod 8 (1/8 each); mnull01–04 on ≡ 7 mod 32 | — | **0** in all 6 (5.3 × 10¹¹ tests) | — |
| **themed × themed, bank, L 1–16, both orders, PT/CT, Vig/Beau/var, Z = X or Y** | | 0 | 0 | **`EXACT-EXCL`** |
| themed X × vocabulary Y (9,395 words, 22 chunks), bank sample | ≡ 11 mod 1000 (166 × 2 dirs), 1.25 × 10¹¹ tests | **0** | null1 0, null2 0 | `EXACT-EXCL` (sample only) |

Power: every bank row has ≥ 8 independent 1/26 checks (case 152), so the chance rate is ≤ 4.8 × 10⁻¹² per test; zero in K4 and in all
nulls is the expected chance picture, and the plants show that a true key does get through. No configuration with ≥ 6 checks
survived for K4, so there was nothing to decrypt; the crib and English checks had no input.

## 4. Controls
- Cycle-164 plants ctl1–5 behind the bank, each run on an 80-entry window so that the planted entry is inside a block, not at its
  start: **5/5 recovered**, full English plaintext or the expected partial, 24/24 crib letters; extra hits are the adjacent
  inverse entry of the same permutation and the column-structure echoes already seen in cycle 164. ctl6 (direct, ZEBRAFISH): recovered.
- New vocabulary plants ([`plant165.py`](../tools/cycle165/plant165.py)) on sampled entries, run against the chunk containing the word:
  vc1 SHADOW × SIGNALS, PT-fed, Z = Y, Vigenère, carved, L 9, inverse of entry 5011 → full plaintext (15 checks);
  vc2 KRYPTOS × PASSIONATE, CT-fed, Z = X, Beaufort, model Q, L 12, entry 120011 → plaintext after the primer (24 checks);
  vc3 CLOCK × CABLES, PT-fed, Z = Y, variant, model Q, L 16, inverse of 77011 → full plaintext (8 checks, the weakest row).
  **3/3, one hit each, no false positives** ([`controls_out.txt`](../data/cycle165/controls_out.txt)).

## 5. What this excludes and what it doesn't
Excluded (exact): Quagmire I/II/IV autokey, PT- or CT-fed, any primer of length 1–16, Vigenère/Beaufort/variant, key read through
either alphabet, two **different** alphabets from the 98 themed keyed alphabets, behind any of the 165,065 bank transpositions in
either direction and either index order. Also excluded on 1/1000 of the bank: themed plain alphabet × any vocabulary cipher alphabet.

Not excluded: the other 999/1000 of the bank for themed × vocabulary (≈ 97 × the themed × themed cost, ~12 h of 8-core time at this speed:
I-077); vocabulary (plain) × themed (cipher), not run behind the bank; vocabulary × vocabulary; lags 17–26 behind the bank;
one-error tolerance (I-076); alphabets outside the keyed-word construction.

## 6. Method note
A budget stop is not a failure until the run directory says so. Before calling a run unfinished, list the slices, their C lines
and the done markers. Added to the routine as I-078.
