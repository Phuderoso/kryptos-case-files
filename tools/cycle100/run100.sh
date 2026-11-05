#!/bin/bash
cd /workspace/k4c100
K=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
for w in 12 13; do seq 0 $((w-1)) | xargs -P 8 -I{} sh -c "./homocol $K $w {} > k4_col${w}_{}.out 2> k4_col${w}_{}.err"; done
i=0; while read n; do i=$((i+1)); for w in 9 10 11; do ./homocol $n $w > null${i}_col$w.out 2>> null${i}_col.err; done; seq 0 11 | xargs -P 8 -I{} sh -c "./homocol $n 12 {} > null${i}_col12_{}.out 2>> null${i}_col12.err"; done < nulls.txt
echo DONE > done.flag
