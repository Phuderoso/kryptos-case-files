#!/bin/bash
# Cycle 210 plant-step fix (disclosed): in run210.sh the slice writer sat in a quoted heredoc, so '$OUT' was not expanded and every
# plant slice was missing (wrq segfaulted on the absent file). Same plants.tsv (hash in hashes.txt), same wrq, same pass rule.
set -u
OUT=$1; export OMP_NUM_THREADS=8
OUT=$OUT python3 - <<'PY' > $OUT/plants_slices.txt
import os
OUT = os.environ["OUT"]
for l in open("plants.tsv"):
    f = l.rstrip("\n").split("\t"); fam, row = f[1], int(f[2]); fn = "bank.bin" if fam == "bank" else "all.bin"
    nr = 165065 if fam == "bank" else 165782; a = max(0, row - 50); b = min(nr, row + 51)
    with open(fn, "rb") as src: src.seek(a * 194); data = src.read((b - a) * 194)
    open(f"{OUT}/plant_{f[0]}.bin", "wb").write(data); print(f[0], a)
PY
while IFS=$'\t' read id fam row d ix iy form L segE segB o1 o2 key ct pt; do
  ./wrq $ct $OUT/plant_$id.bin 1 17 alph8.txt p62.txt 1 0 200000 > $OUT/plant_$id.txt
done < plants.tsv
