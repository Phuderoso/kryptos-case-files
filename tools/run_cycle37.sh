#!/bin/sh
# Cycle 37: lifted (mod-26) digit regrouping, K4 + 3 shuffled nulls + 3 planted controls (needs z3-solver)
cd "$(dirname "$0")"
python3 liftregroup.py k4
for s in 1 2 3; do python3 liftregroup.py null $s; done
for s in 11 12 13; do python3 liftregroup.py control $s; done
