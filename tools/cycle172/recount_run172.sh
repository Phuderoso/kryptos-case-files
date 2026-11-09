#!/bin/bash
# runs recount172.py on every line of run/recount_list.txt (label CT perms q ix p vig N beau N) and compares with q4d172's counts
cd ${W:-/workspace/k4c172}
cat run/recount_list.txt | xargs -P 6 -L 1 sh -c 'r=$(python3 tools/recount172.py "$1" "$2" "$3" "$4" "$5"); echo "$0 q=$3 ix=$4 p=$5 q4d172: vig $7 beau $9 | recount: $r"' > run/recount172.txt
awk '{ok=($6==$12&&$8==$14)?"AGREE":"DIFFER"; print $0, ok}' run/recount172.txt > run/recount172_cmp.txt
grep -c AGREE run/recount172_cmp.txt
