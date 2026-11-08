# Cycle 137 tools — CT-fed autokey, keyed cipher alphabet, free plaintext alphabet

`ctfree.c` tests ciphertext-fed autokey in the form `y(c_j) = x(p_j) ± z(c_{j-L})`,
where `y` is a keyed cipher alphabet, `z` reads the key letter (same keyed
alphabet, A–Z or KRYPTOS) and `x` is **any** plaintext alphabet. Because the
feedback letter is ciphertext (known), `x(p_j)` is computable at every crib; the
test is that these numbers form a permutation of the crib letters (equal letters
equal, different letters different). At least 6 equalities are required.

`ctfree CT words.txt perms.bin label lo hi LMAX [pstride]` — both bank
directions, carved index and plaintext index (model Q), lags 1..LMAX.
Run with a one-entry identity file for the direct test.

`plant.py` — 4 Python-encrypted controls with random plaintext alphabets and 2
shuffled nulls (seeds 13701–13702). `run_cycle137.sh` — K4 in full, nulls on
every tenth bank entry, 8-way parallel.
