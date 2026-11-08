# Cycle 129 — ACA Periodic Gromark

- `mkcfg.py` builds the ACA Periodic Gromark key stream for each keyword: cipher alphabet from the keyword block read by columns in key order, primer = the keyword's numerical key, chain addition with lag L, each group of L letters offset by the position of the matching keyword letter in the cipher alphabet. It reproduces the ACA's published ENIGMA example letter for letter (`WINTRYSHOWERS...` → `RHNAAX NRUZBN ... TLUD`). Variants: cipher alphabet = plain keyword-mixed or KRYPTOS; plaintext alphabet A–Z or KRYPTOS.
- `pgcheck.c` checks each key stream against the 24 crib letters, directly and behind all 165,065 bank transpositions (each also inverted), with the key before (model A) or after (model B) the transposition, Vigenère (ACA) or Beaufort form. Exact.
- `plant.py` makes four planted controls and two shuffled-K4 nulls. `run_cycle129.sh` runs everything (~5 min on 8 cores).
