import numpy as np, sys
from progkw_controls import plain, KA
perms=np.fromfile("perms_A.bin",dtype=np.int16).reshape(-1,97)
idx=int(sys.argv[1]); P=perms[idx]; pt=plain(int(sys.argv[2])); k=[KA.index(c) for c in "ABSCISSA"]; L=8
car=[None]*97
for i in range(97): car[P[i]]=KA[(KA.index(pt[i])+k[i%L])%26]   # model A, KA Vigenere, s=0
print("".join(car))
