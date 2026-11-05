# Cycle 114 — Kryha cipher machine
Source: J.-F. Bouchaudy, *How the Kryha works* (http://www.jfbouch.fr/crypto/kryha/working.html), after P. Marks,
Cryptologia 35(2):114–155 (2011). See case-file/102.

    python3 testA114.py 200 30      # V1 published wheels, free alphabets (exact)      -> data/cycle114/testA.txt
    gcc -O2 -o /workspace/k4c114/v2_114 v2_114.c
    python3 testB114.py 20 10       # B1 any V1 wheel / B2 V2 any hole set, keyword alphabets (exact) -> testB.txt
    python3 testC114.py             # free wheel + free alphabets, CP-SAT, n 1-7 + nulls + controls -> testC.txt
    python3 sweepC114.py            # K4 only, n 8-20                                    -> sweepC.txt
kryha114.py holds the model, the published wheels and the V2 tooth counts. It reproduces Bouchaudy's worked
example (XYICPNDEAMAPDTRAX -> THECOURTISUNABLET).
