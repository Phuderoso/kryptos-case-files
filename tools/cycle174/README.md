# Cycle 174 tools (IDEAS I-108, with the I-110 grid): Hill n 2–3, Ragbaby and Portax behind K3-law decimations and routes

All three read `all.bin` (cycle 168: 165,782 perms = 159,712 K3-law decimations M 97–112 + 6,070 spiral/diagonal routes; each perm and
its inverse are both entries) with the `q4d172` convention (plaintext index i ↔ carved S[i]; ix 0 = substitute on plaintext order,
then transpose; ix 1 = transpose first).

- `PREREG174.md` — pre-registration (families, texts, the 4-cell I-110 grid, verdict rules, one disclosed smoke run), pushed before the K4/null runs (commit b7dc897).
- `hill174.c` — Hill n 2 and 3, linear `P = D·Z` and affine `P = D·Z + e`, A–Z / KRYPTOS numbering, block offsets 0..n−1, both orders.
  Exact row solving mod 2 and mod 13; consistent configs enumerated for an invertible D and decoded; analytic chance per sub-cell.
  Build `gcc -O3 -march=native -o hill174 hill174.c -lm`; run `hill174 CT perms.bin label qlo qhi`.
- `rag174.c` — classic Ragbaby (d = 1, both directions, any word division, word in progress ≤ 20 letters) then the transposition,
  over an alphabet list (`alpha172.txt`, 18,776). Same DFS as `tools/ragperm.c` (case 53) with lazy evaluation.
  `rag174 CT alpha.txt perms.bin label qlo qhi`.
- `portax174.c` — Portax (ACA period-pair digraphic, core copied from `tools/portax.c`, case 56), p 1–48, A–Z/KA, both orders;
  odd tail letters (no partner) are free; decodes print `?` where the cribs leave a column's slide ambiguous.
  `portax174 CT perms.bin label qlo qhi PMAX [pairs_threshold]`. (The `?` decode output and the threshold argument were added after the
  pre-registration push; the consistency test is unchanged.)
- `plant174.py` — 16 planted controls by an independent string-level encryptor (7 Hill incl. 1 negative, 4 Ragbaby, 5 Portax incl. 1 negative),
  each hidden in a 200-perm slice; `checkctl174.py` runs and checks them.
- `run_cycle174.sh` — K4 on the full family (16 chunks per tool) + K4 and 19 shuffled nulls on `all_s4.bin`; resumable (files ending in `END` are skipped).
- `summarize174.py` — per-sub-cell table, Hill's chance expectation, the pre-registered grid (leave-one-out z, max over 4 cells).
- `recount174.py` + `recount_run174.sh` + `compare174.py` + `ragrecount174.py` — independent Python brute force (every row vector for Hill,
  every slide for Portax, explicit word divisions for Ragbaby) on the plant slices, on K4/null ranges and on K4's Portax hits, compared per sub-cell / per config.
