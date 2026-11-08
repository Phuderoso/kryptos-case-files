# Cycle 146 tools

`mixdir.c` — periodic key whose phases each choose their own direction: Vigenère (L = p + k) or Beaufort (L = k − p),
tableau A–Z or KRYPTOS. Per phase the crib pairs fix the key letter exactly for either direction, so the test is exact
(one pass, no search); phases with one crib are form-ambiguous and every combination is quadgram-scored. Direct, and
behind any bank permutation (both directions, model Q and carved). `plant.py` makes six planted controls
(direct, bank, inverse, P 5–19) and two shuffled nulls. Build: `gcc -O2 -march=native mixdir.c -o mixdir`.
Run: `mixdir CT perms97.bin|- label lo hi Pmin Pmax minchecks`.
