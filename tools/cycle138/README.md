# Cycle 138 tools — CT-fed autokey, key letter read through the free plaintext alphabet

Model (Quagmire-style autokey fed by the ciphertext of the same layer):

- SUM: `y(c_j) = x(p_j) + x(c_{j−L})  (mod 26)`
- DIFF: `y(c_j) = x(c_{j−L}) − x(p_j)` (Beaufort; the variant form is the same test with `x → −x`)

`y` is a K1/K2-style keyed alphabet from a word; `x` is **any** of the 26! plaintext alphabets. Each crib gives a two-variable linear equation in the unknown values `x(·)`. `ctself.c` solves the system exactly: it builds components, writes every value as `x_v = s_v·r + o_v`, intersects the root sets demanded by the cycle equations (coefficients 0 or ±2), and backtracks over roots to enforce that `x` is injective.

- `ctself.c` — exact solver; reports satisfiable configurations with at least `MINCYC` independent cycle checks (first version, used for the direct pass).
- `ctself2.c` — same solver, plus enumeration of up to 300 solutions per satisfiable configuration, each scored by the summed excess of English quadgram log-probabilities (`Q + 5.5` per fully decoded window, crib positions excluded). Reports configurations scoring ≥ `THR` (default 8).
- `plant.py` — controls (random plaintext alphabet, independently encrypted in Python) and shuffled nulls (seeds 13801–13802).
- `run_cycle138.sh` — the bank run.

Usage: `ctself2 CT words.txt perms.bin label lo hi LMAX [pstride]` with environment `THR`, `MINWIN`, `ENUMCAP`, `QUAD` (path to the 26⁴ float32 table).
