#!/bin/sh
# Cycle 46: Myszkowski transposition x periodic or progressive keyword substitution, exact.
# railamsco.c (cycle 44, = progkw.c of cycle 41 + SMAX cap) is reused unchanged; perms from myszkowski_gen.py.
# Needs qg.bin (cycles 39-41) and progkw_controls.py (cycle 41) in the same directory.
cd "$(dirname "$0")"
gcc -O3 -march=native -o railamsco railamsco.c
python3 myszkowski_gen.py            # 1,104,415 permutations (w 3-8 every tied rank pattern, 33 themed keywords, inverses, identity)
ln -sf perms_M.bin perms97.bin
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
CH=138052; : > jobs.txt
for s in 81 82 83 84; do python3 progkw_controls.py control $s > ctlM$s.txt 2>metaM$s.txt; done
for t in k4 null1 null2 null3; do
  if [ $t = k4 ]; then C=$K4; else C=$(python3 progkw_controls.py null ${t#null}); fi
  for c in 0 1 2 3 4 5 6 7; do a=$((c*CH)); echo "./railamsco $C perms_M.bin qg.bin $a $((a+CH)) > rM_${t}_c$c.txt" >> jobs.txt; done
done
for s in 81 82 83 84; do p=$(python3 -c "import ast;print(ast.literal_eval(open('metaM$s.txt').read())['perm'])"); a=$((p>2000?p-2000:0))
  echo "./railamsco $(head -1 ctlM$s.txt) perms_M.bin qg.bin $a $((p+2000)) > rM_ctl$s.txt" >> jobs.txt; done
xargs -P8 -I{} sh -c '{}' < jobs.txt
python3 myszkowski_summarize.py > summary.txt
# follow-up on the L=21 excess: list and score the partial fits for K4 and null 3
gcc -O3 -march=native -o l21 myszkowski_l21.c
N3=$(python3 progkw_controls.py null 3)
for c in 0 1 2 3 4 5 6 7; do a=$((c*CH)); ./l21 $K4 perms_M.bin qg.bin $a $((a+CH)) | grep P21 > l21_k4_c$c.txt; ./l21 $N3 perms_M.bin qg.bin $a $((a+CH)) | grep P21 > l21_n3_c$c.txt; done
python3 myszkowski_l21_score.py $N3 > l21_scores.txt
