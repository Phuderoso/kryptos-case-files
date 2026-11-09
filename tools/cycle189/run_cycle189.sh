#!/bin/bash
# Cycle 189 registered run (PREREG189). Every job under setsid timeout; order = priority. Binaries: run/cmp189 (tools/cycle189/cmp189.c),
# run/lrk186 (cycle-187 binary, md5 4f41a243...). Support: all.bin, all_s512.bin, direct.bin, slice189.bin, all_r{6,7}s8.bin,
# azka.txt (A-Z, KRYPTOS), alpha_themed180.txt (144), alpha_direct189.txt (18,824 = vocabulary 18,776 + 48 themed not in it).
W=${W:-/workspace/k4c189/w}; cd $W; mkdir -p run/out run/rc run/i184; K4=$(cat run/k4.txt); C=run/cmp189; S=support
t0=$(date +%s); el(){ echo $(( $(date +%s)-t0 )); }
export OMP_NUM_THREADS=8
# C1: K4, A-Z/KRYPTOS, full set (165,782 routes), models P and C, Vig/Beau, all 260 pairs (m 2-25 < n <= 26, m does not divide n)
setsid timeout 240 $C $K4 $S/all.bin $S/azka.txt k4 0 999999 25 26 5 > run/out/c1_k4_full.txt; echo "C1 done $(el) s"
# C2: K4, direct (identity), 18,824 keyed alphabets (Quagmire III, same alphabet both sides)
setsid timeout 60 $C $K4 $S/direct.bin $S/alpha_direct189.txt k4 0 1 25 26 5 > run/out/c2_k4_direct.txt; echo "C2 done $(el) s"
# C3: K4, 144 themed alphabets on all_s512 (324 routes)
setsid timeout 60 $C $K4 $S/all_s512.bin $S/alpha_themed180.txt k4 0 999999 25 26 5 > run/out/c3_k4_s512_themed.txt; echo "C3 done $(el) s"
# Grid: K4 + 19 nulls (seeds 18911-18929), A-Z/KRYPTOS on all_s512 and direct vocabulary, PE 3
(echo "k4 $K4"; cat run/nulls189.txt) | while read lab ct; do
  setsid timeout 30 $C $ct $S/all_s512.bin $S/azka.txt $lab 0 999999 25 26 3 > run/out/g512_$lab.txt
  setsid timeout 30 $C $ct $S/direct.bin $S/alpha_direct189.txt $lab 0 1 25 26 3 > run/out/gdir_$lab.txt; done; echo "grid done $(el) s"
# Recount: independent numpy linear algebra vs cmp189 PE 0 on slice189 (45 rows), texts rc_texts.txt, A-Z/KRYPTOS
setsid timeout 120 python3 tools/recount189.py $S/slice189.bin $S/azka.txt run/rc_texts.txt 25 26 > run/rc/recount.txt
while read lab ct; do setsid timeout 30 $C $ct $S/slice189.bin $S/azka.txt $lab 0 99 25 26 0 > run/rc/cmp_$lab.txt; done < run/rc_texts.txt; echo "recount done $(el) s"
# Add-on: I-184 classes 6 and 7 (case 174 direction r, strict, L 1-3), each under timeout 60
V=$S/alpha172.txt; TH=$S/alpha_themed180.txt
for r in 6 7; do f=run/i184/k4.r.r${r}s8.txt; setsid timeout 60 run/lrk186 $K4 $S/all_r${r}s8.bin $V $TH k4 0 999999 1 1 3 q4r > $f.tmp && mv $f.tmp $f; echo "I-184 class $r done $(el) s"; done
