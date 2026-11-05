"""Cycle 106 audit of cycle 104: 'fully general periodic substitution (free alphabet per phase) is inconsistent at
every p <= 7 (+9,10,14,15,17,21,25)'. Independent check: for period p, within each residue class the crib pairs
(plain->cipher) must form a partial bijection. Also report the first contradiction for each period."""
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
P={21+k:c for k,c in enumerate("EASTNORTHEAST")}; P.update({63+k:c for k,c in enumerate("BERLINCLOCK")})
bad=[]
for p in range(1,49):
    contra=None
    for r in range(p):
        f={};g={}
        for j in sorted(P):
            if j%p!=r: continue
            a,b=P[j],K4[j]
            if f.get(a,b)!=b: contra=(r,j,f"{a}->{f[a]} and {a}->{b}"); break
            if g.get(b,a)!=a: contra=(r,j,f"{g[b]}->{b} and {a}->{b}"); break
            f[a]=b; g[b]=a
        if contra: break
    if contra: bad.append(p); print(p,"inconsistent",contra)
print("inconsistent periods:",bad)
