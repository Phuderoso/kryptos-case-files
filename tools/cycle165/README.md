# Cycle 165 tools (IDEAS I-074): finish / audit the I-015 bank pass

- `q4akb.c` — the cycle-164 `q4ak.c` with **permutation blocking**: the structures of a block of 64 bank entries are built
  first, then each of the 9,506 × 6 decryption tables is applied to the whole block (tables streamed once per block instead of
  once per entry). Same tests, same histogram (`H`), total (`C`) and survivor (`S`) lines; only the order of `S` lines can differ.
  Lag limit raised to 26 (bank and direct). Build `gcc -O3 -march=native -o q4akb q4akb.c`; usage as `q4ak`.
  Equivalence: identical to `q4ak` on the cycle-164 1/40 sample (all C/H lines), on the six cycle-164 plants (80-entry windows),
  and in recount mode (5 × 5 alphabets, L 1–26, 274 consistent configurations) — [`data/cycle165/equivalence.txt`](../../data/cycle165/equivalence.txt).
- `run_cycle165.sh` — stages `controls`, `sample`, `k4part` (1/8 of the bank for K4, entries ≡ 3 mod 8), `nulls` (null1/null2
  on 1/8, mnull01–04 on 1/32), `vocab` (themed X × vocabulary Y behind every 1000th entry, 22 vocabulary half-chunks so each
  process holds ≤ 200 MB of tables). **Checkpointed:** each slice writes `run/<name>.tmp` and renames it on success; a rerun skips
  finished slices.
- `plant165.py` — three bank plants with a vocabulary cipher alphabet from late chunks (SIGNALS, PASSIONATE, CABLES), on sampled
  entries, PT- and CT-fed, both index orders, both Z readings, L 9/12/16; encrypted with the independent string code of `plant164.py`.

Inputs in the work directory (same as cycle 164): `themed.txt`, `controls.txt`, `mnulls.txt` (= [`data/cycle164/`](../../data/cycle164/)),
`c6list.txt`, and `vh_*` = each cycle-164 vocabulary chunk split in two lines-wise (`split -n l/2 -d vchunk_NN vh_NN_`).
