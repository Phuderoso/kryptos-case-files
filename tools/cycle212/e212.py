"""Cycle 212 analytic expected false-survivor count E(L) per full family for wrj (I-284), computed BEFORE any K4 run.
Approximation: each within-class constraint holds with probability 1/26 for a random ciphertext (uniform letters), independently.
E(L) = sum over configurations of  rows * 2 dirs * (allowed ordered pairs * 2 forms) * 26^-m(config).  m = 24 - #classes."""
SE=[[],[4],[9],[4,9]]; SB=[[],[6]]
def cidx(b,j,o,L):
    pb=-1
    for k in b:
        if k<=j: pb=k
    return ((j-pb) if pb>=0 else (o+j))%L
NA=144; PAIRS=NA*NA-2; ROWS={"bank":165065,"all":165782}
for L in range(1,18):
    s=0.0
    for s1 in range(4):
        for o1 in range(L):
            for s2 in range(2):
                for o2 in range(L):
                    cl=set(cidx(SE[s1],j,o1,L) for j in range(13))|set(cidx(SB[s2],j,o2,L) for j in range(11))
                    s+=26.0**-(24-len(cl))
    print(L, " ".join(f"{f} {2*ROWS[f]*PAIRS*2*s:.3g}" for f in ROWS), f"(8-word slice x{62*2/(PAIRS*2):.2e})")
