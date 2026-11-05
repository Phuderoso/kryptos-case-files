#!/bin/bash
# Cycle 91 driver. jobs file lines: LABEL CT p tab mode align ; resume with data/cycle91/remaining.txt
# usage: bash run91.sh jobs.txt > out.txt   (needs pysat; one job per core, 420 s cap each)
D=$(cd "$(dirname "$0")" && pwd)
one() { r=$(timeout 420 python3 "$D/sat91.py" $2 $3 $4 $5 $6 2>&1 | cut -c1-90); echo "$1 p=$3 $4 m=$5 a=$6 ${r:-TIMEOUT}"; }
export -f one; export D
xargs -P "$(nproc)" -L1 bash -c 'one "$@"' _ < "$1"
