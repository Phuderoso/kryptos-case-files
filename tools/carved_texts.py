"""Cycle 34: build the 'already carved' running-key texts (letters only), forward and reversed."""
from kryptos_text import K1, K2, K3, KA
from solve_k1_k2_k3 import vig_dec, k3_dec
L = lambda s: "".join(c for c in s if c.isalpha())
k2fix = K2[:-8] + "S" + K2[-8:]
P1, P2c, P2f, P3 = L(vig_dec(K1, "PALIMPSEST")), L(vig_dec(K2, "ABSCISSA")), L(vig_dec(k2fix, "ABSCISSA")), L(k3_dec(K3))
K0 = "VIRTUALLYINVISIBLEDIGETALINTERPRETATITSHADOWFORCESLUCIDMEMORYTISYOURPOSITIONSOSRQ"  # same string as cycle 2
tab = "".join(KA[i:] + KA[:i] for i in range(26))          # KA tableau body, row by row

texts = {
 "K1pt": P1, "K2pt_carved": P2c, "K2pt_fixed": P2f, "K3pt": P3, "K123pt": P1 + P2f + P3,
 "K1ct": L(K1), "K2ct": L(K2), "K3ct": L(K3), "K123ct": L(K1 + K2 + K3), "K0morse": K0,
 "KAtableau_rows": tab,
 "K123pt_K0": K0 + P1 + P2f + P3,
}
with open("texts.txt", "w") as f:
    for n, t in texts.items():
        f.write(f"{n} {t}\n"); f.write(f"{n}_rev {t[::-1]}\n")
for n, t in texts.items(): print(n, len(t), t[:40])
