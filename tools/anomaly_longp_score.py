"""Cycle 24: English check of every crib-consistent configuration at periods 19-22 (where the crib test alone has no
power), K4 vs shuffled nulls vs a planted control with a 21-letter key. Decrypts the full text and scores quadgrams."""
import sys, random, subprocess
from kryptos_text import K4
import anomaly_controls as ac
sys.argv = ['x', '/dev/null', '97', 'none']; exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'anomaly_decode.py')).read())
N = {"none": 97, "chg": 97, "del": 98, "ins": 96}
def best(text, model, pmin=19, pmax=22):
    out = subprocess.run(["./anomaly_periodic", f"perms{N[model]}.bin", str(N[model]), model, text, str(pmax), str(pmax)],
                         capture_output=True, text=True).stdout.split("\n")
    hits = [l for l in out if l.startswith("HIT") and int(l.split("p=")[1].split()[0]) >= pmin]
    global K4
    sc = []
    for l in hits:
        K4save = K4; globals()['K4'] = text
        s = decode(l, N[model], model); globals()['K4'] = K4save
        sc.append((score(s)[0], s, l))
    sc.sort(reverse=True); return len(hits), sc[:3]
def show(tag, text, model):
    n, top = best(text, model)
    print(f"{tag} model={model} hits(p19-22)={n} best=" + (f"{top[0][0]:.2f} {top[0][1]}" if top else "none"), flush=True)
if __name__ == "__main__":   # K4, 3 shuffled nulls, 3 planted controls with a 21-letter key (see case file 23)
    import random, anomaly_controls as ac
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for m in ("none", "chg", "del", "ins"): show("K4", K4, m)
    for seed in (1, 2, 3):
        l = list(K4); random.Random(seed).shuffle(l); s = "".join(l)
        for m in ("none", "chg", "del", "ins"): show(f"NULL{seed}", s, m)
    for seed, (model, n) in enumerate([("del", 98), ("ins", 96), ("chg", 97)]):
        r = random.Random(500 + seed); P = ac.perms(n); t = r.randrange(len(P)); perm = P[t]; pt = ac.plain(n)
        key = [r.randrange(26) for _ in range(21)]; Cp = [None] * n
        for j in range(n): Cp[perm[j]] = AZ[(AZ.index(pt[j]) + key[j % 21]) % 26]
        Cp = "".join(Cp)
        if model == "del": d = r.randrange(98); carved = Cp[:d] + Cp[d+1:]
        elif model == "ins": d = r.randrange(97); carved = Cp[:d] + "Q" + Cp[d:]
        else: d = int(perm[30]); carved = Cp[:d] + ("A" if Cp[d] != "A" else "B") + Cp[d+1:]
        print(f"CONTROL t={t} d={d} key-period 21 AZ vig idx=pt"); show("CONTROL", carved, model)
