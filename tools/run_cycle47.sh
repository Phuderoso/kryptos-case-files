#!/bin/bash
# Cycle 47: turning grille (convention A) x periodic key, exact. Jobs in jobs.txt, 60 s cap each, 8 in parallel.
cd "$(dirname "$0")"
xargs -P 8 -L 1 bash -c 'timeout 60 python3 grille_exact.py "$0" "$1" "$2" "$3" "$4" || echo "$0 A $1 $2 $3 L=$4 TIMEOUT"' < "$1"
