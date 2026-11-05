import sys; sys.path.insert(0,"tools")
from kryptos_text import K3
from solve_k1_k2_k3 import k3_dec
body=K3[:336]; pt=k3_dec(K3)[:336]
# find perm: pt[i]=body[p[i]] via the rotation on indices
def rot(seq,w):
    h=len(seq)//w; return [seq[(h-1-r)*w+c] for c in range(w) for r in range(h)]
p=rot(rot(list(range(336)),24),8)
assert "".join(body[j] for j in p)==pt
d=[(p[i+1]-p[i])%336 for i in range(335)]
from collections import Counter; print(Counter(d).most_common(5))
d2=[(p[i+1]-p[i])%337 for i in range(335)]; print(Counter(d2).most_common(5))
print(pt[:60]); print(p[:20])
