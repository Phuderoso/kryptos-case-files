"""Cycle 10 (B): Bean's Gromark lead, reproduced independently and pushed to alphabet recovery.
Model (ACA Gromark, Hall 1969): key digits k_i from a 5-digit primer by lagged Fibonacci mod 10;
   ciphertext c_i = CA[(PA^-1(p_i) + k_i) mod 26]   (PA plain alphabet, CA cipher alphabet).
Unknown alphabets -> constraint graph: nodes plain letters u_p and cipher letters v_c with v_c - u_p = k_i (mod 26);
feasible iff no cycle contradiction and no two same-side letters forced to the same value inside a component.
Run: python3 tools/gromark_alphabet.py [control]"""
import sys, itertools, json, math
import numpy as np
sys.path.insert(0, "tools")
from kryptos_text import K4
from k4_anneal import AZ, KA, KN
N = 97; CR = sorted(KN.items())

def keys(b=10, L=5, n=N):
    prim = np.array(list(itertools.product(range(b), repeat=L)), dtype=np.int16)
    K = np.zeros((len(prim), n), dtype=np.int16); K[:, :L] = prim
    for t in range(L, n): K[:, t] = (K[:, t - L] + K[:, t - L + 1]) % b
    return prim, K

def feasible(CT, k, plain_fixed=None):
    """returns (ok, partial) ; partial = dict of relative positions per component."""
    par = {}; off = {}          # union-find with offsets: value(node) = value(root) + off[node]
    def find(x):
        if par.setdefault(x, x) == x: off.setdefault(x, 0); return x
        r = find(par[x]); off[x] = (off[x] + off[par[x]]) % 26; par[x] = r; return r
    def union(a, b, d):         # value(b) - value(a) = d
        ra, rb = find(a), find(b)
        if ra == rb: return (off[b] - off[a]) % 26 == d % 26
        par[rb] = ra; off[rb] = (off[a] + d - off[b]) % 26; return True
    if plain_fixed is not None:     # anchor: all plain letters relative to a common node "0"
        for p in set(p for _, p in CR): 
            if not union("0", "p" + p, plain_fixed.index(p)): return False, None
    for (i, p), kk in zip(CR, k):
        if not union("p" + p, "c" + CT[i], int(kk)): return False, None
    seen = {}
    for x in list(par):
        if x == "0": continue
        r = find(x); key = (r, x[0], off[x])
        if key in seen and seen[key] != x: return False, None
        seen[key] = x
    comps = {}
    for x in par:
        if x != "0": comps.setdefault(find(x), []).append((off[x], x))
    return True, comps

def scan(CT, plain_fixed=None):
    prim, K = keys(); hits = []
    for idx in range(len(prim)):
        ok, comps = feasible(CT, K[idx, [i for i, _ in CR]], plain_fixed)
        if ok: hits.append(("".join(map(str, prim[idx])), comps))
    return hits

def ca_from(comps):
    """With PA = AZ anchored at node '0', cipher letters get absolute CA positions."""
    ca = ["."] * 26
    for r, members in comps.items():
        base = dict((x, o) for o, x in members)
        if "0" in [x for _, x in members] or any(x == "0" for _, x in members): pass
    return ca

def keyed(w, alpha=AZ):
    s = []
    for ch in w + alpha:
        if ch not in s: s.append(ch)
    return "".join(s)
def aca_columnar(w):
    """ACA Gromark-style mixed alphabet: keyword-keyed alphabet written in rows under the keyword (no repeats),
    columns read in alphabetical order of the keyword letters."""
    kw = "".join(dict.fromkeys(w)); rows = keyed(kw)
    cols = [rows[j::len(kw)] for j in range(len(kw))]
    return "".join(c for _, c in sorted(zip(kw, cols)))

if __name__ == "__main__":
    CT = K4
    if len(sys.argv) > 1 and sys.argv[1] == "control":
        eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKE"[:N]
        pt = list(eng)
        for i, ch in KN.items(): pt[i] = ch
        prim, K = keys(); CA = aca_columnar("SHADOW"); kk = K[27182]
        CT = "".join(CA[(AZ.index(p) + int(kk[i])) % 26] for i, p in enumerate(pt))
        print("CONTROL planted primer", "".join(map(str, prim[27182])), "CA=aca_columnar(SHADOW)=", CA)
    gen = scan(CT); fixed = scan(CT, AZ)
    print(f"primers (base 10, length 5) feasible with ANY plain+cipher alphabets: {len(gen)}")
    print(f"primers feasible with plain = A-Z (ACA standard), any cipher alphabet: {len(fixed)}")
    out = {"general": [h for h, _ in gen], "plainAZ": []}
    for h, comps in fixed:
        anchor = [c for c in comps.values() if any(x == "p" + "A" or x.startswith("p") for _, x in c)]
        # absolute CA positions: in the component containing plain letters, value(pX)=AZ.index(X)
        ca = ["."] * 26
        for members in comps.values():
            pl = [(o, x) for o, x in members if x.startswith("p")]
            if not pl: continue
            o0, x0 = pl[0]; shift = (AZ.index(x0[1]) - o0) % 26
            for o, x in members:
                if x.startswith("c"): ca[(o + shift) % 26] = x[1]
        out["plainAZ"].append((h, "".join(ca)))
        print(f"  primer {h}: partial CA = {''.join(ca)}")
    if len(sys.argv) == 1: json.dump(out, open("analysis/gromark_feasible.json", "w"), indent=1)
