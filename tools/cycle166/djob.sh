#!/bin/bash
# direct strict + 24 leave-one-crib-out runs for one text: djob.sh LABEL CT
X=$(dirname "$0")/split3; A=/home/box/kryptos_support_backup/alpha.bin
$X $2 $A - $1 0 1 86731; for d in $(seq 0 23); do $X $2 $A - $1 0 1 86731 $d | sed "s/^/D$d /"; done
