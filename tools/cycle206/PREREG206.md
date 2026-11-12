# PREREG206 — word restart beyond one tableau (I-258), new structure (cycle 206, 2026-11-12, written before any K4 run)

Cycle 203 ([case 190](../../case-file/190-word-restart-key.md)) excluded the word-restart key R1 (key index = position of the letter
inside its plaintext word, mod L) on one tableau with **no transposition**, and Quagmire III by SAT at small L. Its "open" list:
two different alphabets, a transposition layer, other restart markers. This cycle tests the first two.

## Part A — R1 behind the 165,065-transposition bank (exact)
- **Model (model Q, as in cycles 133/164):** the clerk enciphers the plaintext in plaintext order with a word-restart key on one
  tableau (AZ or KA), then applies a transposition σ from the bank `perms97.bin` (165,065 entries, both directions σ and σ⁻¹).
  Plaintext letter i is carved at the bank position, i.e. layer letter i = C[S[i]] exactly as `q4ak.c` (cycle 164) reads the bank.
  Cribs at plaintext positions 22–34 and 64–74 (1-indexed).
- **Rules:** Vigenère / Beaufort / variant on AZ and KA (variant gives the same consistency test as Vigenère and is counted
  separately only to stay comparable with case 190). Primary segmentations of case 190 (4 × 2), free word offset o ∈ 0..L−1 per crib,
  L = 1..26 computed, decision range set by the null below.
- **Survivor:** equal key indices give equal key values on all 24 crib letters.
- **Gate G0 (regression):** the identity permutation must reproduce case 190's direct counts (0 at L ≤ 22; 2 / 184 / 414 / 692 at L 23–26).
- **Control C1:** an invented K2-style plaintext enciphered with R1 (KA Vigenère, key ABSCISSA, L 8) then a bank permutation
  (entry 12,345, dir 0) must be found at that entry with the right key letters. **C1b:** same with AZ Beaufort, key PALIMPSEST, L 10, entry 98,765 dir 1.
- **Null:** 20 shuffled K4 (seed 206206; letters permuted, cribs kept), each run over the full bank. For each L, the null mean
  number of surviving (perm, dir, tableau, mode) cells and the fraction of nulls with ≥ 1 survivor are reported.
- **Decision:** at every L where < 5 % of nulls (i.e. 0 of 20) have a survivor and K4 has 0 survivors: **EXCLUDED (exact, under these
  assumptions, for this bank)**. Where the null survives in ≥ 1 of 20 shuffles: K4 survivors are compared with the null and labelled
  NO-DISCRIMINATION unless K4 exceeds every null; any K4 survivor at a discriminating L is decrypted (layer filled where the key is
  known) and read for English; key letters checked against a word list.

## Part B — R1 with two alphabets, direct (SAT)
- **Models:** Quagmire I (plain alphabet unknown, cipher A–Z), Quagmire II (plain A–Z, cipher alphabet unknown), Quagmire IV (both
  unknown and independent), Vigenère form c = Y[x(p) + s_k] and Beaufort form c = Y[s_k − x(p)]; key index R1 as case 190; same
  segmentations; offsets o ∈ 0..L−1. Solver pysat Glucose4, as `sat203.py`.
- **Output:** for each model × form, the smallest L at which K4 becomes SAT (scan L = 1, 2, …, stop at first SAT; L ≤ 13).
  UNSAT at an L for every segmentation and offset = **EXCLUDED (exact)** at that L. SAT = **underdetermined**, not support, unless
  nulls stay UNSAT there.
- **Control C2:** planted Quagmire IV R1 (random X, Y, L 8, invented text) must be SAT at its true configuration; C2b planted QII.
- **Null:** 5 shuffled K4 per model × form (seed 206207), first SAT L. Descriptive (small sample).
- **Budget:** ≈ 8 min of heavy compute in total; SAT runs carry a wall-clock cap and report where they stopped.

Nothing here is a solution claim; a real solution must be a full 97-letter English decryption with the cribs in place.
