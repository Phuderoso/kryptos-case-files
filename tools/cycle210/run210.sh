#!/bin/bash
# Cycle 210 registered run (PREREG210). Own process group via setsid; caller applies the hard timeout.
# usage: run210.sh OUTDIR   (run from the directory holding wrq, wrbank, alph8.txt, p62.txt, bank.bin, all.bin, plants.tsv)
set -u
OUT=$1; mkdir -p $OUT; export OMP_NUM_THREADS=8
K4=$(cat k4.txt)
echo "start $(date +%T)"
# G0': AZ/AZ + KA/KA through wrq must reproduce wrbank (case 193 / 206) per tableau-form on the bank, L 1-20
printf "0 0\n1 1\n" > $OUT/p_g0.txt
./wrq $K4 bank.bin 1 20 alph8.txt $OUT/p_g0.txt 1 0 0 > $OUT/g0_wrq.txt
./wrbank $K4 bank.bin 1 20 0 > $OUT/g0_wrbank.txt
echo "g0 done $(date +%T)"
# plants (seed 209214): each on a 101-row slice of its family around the true row
python3 - <<'PY' > $OUT/plants_slices.txt
import struct
for l in open("plants.tsv"):
    f = l.rstrip("\n").split("\t"); fam, row = f[1], int(f[2]); fn = "bank.bin" if fam == "bank" else "all.bin"
    nr = 165065 if fam == "bank" else 165782; a = max(0, row - 50); b = min(nr, row + 51)
    with open(fn, "rb") as src: src.seek(a * 194); data = src.read((b - a) * 194)
    open(f"{'$OUT'}/plant_{f[0]}.bin", "wb").write(data); print(f[0], a)
PY
while IFS=$'\t' read id fam row d ix iy form L segE segB o1 o2 key ct pt; do
  ./wrq $ct $OUT/plant_$id.bin 1 17 alph8.txt p62.txt 1 0 200000 > $OUT/plant_$id.txt
done < plants.tsv
echo "plants done $(date +%T)"
# K4, full families, L 1-17, 62 pairs x 2 forms
./wrq $K4 bank.bin 1 17 alph8.txt p62.txt 1 0 5000 > $OUT/k4_bank.txt
echo "k4 bank done $(date +%T)"
./wrq $K4 all.bin 1 17 alph8.txt p62.txt 1 0 5000 > $OUT/k4_all.txt
echo "k4 all done $(date +%T)"
# nulls: 20 shuffled K4 (random.Random(209213)); null i (0-based) on rows q % 10 == i % 10 of bank (i < 10) or all.bin (i >= 10)
python3 -c "
import random
k=open('k4.txt').read().strip(); r=random.Random(209213)
for i in range(20):
    l=list(k); r.shuffle(l); print(''.join(l))" > $OUT/nulls_ct.txt
i=0; while read SH; do
  if [ $i -lt 10 ]; then F=bank.bin; else F=all.bin; fi
  ./wrq $SH $F 1 17 alph8.txt p62.txt 10 $((i % 10)) 200 > $OUT/null_$i.txt; echo "null $i $(date +%T)"; i=$((i+1)); done < $OUT/nulls_ct.txt
echo "end $(date +%T)"
