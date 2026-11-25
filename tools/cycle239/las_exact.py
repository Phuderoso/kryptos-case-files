"""Cycle 237 (I-367): exact look-and-say term lengths (OEIS A005341) without truncation, via audioactive atoms (Conway).
Atoms are DERIVED here (not copied): split term strings at cut points where k-step evolutions never interact, then validated
against direct computation (n<=45) and the OEIS b-file (n<=3000). Provides las_len(n), n>=1 (term 1 = '1')."""
import sys
def ev(s):
    out = []; i = 0; n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]: j += 1
        out.append(str(j - i) + s[i]); i = j
    return ''.join(out)
def evk(s, k):
    for _ in range(k): s = ev(s)
    return s
def split_atom(s, K=9):
    full = evk(s, K) if len(s) < 3000 else None
    for p in range(1, len(s)):
        l, r = s[:p], s[p:]
        if full is None: raise SystemExit('term too long to split')
        if evk(l, K) + evk(r, K) == full:
            return split_atom(l, K) + split_atom(r, K)
    return [s]
def build(n0=16):
    s = '1'
    for _ in range(n0 - 1): s = ev(s)
    atoms = {}   # string -> index
    queue = split_atom(s)
    todo = list(queue)
    while todo:
        a = todo.pop()
        if a in atoms: continue
        atoms[a] = len(atoms)
        for b in split_atom(ev(a)):
            if b not in atoms: todo.append(b)
    names = list(atoms)
    dec = [[atoms[b] for b in split_atom(ev(a))] for a in names]
    init = {}
    for a in queue: init[atoms[a]] = init.get(atoms[a], 0) + 1
    return names, dec, init, n0
NAMES, DEC, INIT, N0 = build()
LEN = [len(a) for a in NAMES]
def las_len(n):
    """length of term n (n>=1)."""
    if n <= N0 + 2:
        s = '1'
        for _ in range(n - 1): s = ev(s)
        return len(s)
    cnt = dict(INIT)
    for _ in range(n - N0):
        new = {}
        for a, c in cnt.items():
            for b in DEC[a]: new[b] = new.get(b, 0) + c
        cnt = new
    return sum(c * LEN[a] for a, c in cnt.items())
if __name__ == '__main__':
    print('atoms', len(NAMES), 'n0', N0)
    ref = {}
    for ln in open("b005341.txt"):
        if ln.startswith('#') or not ln.strip(): continue
        a, b = ln.split(); ref[int(a)] = int(b)
    # direct check n<=45
    s = '1'
    for n in range(1, 46):
        assert len(s) == las_len(n) == ref[n], n
        s = ev(s)
    cnt = dict(INIT); bad = []
    for n in range(N0, max(ref) + 1):
        if n > N0:
            new = {}
            for a, c in cnt.items():
                for b in DEC[a]: new[b] = new.get(b, 0) + c
            cnt = new
        if sum(c * LEN[a] for a, c in cnt.items()) != ref[n]: bad.append(n)
    print('OEIS terms', len(ref), 'mismatches', len(bad), bad[:5])
