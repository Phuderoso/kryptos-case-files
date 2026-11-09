#!/bin/bash
# Cycle 168: running keys (named texts, exact; unnamed English, scored) behind K3-law decimations + spiral/diagonal routes.
# Inputs: dec_perm.bin (tools/decimation_gen.py, cycle 59: 159,712 perms incl. inverses, not in the 165k bank),
# route_perm.bin (tools/route_gen61.py, cycle 61: 6,070 perms incl. inverses), key texts from cycles 34-36 (texts168.py),
# quadgrams.json and Gutenberg rkg*.txt from the support backup. bookrk.c (cycle 35) is used unchanged.
set -e
W=${W:-/workspace/k4c168/run}; T=$(cd "$(dirname "$0")" && pwd); B=${B:-/home/box/kryptos_support_backup}; cd $W
python3 $T/texts168.py /workspace/k4c34/texts.txt /workspace/k4c35/texts.txt /workspace/k4c36/texts.txt texts.txt
cat dec_perm.bin route_perm.bin > all.bin                     # 165,782 perms
n=$(( $(stat -c%s all.bin)/194 )); per=$(( (n+15)/16 )); split -b $((per*194)) -d -a 2 all.bin chunk_
gcc -O3 -march=native -o bookrk $T/../bookrk.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
$T/run_part_a.sh k4 $K4                                       # part A, K4, 16 chunks (checkpointed)
mkdir -p ctl; (cd ctl && python3 $T/rk168_controls.py ../all.bin ../texts.txt $B/rkg1260.txt 12 16801)
NNULL=24 $T/run_nulls_ctl.sh                                  # 12 controls + 24 nulls on chunk_15
for i in $(seq 0 11); do python3 $T/rk168_verify.py verify $(cat ctl/ctl$i.txt) ctl/ctl${i}_slice.bin texts.txt out/ctl$i.out; done > ctl_verify.txt
sed 's/md<29;md++/md<NMD;md++/' $T/../bookrk.c > bookrk_add.c && gcc -O3 -march=native -DNMD=24 -o bookrk_add bookrk_add.c
python3 $T/rk168_verify.py depth $K4 all.bin texts.txt 40 tail > recount40_tail.txt   # writes depth_sample.bin
python3 $T/rk168_verify.py depth $K4 all.bin texts.txt 40 > recount40_exact.txt
./bookrk_add $K4 depth_sample.bin texts.txt 30 | tail -1 > recount40_bookrk.txt
python3 $T/fragscore168.py all.bin $B/quadgrams.json k4 > partb_k4.json             # part B
python3 $T/fragscore168.py all.bin $B/quadgrams.json nulls:48:168 > partb_nulls.jsonl
python3 $T/fragscore168.py all.bin $B/quadgrams.json controls:12:1680 $B/rkg1260.txt $B/rkg345.txt > partb_controls.jsonl
python3 $T/fragscore168.py all.bin $B/quadgrams.json controls:8:1681 $B/rkg108.txt $B/rkg2147.txt > partb_controls2.jsonl
python3 $T/summarize168.py . > summary168.txt
