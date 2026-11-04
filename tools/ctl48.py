import random
from grille_sat import encrypt, CRIBS, KA, AZ, K4
random.seed(48)
def pt():
    p = [random.choice(AZ) for _ in range(97)]
    for j, ch in CRIBS.items(): p[j] = ch
    return "".join(p)
plants = [("pt", KA, "vig", "PALIM", "KA"), ("ct", AZ, "beau", "QX", "AZ"), ("pt", AZ, "vig", "K", "AZ")]
for n, (side, al, mode, key, tn) in enumerate(plants):
    o = [random.randrange(4) for _ in range(25)]
    c = encrypt(pt(), o, "B", side, al, mode, key)
    open(f"ctlB_{n}.txt", "w").write(c); print(n, side, tn, mode, key, "".join(map(str, o)))
for n in range(3):
    s = list(K4); random.shuffle(s); open(f"nullB_{n}.txt", "w").write("".join(s))
