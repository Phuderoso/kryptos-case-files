#!/bin/bash
# Cycle 212 registered run (PREREG212, I-284). Run from w/ (wrj, wrq, alph8.txt, p62.txt, alpha_themed180.txt, bank.bin, all.bin,
# plants.tsv, plants212.tsv, k4.txt). Own process group via setsid; caller applies the hard timeout. Every step writes its own file.
set -u
OUT=$1; mkdir -p $OUT; export OMP_NUM_THREADS=8
K4=$(cat k4.txt); A=alpha_themed180.txt
echo "start $(date +%T)"
# G0'' (I-283): wrj with case 197's 8 alphabets / 62 pairs must reproduce case 197's published K4 numbers, L 1-17 (both families)
./wrj $K4 bank.bin 1 17 alph8.txt p62.txt 1 0 5000 > $OUT/g0_bank.txt
./wrj $K4 all.bin 1 17 alph8.txt p62.txt 1 0 5000 > $OUT/g0_all.txt
echo "g0 done $(date +%T)"
# plants: 12 (case 197) + 8 (new, seed 209218) on 101-row slices, 144 alphabets, all pairs, L 1-16
python3 - "$OUT" <<'PY'
import sys
OUT = sys.argv[1]
with open(f"{OUT}/plants_slices.txt", "w") as o:
    for fn, tag in (("plants.tsv", "c197"), ("plants212.tsv", "new")):
        for l in open(fn):
            f = l.rstrip("\n").split("\t"); fam, row = f[1], int(f[2]); src = "bank.bin" if fam == "bank" else "all.bin"
            nr = 165065 if fam == "bank" else 165782; a = max(0, row - 50); b = min(nr, row + 51)
            with open(src, "rb") as s: s.seek(a * 194); data = s.read((b - a) * 194)
            open(f"{OUT}/plant_{tag}_{f[0]}.bin", "wb").write(data); o.write(f"{tag}_{f[0]} {a}\n")
PY
for P in plants.tsv:c197 plants212.tsv:new; do F=${P%%:*}; T=${P##*:}
  while IFS=$'\t' read id fam row d ix iy form L segE segB o1 o2 key ct pt; do
    ./wrj $ct $OUT/plant_${T}_$id.bin 1 16 $A all 1 0 200000 > $OUT/plant_${T}_$id.txt
  done < $F; done
python3 check212.py $OUT > $OUT/plants_check.txt; tail -1 $OUT/plants_check.txt
echo "plants done $(date +%T)"
# K4, full families, L 1-16, 144 alphabets, all ordered pairs except AZ/AZ and KA/KA, both forms
./wrj $K4 bank.bin 1 16 $A all 1 0 5000 > $OUT/k4_bank.txt; echo "k4 bank done $(date +%T)"; grep "^T" $OUT/k4_bank.txt
./wrj $K4 all.bin 1 16 $A all 1 0 5000 > $OUT/k4_all.txt; echo "k4 all done $(date +%T)"; grep "^T" $OUT/k4_all.txt
# nulls: 20 shuffled K4 (random.Random(209219)); null i on rows q % 10 == i % 10 of bank (i < 10) or all.bin (i >= 10)
python3 -c "
import random
k=open('k4.txt').read().strip(); r=random.Random(209219)
for i in range(20):
    l=list(k); r.shuffle(l); print(''.join(l))" > $OUT/nulls_ct.txt
i=0; while read SH; do
  if [ $i -lt 10 ]; then F=bank.bin; else F=all.bin; fi
  ./wrj $SH $F 1 16 $A all 10 $((i % 10)) 200 > $OUT/null_$i.txt; echo "null $i $(date +%T) $(grep '^T' $OUT/null_$i.txt | sed 's/.*survivors[^=]*=//')"; i=$((i+1)); done < $OUT/nulls_ct.txt
echo "end $(date +%T)"
