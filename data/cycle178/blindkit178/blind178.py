"""I-106 blind kit (cycle 178): six ciphertexts behind rows of all.bin; four are linear-recurrence keys mod 26 (the cycle-178
family), two are decoys. Writes the public kit (ciphertexts + SHA-256 of "id|answer", answer = plaintext positions 21-96 (76 letters) or NONE) and a PRIVATE answer
file that stays on the box. usage: blind178.py all.bin seeds178.txt public_dir private_json   (seed 17890)"""
import sys, json, random, hashlib, os
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); words = open(sys.argv[2]).read().split()
pub, priv = sys.argv[3], sys.argv[4]; os.makedirs(pub, exist_ok=True); R = random.Random(17890)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
def fit(s, n): s = "".join(ch for ch in s.upper() if ch.isalpha()); return (s + "X" * n)[:n]
TX = [("THE WATER BEYOND THE GATE", "WAS COLD AND THE BOATMEN WAITED FOR", "AT THE HOUR OF THE FIRST BELL"),
      ("NOBODY READ THE LETTER", "UNTIL THE LAMP HAD BURNED DOWN TO A", "SO THE MESSAGE STAYED SHUT"),
      ("A SMALL BOX OF SALT WAS", "BURIED UNDER THE THIRD STONE FROM THE", "WHERE THE ROADS CROSS TWICE"),
      ("FOUR MEN CARRIED THE MAP", "THROUGH THE SNOW AND LEFT IT AT THE", "STATION WITH THE GREEN DOOR"),
      ("HER LAST NOTE SAID GO", "AND THEN THE LINE WENT QUIET UNTIL", "THE RAIN STOPPED AT DAWN"),
      ("THE KEEPER COUNTED SHEEP", "TWICE AND STILL FOUND ONE TOO MANY AT", "BEFORE HE LOCKED THE PEN")]
def pt(i): a, b, c = TX[i]; return fit(a, 21) + "EASTNORTHEAST" + fit(b, 29) + "BERLINCLOCK" + fit(c, 23)
def ks(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def enc(p, k, al, form): i = al.index(p); return al[(i + k) % 26] if form == "vig" else al[(k - i) % 26]
def build(p, k, al, form, q, ix):
    S = P[q]; C = ["?"] * 97
    for i in range(97): C[S[i]] = enc(p[i], k[i] if ix == 0 else k[S[i]], al, form)
    return "".join(C)
rc = lambda L: [R.randrange(26) for _ in range(L)]
spec = []
w = R.choice([x for x in words if len(x) >= 8])
cfgs = [("pos", 0, 4, "ka", "beau", rc(4), R.randrange(26), rc(4)),
        ("pos", 1, 3, "az", "vig", rc(3), R.randrange(26), rc(3)),
        ("pos", 1, 8, "ka", "vig", [R.randrange(2) for _ in range(7)] + [1], R.randrange(26), [AZ.index(x) for x in w[:8]]),
        ("pos", 0, 7, "az", "vig", rc(7), R.randrange(26), rc(7)),
        ("decoy", 0, 0, "az", "vig", None, None, None),
        ("decoy", 1, 0, "ka", "beau", None, None, None)]
order = list(range(6)); R.shuffle(order)
for slot, ci in enumerate(order):
    kind, ix, L, pa, form, c, d, seed = cfgs[ci]; q = R.randrange(P.shape[0]); p = pt(ci); al = KA if pa == "ka" else AZ
    k = ks(c, d, seed) if kind == "pos" else [R.randrange(26) for _ in range(97)]
    ct = build(p, k, al, form, q, ix)
    ans = p[21:] if kind == "pos" else "NONE"     # positions 21-96: what every fit determines (0-20 need an invertible c_L)
    spec.append(dict(id=f"B{slot+1}", ct=ct, kind=kind, ix=ix, L=L, pa=pa, form=form, c=c, d=d, seed=seed, q=q, pt=p,
                     seedword=(w if ci == 2 else None), sha256=hashlib.sha256(f"B{slot+1}|{ans}".encode()).hexdigest()))
json.dump(spec, open(priv, "w"), indent=1)
with open(f"{pub}/kit178.txt", "w") as o:
    for s in spec: o.write(f"{s['id']} {s['ct']} sha256(id|answer)={s['sha256']}\n")
    o.write(f"commitment sha256(private answers file)={hashlib.sha256(open(priv,'rb').read()).hexdigest()}\n")
print(open(f"{pub}/kit178.txt").read())
