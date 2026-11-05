#!/bin/bash
# Cycle 85: halfabet screen over the 86,731-alphabet list x 165,065 transpositions, 8 parallel chunks per text.
# usage: run85.sh BIN SUPPORT_DIR TEXT... ; writes out_<text>_<chunk>.txt in the current directory
BIN=$1; S=$2; shift 2
for T in "$@"; do for c in 0 1 2 3 4 5 6 7; do echo "$T $c"; done; done | \
 xargs -P8 -n2 sh -c 'a0=$(( $2*10842 )); a1=$(( ($2+1)*10842 )); '"$BIN"' '"$S"'/perms97.bin '"$S"'/alpha.bin $1.txt 26 $a0 $a1 > out_$1_$2.txt' sh
