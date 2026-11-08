# Cycle 133 tools — plaintext-autokey (Quagmire III and keyword stacks) behind the bank

`qak.c` tests three model-Q families (substitution at the plaintext position, then one
of the 165,065 bank transpositions, either direction) against every vocabulary keyword
and every vocabulary primer of length 3–10:

- **Q** — Quagmire III PT-autokey: keyed alphabet from word W (unique letters then
  A–Z remainder, the K1/K2 construction), primer R, Vigenère / Beaufort / variant.
- **KA** — repeating keyword W on the A–Z or KRYPTOS tableau, then PT-autokey with
  primer R whose feedback is the first layer's output.
- **AK** — PT-autokey of the plaintext with primer R, then repeating keyword W.
  Both layers share one AZ or KA tableau; 3 × 3 directions.

For primer length L ≤ 10 no crib letter sits in the primer region, so the partial
crib signature (n = 24 − 2L letters) depends on W, L and the setting but not on the
primer letters. Each of the 330,130 permutations is hashed under that mask; a hit is
fully decrypted and checked against all 24 official crib letters. CT-fed autokey is
blind on this list (longest word 14; a CT primer must reach position 21). L ≥ 11 is
left open (n ≤ 2, filter underpowered).

- `qak CT words.txt perms.bin label lo hi` — rows lo..hi of the word list as W,
  every primer of length 3–10, all 39 settings.
- `plant.py` — 4 independent Python-encrypted controls and 2 shuffled nulls (seeds 13301–13302).
- `run_cycle133.sh` — K4 + two nulls, 8-way parallel.

Lists come from `tools/cycle131/mklists.py` (10,056 words).
