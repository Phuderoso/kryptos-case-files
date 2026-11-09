#!/bin/bash
# Cycle 166 part B: all 86,731 alphabets behind every 20th bank entry with offset 10 (q = 10 mod 20; disjoint from the
# stride-200 sample), K4 + null1 + mnull01, 8 resumable slices each.
H=$(cd "$(dirname "$0")" && pwd); W=${W:-/workspace/k4c166/run166}; A=/home/box/kryptos_support_backup/alpha.bin; B=/home/box/kryptos_support_backup/perms97.bin
cd $W; X=$H/split3
grep -E '^(K4|null1|mnull01) ' $H/texts166.txt | while read lab ct; do for i in 0 1 2 3 4 5 6 7; do lo=$((i*20640+10)); hi=$(((i+1)*20640+10));
  [ -s BS20_${lab}_$i.txt ] || echo "$ct $lab $lo $hi $i"; done; done |
 xargs -P 8 -L 1 sh -c "$X \"\$0\" $A $B \"\$1\" \"\$2\" \"\$3\" 86731 -1 20 > BS20_\"\$1\"_\"\$4\".tmp && mv BS20_\"\$1\"_\"\$4\".tmp BS20_\"\$1\"_\"\$4\".txt"
date > doneB.txt
