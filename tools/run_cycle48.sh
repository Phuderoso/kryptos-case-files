#!/bin/bash
# Cycle 48: turning grille, convention B (classic Fleissner), exact SAT. Usage: run_cycle48.sh JOBFILE [timeout_s]
cd "$(dirname "$0")"
xargs -P 8 -L 1 bash -c 'timeout '"${2:-240}"' python3 fleissner_cnf.py "$0" "$1" "$2" "$3" "$4" || echo "$0 $1 $2 $3 L=$4 TIMEOUT"' < "$1"
