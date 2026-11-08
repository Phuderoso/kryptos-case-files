# tools/cycle124 — every column order of width 9 and 10 + periodic key

- `allcol.c` — exact crib test over **all** w! column orders (w = 9: 362,880; w = 10: 3,628,800; split by π[0] for parallel runs), rotation 0, ragged 97-letter grid (short last row holds columns 0..97 mod w − 1). Read by columns (COL, textbook keyword columnar) or row by row with the columns permuted (ROW); both directions (plaintext written into the grid, or σ⁻¹). Then a periodic key p 1..PMAX on the A–Z or KRYPTOS tableau, Vigenère or Beaufort (variant has Vigenère's consistency), key indexed by plaintext position (model A, key before transposition) or carved position (model B, key after). Survivor = all 24 crib letters consistent.
- `plant.py` — independent textbook encryptors (columnar, row read, inverse) for 4 planted controls (PALIMPSEST w10, LODESTONE w9, UNDERGRUND w10 row read, NORTHEAST w9 inverse; keys KRYPTOS p7 KA, SHADOWFORCE p11 Beaufort, ABSCISSA p8, ILLUSIONDIGETALQ p16 KA) + 3 shuffled-K4 nulls (seeds 125–127); 7 more nulls (seeds 128–134) were run the same way at p ≤ 22 for the crib-distinct baseline (`data/cycle124/results.txt`).
- `score_surv.py` — decrypts each survivor with the crib-derived key residues ('?' where a residue is unknown) and scores it by mean log10 quadgram.
- `run_cycle124.sh` — full reproduction, about 2 minutes on 8 cores.

Results: [`data/cycle124/`](../../data/cycle124/); write-up: [`case-file/112-all-orders-w9-w10.md`](../../case-file/112-all-orders-w9-w10.md).
