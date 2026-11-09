"""Cycle 165 bank controls for the themed x vocabulary sample (X themed, Y vocabulary word from a late chunk), planted on
sampled bank entries (11 + 1000k). Encryption reuses the independent string-alphabet code of plant164.py."""
import sys
sys.path.insert(0, "/workspace/k4c165/tools/cycle164"); sys.path.insert(0, "/workspace/k4c165/tools/cycle127")
import numpy as np
from plant164 import keyed, autokey, move
from plant import plain
CTL = [("vc1","SHADOW","SIGNALS",1,0,"PT","QUIETNESS","carved",5011,1),
       ("vc2","KRYPTOS","PASSIONATE",0,1,"CT","LANGLEYVIRGI","pt",120011,0),
       ("vc3","CLOCK","CABLES",1,2,"PT","ABCDEFGHIJKLMNOP","pt",77011,1)]
P = plain(); B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
for name, x, y, zY, f, feed, primer, order, q, d in CTL:
    X, Y = keyed(x), keyed(y); s = B[q] if d == 0 else np.argsort(B[q])
    ct = move(autokey(P, primer, X, Y, zY, f, feed), s) if order == "pt" else autokey(move(P, s), primer, X, Y, zY, f, feed)
    print(name, ct, x, y, "zY" if zY else "zX", ["vig","beau","var"][f], feed, primer, len(primer), order, q, d)
