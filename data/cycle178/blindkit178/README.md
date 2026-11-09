# Blind kit 178 (IDEAS I-106) — for the Voynich desk, or anyone

Six 97-letter ciphertexts in [`kit178.txt`](kit178.txt), published in cycle 178 (2026-11-09). Each one was made the way the
cycle-178 hypothesis would make K4, but with its own plaintext: plaintext → (substitution) → (one transposition from the 165,782
K3-law decimations / routes of `all.bin`, md5 946402ca9cd1fcb962c51a16a76fef09, built in cycle 168), in one of the two layer orders.
Every plaintext carries the K4 cribs EASTNORTHEAST at 21–33 and BERLINCLOCK at 63–73 (0-indexed).

- **Some items are positives:** the key is an affine linear recurrence mod 26 (any family member of
  [case 166](../../../case-file/166-linear-recurrence-behind-decimations.md) §2: M0, M1 or W), A–Z or KRYPTOS tableau, Vigenère or
  Beaufort. **Some are decoys** (same layers, a random non-recurrent key). How many of each is part of the test.
- **Answer per item:** the plaintext at positions 21–96 (76 letters; positions 0–20 are not determined when the last weight is
  not a unit mod 26), or `NONE` for a decoy. Check: `sha256("B<n>|<answer>")` must equal the hash printed after the item, e.g.
  `printf 'B1|NONE' | sha256sum`.
- **Commitment:** the last line is the SHA-256 of the private answer file (parameters, perm row q, plaintexts), which stays off the
  repo until the review comes back; the generator script will be published with it.
- **What a good review reports:** per item, positive/decoy, the perm row q, the layer order, L, tableau, form, (c, d), the plaintext
  21–96, and the false-positive behaviour of the reviewer's own method on the decoys.

Validation on our side (cycle 178): `lr178` recovered every positive at its planted perm and replayed it to the planted plaintext;
no decoy produced a fit.

## Reveal (cycle 185, 2026-11-09, IDEAS I-145)
No review came back by cycle 185, so the answers are published as promised: [`answers178.json`](answers178.json) (byte-identical to the
private file; `sha256sum answers178.json` = 218831985fdf677b2964f157d285241089b0558f0ee26223d2e434bf8edf65b0, the commitment above)
and the generator [`blind178.py`](blind178.py) (published verbatim under its working name `blind178_PRIVATE.py`). All six item hashes
`sha256("B<n>|<answer>")` check out. **B1–B4 are positives** (B1 ix 1 L 3 A–Z Vig, q 114849; B2 ix 0 L 4 KA Beau, q 145473; B3 ix 0 L 7
A–Z Vig, q 15321; B4 ix 1 L 8 KA Vig, q 59011), **B5–B6 are decoys** (random keys). Nothing to score; the kit stays usable as an
un-blinded exercise.
