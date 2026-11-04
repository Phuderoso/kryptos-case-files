"""Cycle 47: turning grille 10x10, convention A (K3-like), exact search by crib decomposition.

Plaintext (97 letters) is written row-major into a 10x10 grid; cells 97-99 stay empty. A grille with 25 holes
(one per rotation orbit) is laid on it and rotated clockwise 4 times; at each rotation the letters under the holes
are read in row-major order (empty cells skipped). A periodic Vigenere/Beaufort key (A-Z or KRYPTOS numbering)
acts before ('pt': key index = plaintext position) or after ('ct': key index = ciphertext position) the transposition.

Cell c read in rotation r gets ciphertext index T(c) = 25r - E(<r) + #{c' < c read in rotation r}, where E(<r)
counts empty cells read before rotation r. So each crib block only needs: the rotation label of each crib cell and
one offset per label. We enumerate those exactly (lazy offsets, key-consistency pruning), join the two blocks, then
check by dynamic programming over the free orbits that a real grille realises the implied counts. Exact: nothing is
sampled. Usage: python3 grille_exact.py TEXTFILE|K4 SIDE TAB MODE L
"""
import sys, time
from grille_sat import K4, KA, AZ, CRIBS, WHERE, ORB, perm_from_choice, encrypt, N

B1 = list(range(21, 34)); B2 = list(range(63, 74))

def block_dfs(cells, Cv, Pv, L, side, mode, nmax):
    out = []
    def lo(r): return 25 * r - min(r, 3)
    def rec(i, lab, off, cnt, key, orb):
        if i == len(cells):
            out.append((dict(lab), dict(off), dict(key), dict(orb))); return
        c = cells[i]; k, q = WHERE[c]
        for r in range(4):
            o = (q - r) % 4
            if k in orb and orb[k] != o: continue
            if r in off: Ts = [off[r] + cnt[r]]
            else: Ts = range(lo(r), min(25 * r + nmax, N - 1) + 1)
            for T in Ts:
                if T >= N: continue
                idx = (c if side == "pt" else T) % L
                val = (Cv[T] - Pv[c]) % 26 if mode == "vig" else (Cv[T] + Pv[c]) % 26
                if key.get(idx, val) != val: continue
                newk = idx not in key; newo = k not in orb; newoff = r not in off
                if newk: key[idx] = val
                if newo: orb[k] = o
                if newoff: off[r] = T - cnt[r]
                lab[c] = r; cnt[r] += 1
                rec(i + 1, lab, off, cnt, key, orb)
                cnt[r] -= 1; del lab[c]
                if newk: del key[idx]
                if newo: del orb[k]
                if newoff: del off[r]
    rec(0, {}, {}, [0, 0, 0, 0], {}, {})
    return out

def feasible(orb, off1, off2):
    """Is there a grille consistent with fixed orbit choices whose counts give these offsets?"""
    for e97 in range(4):
        for e98 in range(4):
            for e99 in range(4):
                fix = dict(orb); ok = True
                for cell, r in ((97, e97), (98, e98), (99, e99)):
                    k, q = WHERE[cell]; o = (q - r) % 4
                    if fix.get(k, o) != o: ok = False; break
                    fix[k] = o
                if not ok: continue
                E = [e97, e98, e99]
                def Elt(r): return sum(1 for x in E if x < r)
                tgt = {}
                for r, A in off1.items(): tgt[("a", r)] = A - 25 * r + Elt(r)
                for r, Bv in off2.items(): tgt[("b", r)] = Bv - 25 * r + Elt(r)
                if any(v < 0 for v in tgt.values()): continue
                keys = list(tgt)
                def contrib(k, o):
                    v = [0] * len(keys)
                    for q, c in enumerate(ORB[k]):
                        r = (q - o) % 4
                        for n, (blk, rr) in enumerate(keys):
                            if rr == r and c < (21 if blk == "a" else 63): v[n] += 1
                    return v
                states = {tuple([0] * len(keys)): None}
                limit = [tgt[x] for x in keys]
                for k in range(25):
                    choices = [fix[k]] if k in fix else range(4)
                    ns = {}
                    for s, path in states.items():
                        for o in choices:
                            v = contrib(k, o); t = tuple(a + b for a, b in zip(s, v))
                            if all(a <= b for a, b in zip(t, limit)) and t not in ns:
                                ns[t] = (path, k, o)
                    states = ns
                    if not states: break
                if tuple(limit) in states:
                    # rebuild the grille
                    o = [0] * 25; node = states[tuple(limit)]
                    while node: node, k, ov = node; o[k] = ov
                    return o
    return None

def run(text, side, tab, mode, L, verbose=True):
    alpha = KA if tab == "KA" else AZ
    Cv = [alpha.index(ch) for ch in text]
    Pv = {j: alpha.index(ch) for j, ch in CRIBS.items()}
    t0 = time.time()
    s1 = block_dfs(B1, Cv, Pv, L, side, mode, 21)
    s2 = block_dfs(B2, Cv, Pv, L, side, mode, 25)
    hits, joins = [], 0
    # index s2 by orbit/key compatibility lazily
    for lab1, off1, key1, orb1 in s1:
        for lab2, off2, key2, orb2 in s2:
            if any(key1.get(i, v) != v for i, v in key2.items()): continue
            if any(orb1.get(k, v) != v for k, v in orb2.items()): continue
            joins += 1
            orb = dict(orb1); orb.update(orb2)
            # block-2 offsets count cells < 63; block-1 cells labelled r are among them, consistent automatically
            g = feasible(orb, off1, off2)
            if g is not None:
                tp = perm_from_choice(g, "A")
                ok = True; key = dict(key1); key.update(key2)
                for j, ch in CRIBS.items():
                    T = tp[j]; idx = (j if side == "pt" else T) % L
                    val = (Cv[T] - Pv[j]) % 26 if mode == "vig" else (Cv[T] + Pv[j]) % 26
                    if key.get(idx, val) != val: ok = False; break
                    key[idx] = val
                if ok: hits.append((g, key))
    dt = time.time() - t0
    return len(s1), len(s2), joins, hits, dt

if __name__ == "__main__":
    name, side, tab, mode, L = sys.argv[1:6]
    text = K4 if name == "K4" else open(name).read().strip()
    n1, n2, joins, hits, dt = run(text, side, tab, mode, int(L))
    alpha = KA if tab == "KA" else AZ
    print(f"{name} A {side} {tab} {mode} L={L} block1={n1} block2={n2} joins={joins} grilles={len(hits)} {dt:.1f}s", flush=True)
    for g, key in hits[:5]:
        print("  HIT grille", g, "key", "".join(alpha[key.get(i, 0)] if i in key else "?" for i in range(int(L))))
