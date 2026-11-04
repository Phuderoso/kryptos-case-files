#!/bin/sh
# Cycle 40: progressive affine (linear and second-order shift) on either side of 165,065 transpositions (incl. identity).
# Needs perms97.bin (python3 export_perms.py) and qg.bin (built as in run_cycle39.sh).
cd "$(dirname "$0")"
gcc -O3 -march=native -o progaffine progaffine.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
NP=165065
# second-order (q) runs, K4 and one null, split in 8 chunks each
for t in k4 qnull1; do
  if [ $t = k4 ]; then C=$K4; else C=$(python3 progaffine_controls.py null 101); fi
  for c in 0 1 2 3 4 5 6 7; do s=$((c*NP/8)); e=$(((c+1)*NP/8)); ./progaffine $C perms97.bin qg.bin $s $e 1 > rq_${t}_$c.txt & done
done
# linear runs: K4, 10 nulls, 6 planted linear controls
./progaffine $K4 perms97.bin qg.bin 0 $NP 0 > r_k4.txt &
for s in 1 2 3 4 5 6 7 8 9 10; do ./progaffine $(python3 progaffine_controls.py null $s) perms97.bin qg.bin 0 $NP 0 > r_null$s.txt & done
for s in 41 42 43 44 45 46; do ./progaffine $(python3 progaffine_controls.py control $s 2>meta_ctl$s.txt) perms97.bin qg.bin 0 $NP 0 > r_ctl$s.txt & done
# second-order controls: 20,000-transposition window containing the planted one
for s in 47 48; do C=$(python3 progaffine_controls.py qcontrol $s 2>meta_ctl$s.txt); P=$(python3 -c "import ast;print(ast.literal_eval(open('meta_ctl$s.txt').read())['perm'])")
  S=$((P>10000 ? P-10000 : 0)); ./progaffine $C perms97.bin qg.bin $S $((S+20000)) 1 > r_ctl$s.txt & done
wait
python3 progaffine_summarize.py
