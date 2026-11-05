#!/bin/bash
# Cycle 98: self-keying by transposition. Needs perms97.bin, dec_perm.bin, route_perm.bin (cycle 97 exports) and affine.bin (built below).
set -e
gcc -O2 -o selfkey selfkey.c
python3 - <<'PY'
import struct
out=[[(a*i+b)%97 for i in range(97)] for a in range(1,97) for b in range(97)]+[[(b-i)%97 for i in range(97)] for b in range(97)]
open('affine.bin','wb').write(b''.join(struct.pack('<97h',*p) for p in out))
PY
F="perms97.bin dec_perm.bin route_perm.bin affine.bin"
./selfkey $(cat k4.txt) $F > k4.out 2> k4.err
python3 ctl98.py > controls.txt
i=0; awk '{print $NF}' controls.txt | while read ct; do i=$((i+1)); ./selfkey $ct $F > ctl_$i.out 2> ctl_$i.err; done
