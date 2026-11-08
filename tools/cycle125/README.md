# tools/cycle125 — Digrafid (27-symbol digraphic fractionation) with one null or one missing letter

- `digrafid.c` — exact crib test. Grid 1 = keyword alphabet (A–Z + `#`) in 3 rows × 9; grid 2 = keyword alphabet in 9 rows × 3, filled down the columns (ACA) or across the rows; period p = 1–48 pairs. K4 is odd-length, so two length models: **A** one carved letter is a null (drop it, later crib positions shift by −1); **B** one cipher letter is missing before carved position d (98-letter cipher; the block with the gap is skipped, ≥ 12 crib letters must still be checked). Survivor = every checked crib letter matches.
- `mkkeys.py` — 9,401 distinct keyword alphabets (106 themed: cycle-52 list + Digrafid/fractionation words; plus cycle-56 vocabulary) and three pair lists: same key in both grids (9,401), themed × themed (11,130), themed × vocabulary both ways (1.97 M).
- `plant.py` — independent ACA reference encryptor, 4 planted controls (KRYPTOS/PALIMPSEST p 7 null at 50; SHADOW/SHADOW p 12 null at 96; DIGRAFID/BERLINCLOCK row-filled p 5 null at 10; LODESTONE/KRYPTOS p 9 last letter missing) and 3 shuffled-K4 nulls (seeds 12501–12503).
- `run_cycle125.sh` — full reproduction, about 2 minutes on 8 cores.

Results: [`data/cycle125/`](../../data/cycle125/); write-up: [`case-file/113-digrafid.md`](../../case-file/113-digrafid.md).
