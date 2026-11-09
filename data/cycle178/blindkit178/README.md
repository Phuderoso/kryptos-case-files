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
