#!/bin/bash
# Cycle 86 follow-up (for cycle 87+): shuffled nulls at p 8 in the one config where K4 came back SAT (AZ Beaufort odd),
# then the 4 K4 p 8 configs still pending. Run from a scratch copy of tools/cycle83 + controls83.json (with ctl4/ctl5).
cd "$(dirname "$0")"
TO=${TO:-420} timeout ${BUDGET:-470} python3 run83.py null0:8:AZ/1/1 null1:8:AZ/1/1 K4:8:all
pkill -f "python3 run83.py"   # timeout only kills the parent; stop orphaned pool workers
