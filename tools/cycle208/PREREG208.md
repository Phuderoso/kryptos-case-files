# PREREG208 — word restart R1 behind the K3-law decimations / routes (I-269), new family (cycle 208, 2026-11-12)

Written 2026-11-12 23:47 PT (America/Vancouver), base commit 9984a1f, **before any K4 or null run on this family**.

## Why
[Case 193](../../case-file/193-word-restart-two-alphabets-and-behind-bank.md) excluded the word-restart key R1 (key index = position of
the letter inside its plaintext word, mod L) behind the 165,065-entry columnar/rotation bank at L ≤ 16 (plant-gated in
[case 194](../../case-file/194-word-restart-bank-plant-gate.md)). The repo's *other* transposition family, the 165,782 K3-law
decimations / spiral-diagonal routes of `all.bin` (built cycle 168, used in cycles 173–183), was never combined with R1. This is
K3's actual transposition law (every s-th letter around a wheel) with a K1/K2-style key rule, so it is the closest untested
"K1–K3 style" pairing in the word-restart line.

## Tool and family
- Solver: `tools/cycle206/wrbank.c` **unchanged** (copied verbatim, gcc -O3 -march=native -fopenmp). Model Q: plaintext enciphered in
  plaintext order with R1 on one tableau (A–Z or KRYPTOS), then plaintext position i carved at S[i] (layer letter i = C[S[i]], the
  cycle 168/176/178 convention), S = entry (dir 0) or its inverse (dir 1). Vigenère / Beaufort / variant (variant = Vigenère for
  consistency), case 190 segmentations (EAST|NORTH|EAST variants × BERLIN|CLOCK variants), free offsets o1, o2 ∈ 0..L−1.
- Family: `all.bin`, md5 946402ca9cd1fcb962c51a16a76fef09 (sha256 prefix 8a9e1b3200cf803c), 165,782 rows, 165,740 distinct
  (42 duplicate rows), **closed under inverse** (checked on all rows; 108 self-inverse), no identity row, 796 rows shared with the
  165,065 bank. Because the family is inverse-closed, dir 1 re-covers dir 0 on a different row: raw cell counts are reported as
  produced (each configuration typically counted twice by direction and twice by Vigenère/variant), never deduplicated silently.
- Cribs at 1-indexed 22–34 (EASTNORTHEAST) and 64–74 (BERLINCLOCK).

## Gate G0 (regression)
`wrbank K4 x 1 26` must reproduce case 190's direct counts (0 at L ≤ 22; 2 / 184 / 414 / 692 at L 23–26).

## Controls (planted, invented plaintexts, not K4 guesses; seed 208209; recorded next free seed 208210)
Planted R1 ciphertexts behind uniformly drawn `all.bin` rows, direction uniform, tableau/form cycling AZ Vig, AZ Beau, KA Vig, KA Beau,
random uniform keys; detection = survivor line at the true (row, dir, tm, L, segE, segB, o1, o2) with the planted key on every
determined index (same rule as PREREG207), solver run on the full family at that single L.
- **Stratum M, n = 20, L 16:** case 194's template, words EAST | NORTHEAST and BERLIN | CLOCK, o1 = o2 = 0.
- **Stratum A, n = 20, L 16:** same text with EASTNORTH | EAST and BERLINCLOCK, o1 = o2 = 0 (alternative segmentation; "grid-aligned"
  has no meaning for decimations, so this stratum tests the other segmentation branch).
- **Stratum O, n = 10, L 16 (new: non-zero offsets, a blind spot of case 194):** crib words glued to the preceding word (…TURNEDEAST
  NORTHEAST … THATBERLIN CLOCK …), so o1 = 6, o2 = 4 with segmentation EAST|NORTHEAST + BERLIN|CLOCK.
- **Optional:** 5 stratum-M plants at L 17, descriptive.
- **Gate:** M ≥ 19 / 20, A ≥ 19 / 20, O ≥ 9 / 10. Any failure: no exclusion from this cycle may be cited as tool-validated for that
  stratum, and the tool is debugged before reuse.

## K4 run and null
- K4 behind the full family, L 1–22 (survivors printed up to 5,000) and L 23–26 (counts only).
- **Null:** 20 shuffled K4 (seed 208208; letters permuted, the 24 crib positions are then ordinary letters as in case 193), each over the
  full family, L 1–22. Per L: null mean cells and the fraction of nulls with ≥ 1 cell.
- **Decision (per L):** K4 = 0 and 0 / 20 nulls with a cell → **EXCLUDED (exact, under these assumptions, for this family)**; the
  rate claim is then backed by the analytic / null-mean estimate of P(any false survivor), and an L whose null mean implies
  P(any) > 1 % is labelled "excluded, weaker" (case 193 addendum lesson: 0/20 alone does not show < 5 %). Where ≥ 1 null has a cell:
  K4's count is compared with the null distribution → NO-DISCRIMINATION unless K4 exceeds every null; any K4 survivor at an L ≤ the
  last discriminating L is decrypted (layer filled where the key is determined) and read for English, key letters checked against
  a word list.

## Budget and process
≈ 8 min heavy compute total on 6 threads, in one owned process group (setsid + timeout, 600 s cap per stage); nothing outside the
group is touched. Nothing here is a solution claim: a solution must be a full 97-letter coherent English decryption with both cribs
at their official positions.
