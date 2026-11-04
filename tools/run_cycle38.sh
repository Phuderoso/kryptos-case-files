#!/bin/sh
# Cycle 38: lifted digit regrouping + themed keyword layer (both orders), K4 + 3 nulls + 3 planted controls (needs z3-solver)
cd "$(dirname "$0")"
python3 liftkey.py k4 > r_k4.txt &
for s in 1 2 3; do python3 liftkey.py null $s > r_null$s.txt & done
for s in 21 22 23 24 25 26 27 28 29; do python3 liftkey.py control $s > r_ctl$s.txt & done
wait
