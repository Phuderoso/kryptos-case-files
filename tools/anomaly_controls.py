"""Cycle 24: planted positive controls and shuffled-K4 nulls for anomaly_periodic.c.
Each control: English plaintext with the cribs at the official positions, periodic key word, KA/AZ tableau,
a transposition drawn from the cycle-19 family, then ONE carving anomaly (dropped / extra / changed letter)."""
import sys, random, subprocess, numpy as np
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = ("SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTH" + "BERLINCLOCK"
        + "STRIKEATDUSKWHILEWEWAITEDXQ")
def plain(n): return BASE[:n]
def perms(n): return np.fromfile(f"perms{n}.bin", dtype=np.int16).reshape(-1, n)
def make(seed, model):
    r = random.Random(seed); n = {"del": 98, "ins": 96, "chg": 97}[model]
    P = perms(n); t = r.randrange(len(P)); perm = P[t]; pt = plain(n)
    PA = r.choice([AZ, KA]); CA = r.choice([AZ, KA]); mode = r.choice(["vig", "beau", "var"])
    key = r.choice(["LAYER", "CLOCK", "SHADOW", "BERLIN", "ABSCISSA", "PALIMPSEST", "LODESTONE", "NORTHEAST"])
    kv = [KA.index(ch) if PA == KA else AZ.index(ch) for ch in key]   # key letters read in the plain alphabet
    ix = r.choice(["pt", "ct"]); Cp = [None]*n
    for j in range(n):
        k = kv[(j if ix == "pt" else perm[j]) % len(key)]; p = PA.index(pt[j])
        c = {"vig": p + k, "var": p - k, "beau": k - p}[mode] % 26; Cp[perm[j]] = CA[c]
    Cp = "".join(Cp)
    if model == "del": d = r.randrange(98); carved = Cp[:d] + Cp[d+1:]
    elif model == "ins": d = r.randrange(97); carved = Cp[:d] + r.choice(AZ) + Cp[d:]
    else:
        ci = [21+i for i in range(13)] + [63+i for i in range(11)]; d = r.randrange(24); pos = int(perm[ci[d]])
        carved = Cp[:pos] + r.choice([x for x in AZ if x != Cp[pos]]) + Cp[pos+1:]
    assert len(carved) == 97
    return carved, dict(model=model, t=t, d=d, PA="KA" if PA == KA else "AZ", CA="KA" if CA == KA else "AZ",
                        mode=mode, key=key, idx=ix, p=len(key))
def run(text, model, pprint=14):
    n = {"del": 98, "ins": 96, "chg": 97, "none": 97}[model]
    out = subprocess.run(["./anomaly_periodic", f"perms{n}.bin", str(n), model, text, "26", str(pprint)],
                         capture_output=True, text=True).stdout.strip().split("\n")
    return [l for l in out if l.startswith("HIT")], out[-1]
def swap_control():
    """Cycle-24 swap control (run inline in the cycle): KA Quagmire III key SHADOW, then two adjacent carved letters swapped."""
    from kryptos_text import KA
    P = perms(97); r = random.Random(77); t = r.randrange(len(P)); perm = P[t]; pt = plain(97); key = "SHADOW"; C = [None]*97
    for j in range(97): C[perm[j]] = KA[(KA.index(pt[j]) + KA.index(key[j % 6])) % 26]
    d = int(perm[25]); C[d], C[d+1] = C[d+1], C[d]; C = "".join(C)
    out = subprocess.run(["./anomaly_periodic", "perms97.bin", "97", "swp", C, "26", "18"], capture_output=True, text=True).stdout.split("\n")
    print("SWAP CONTROL t=%d d=%d: hits at true (t,d)=%d" % (t, d, sum(f"t={t} d={d} " in l for l in out)))
if __name__ == "__main__":
    what = sys.argv[1]
    if what == "swap": swap_control(); sys.exit()
    if what == "controls":
        for model in ("del", "ins", "chg"):
            for seed in (1, 2, 3):
                carved, truth = make(seed * 10 + len(model), model)
                hits, hist = run(carved, model)
                ok = [h for h in hits if f"t={truth['t']} " in h and f"d={truth['d']} " in h]
                print("CONTROL", truth, "\n  carved", carved, f"\n  hits(p<=14)={len(hits)} at true (t,d)={len(ok)}")
                for h in hits[:6]: print("   ", h)
                print("  ", hist)
    else:
        for seed in range(1, 6):
            l = list(K4); random.Random(seed).shuffle(l); s = "".join(l)
            for model in ("none", "chg", "del", "ins"):
                hits, hist = run(s, model); print(f"NULL seed={seed} {model} hits(p<=14)={len(hits)}  {hist}")
