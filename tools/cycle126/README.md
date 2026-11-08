# Cycle 126 tools

- `allcol2.c`: cycle 124's exhaustive all-column-orders solver (`tools/cycle124/allcol.c`) with an alphabet-set argument. Pair codes: 0 = A–Z/A–Z, 1 = KRYPTOS/KRYPTOS (Quagmire III), 2 = plaintext KRYPTOS / cipher A–Z (Quagmire I), 3 = plaintext A–Z / cipher KRYPTOS (Quagmire II). Build: `gcc -O2 -o allcol2 allcol2.c`. Usage: `allcol2 CT w first PMAX label ALPHSET`.
- `plant.py`: planted Quagmire I/II and width-11 controls built with an independent textbook encryptor (reuses cycle 124's transposition helpers), plus 3 shuffled-K4 nulls.
- `run_cycle126.sh`: the run (about 7.5 minutes on 8 cores).
