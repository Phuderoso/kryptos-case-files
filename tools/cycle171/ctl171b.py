"""Cycle 171 (I-091) one-error planted running-key controls behind the 165,065-perm bank (independent string-level encryptor;
same key/mode conventions as bookrk / ctl169.py: model A = key index j, carved position perm[j]; model B = carved position inv[c],
key index inv[c]; additive modes 0..23 = (type, plain-KA, cipher-KA, key-KA)).
  e0..e7 : one error at a crib position (even: wrong carved letter; odd: wrong crib letter re-encrypted)  -> FIT23 miss=index
  n0,n1  : one wrong carved letter at a non-crib position                                                -> FULL
  d0,d1  : two crib-position errors                                                                      -> planted config ABSENT
  s0,s1  : no error                                                                                      -> FULL
Each control: 200-perm slice of bank.bin with the planted perm at a random slot.
usage: ctl171b.py bank.bin texts.txt SEED   (writes ctl171b/)"""
import sys, os, random, numpy as np
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
T = dict(l.split() for l in open(sys.argv[2])); rnd = random.Random(int(sys.argv[3]))
CP = list(range(21, 34)) + list(range(63, 74))
PT = ("THEYCAMEATDAWNANDSTOOD" + "EASTNORTHEAST" + "OFTHEOLDSTONEWALLWHEREWESAWTHE" + "BERLINCLOCK" + "SHININGINTHEEMPTYSQUARETONIGHTX")
PT = (PT[:21] + "EASTNORTHEAST" + PT[34:63] + "BERLINCLOCK" + PT[74:])[:97]
def enc(p, k, md):
    ty, ap, ac, ak = md % 3, (md // 3) & 1, (md // 6) & 1, (md // 12) & 1
    kv = KA.index(k) if ak else ord(k) - 65; pp = KA.index(p) if ap else ord(p) - 65
    c = (pp + kv) % 26 if ty == 0 else (kv - pp) % 26 if ty == 1 else (pp - kv) % 26
    return KA[c] if ac else AZ[c]
os.makedirs("ctl171b", exist_ok=True); out = []
names = [n for n in T if len(T[n]) > 500]
kinds = [f"e{i}" for i in range(8)] + ["n0", "n1", "d0", "d1", "s0", "s1"]
for name in kinds:
    j = rnd.randrange(len(P)); perm = P[j]; inv = np.argsort(perm); model = rnd.choice("AB"); md = rnd.randrange(24)
    tn = rnd.choice(names); t = T[tn]; o = rnd.randrange(len(t) - 97)
    cpos = lambda c: int(perm[c]) if model == "A" else int(inv[c]); kidx = lambda c: o + (c if model == "A" else int(inv[c]))
    car = [None] * 97
    for c in range(97): car[cpos(c)] = enc(PT[c], t[kidx(c)], md)
    L = car[:]; info = ""
    if name[0] == "e":
        jj = rnd.randrange(24); c = CP[jj]
        if int(name[1:]) % 2 == 0: L[cpos(c)] = rnd.choice([x for x in AZ if x != car[cpos(c)]]); info = f"carved error crib_index {jj} expect FIT23 miss={jj}"
        else:
            newp = rnd.choice([x for x in AZ if x != PT[c]]); L[cpos(c)] = enc(newp, t[kidx(c)], md); info = f"crib error {PT[c]}->{newp} crib_index {jj} expect FIT23 miss={jj}"
            if L[cpos(c)] == car[cpos(c)]: info += " (no visible change!)"
    elif name[0] == "n":
        x = rnd.choice([x for x in range(97) if x not in {cpos(c) for c in CP}]); L[x] = rnd.choice([y for y in AZ if y != car[x]]); info = f"non-crib carved error pos {x} expect FULL"
    elif name[0] == "d":
        a, b = rnd.sample(range(24), 2)
        for jj in (a, b): q = cpos(CP[jj]); L[q] = rnd.choice([y for y in AZ if y != car[q]])
        info = f"errors crib_index {a},{b} expect ABSENT"
    else: info = "no error expect FULL"
    sl = [rnd.randrange(len(P)) for _ in range(200)]; slot = rnd.randrange(200); sl[slot] = j
    P[sl].tofile(f"ctl171b/{name}_slice.bin"); open(f"ctl171b/{name}.txt", "w").write("".join(L) + "\n")
    out.append(f"{name}: bankperm {j} slot {slot} model {model} mode {md} text {tn} offset {o} {info}")
open("ctl171b/planted.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
