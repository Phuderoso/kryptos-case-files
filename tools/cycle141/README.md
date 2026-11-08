# Cycle 141 tools — Hill 5×5

`hill5.c` tests a 5×5 Hill cipher with any invertible decryption matrix mod 26, every block
alignment (o = 0–4; 97 = 19·5 + 2), standard A–Z or KRYPTOS-alphabet numbering, directly and
behind bank permutations (model Q: undo transposition then Hill; carved order: Hill then
undo transposition).

Each row of the decryption matrix only meets the plaintext letters in its own residue class,
so the 24 crib letters give each row its own small linear system (4–6 equations in 5 unknowns
directly; scattered behind a transposition). Rows are solved exactly mod 2 and mod 13 and
joined by CRT. Inconsistent systems are excluded outright; consistent but underdetermined ones
are enumerated (≤ 676 solutions per row, ≤ 200,000 matrices per configuration), invertible
matrices are kept, and the full decryption is ranked by mean log10 quadgram over windows
outside the cribs.

`plant.py` builds 5 controls (seed 14100) and 2 shuffled-K4 nulls; `run_cycle141.sh` runs
everything (~7 min on 8 cores). Control 4 is underdetermined at the default caps and is run
with `ROWCAP=17576 COMBOCAP=2000000`; that case is a stated limit of the bank run.
