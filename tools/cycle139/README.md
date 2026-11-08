# Cycle 139 tools — plaintext-fed autokey with a free plaintext alphabet, on crib-to-crib links

In a plaintext-fed autokey the key letter at position `j` is the plaintext letter `p_{j−L}`. When both `j` and `j−L` are crib positions, every letter in the equation is known except the plaintext-alphabet values, so the primer and the rest of the text never matter.

- Vigenère: `y(c_j) = x(p_j) + z(p_{j−L})` (Beaufort is the same test after `x → −x`)
- variant: `y(c_j) = x(p_j) − z(p_{j−L})`

`y` is a K1/K2-style keyed alphabet from a word; `x` is any of the 26! plaintext alphabets; the key letter is read through `z` ∈ {`y`, A–Z, KRYPTOS} (then `x(p_j)` is computed outright and must form a permutation) or `z = x` (two-variable equations mod 26, solved exactly as in cycle 138).

- `ptfree.c` — the exact test. `ptfree CT words.txt perms.bin|- label lo hi [pstride]`; environment `MINCHK` (default 5 independent checks) and `MINBITS` (default 23.5, applies to `z = x`: an even cycle counts log₂26 ≈ 4.7 bits, an odd cycle — coefficient ±2, including self-loops — only 1 bit).
- `plant.py` — controls with a random plaintext alphabet and random primer, independently encrypted; nulls seeds 13901–13902.
- `run_cycle139.sh` — the direct and bank runs.
