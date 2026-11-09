"""Cycle 171 control checks + string-level decryption (no code from porta171.c / bookrk1e.c).
porta  : verify171.py porta ctl/plants.txt      -> planted (slot, ordering, V, model, L | RK t0) present in ctl/ctlN.out?
         single-error plants must be found; two-error plants (ctl10, ctl11) must be absent at the planted cell.
         For periodic finds the key is rebuilt from the 23 crib pairs other than the error and all 97 letters decrypted.
bank   : verify171.py bank ctl171b/planted.txt  -> FIT23 miss / FULL / ABSENT as expected in ctl171b/NAME.out
decode : verify171.py decode CT perms.bin OUT... -> string-level periodic decryptions of FIT lines (L <= 23)"""
import sys, re, numpy as np
from collections import Counter
C1, C2 = "EASTNORTHEAST", "BERLINCLOCK"; CP = list(range(21, 34)) + list(range(63, 74)); CL = C1 + C2
PLANT = ("THEYCAMEATDAWNANDSTOOD" + C1 + "OFTHEOLDSTONEWALLWHEREWESAWTHE" + C2 + "SHININGINTHEEMPTYSQUARETONIGHTX")
PLANT = (PLANT[:21] + C1 + PLANT[34:63] + C2 + PLANT[74:])[:97]
def kval(p, c, o, var):
    ip, ic = o.index(p), o.index(c)
    if (ip < 13) == (ic < 13): return None
    h1, h2 = (ip, ic - 13) if ip < 13 else (ic, ip - 13)
    return (h2 - h1) % 13 if var == 1 else (h2 + h1) % 13
def porta(ch, o, k, var):
    i = o.index(ch)
    if i < 13: return o[13 + ((i + k) % 13 if var == 1 else (k - i) % 13)]
    h = i - 13; return o[(h - k) % 13 if var == 1 else (k - h) % 13]
def per_decrypt(ct, perm, o, var, model, L):
    """majority key per residue over the crib pairs (one dissent allowed overall); returns pt, key, dissenting crib index"""
    cls = {}
    for i, (j, p) in enumerate(zip(CP, CL)):
        idx = j if model == 'A' else perm[j]; k = kval(p, ct[perm[j]], o, var); cls.setdefault(idx % L, []).append((k, i))
    key = {}; bad = []
    for r, lst in cls.items():
        mc = Counter(k for k, _ in lst if k is not None).most_common(1)
        key[r] = mc[0][0] if mc else None; bad += [i for k, i in lst if k != key[r]]
    if len(bad) > 1: return None, None, bad
    pt = ''.join(porta(ct[perm[j]], o, key[(j if model == 'A' else perm[j]) % L], var) if key.get((j if model == 'A' else perm[j]) % L) is not None else '?' for j in range(97))
    return pt, [key.get(r, '?') for r in range(L)], bad
def parse(line):
    m = re.match(r"FIT perm (\d+) ord (\d+) src_alpha (\d+) split (\w) d (-?\d+) (\w+) per (.*?) rk (\d+)(.*)", line)
    per = {}
    for part in m.group(7).split():
        tag, Ls = part.split(':'); per[tag] = [int(x) for x in Ls.split(',') if x]
    return dict(perm=int(m.group(1)), d=int(m.group(5)), o=m.group(6), per=per, nrk=int(m.group(8)), rk=m.group(9).split())
mode = sys.argv[1]
if mode == 'porta':
    ok = n = 0
    for line in open(sys.argv[2]):
        f = line.split(); name = f[0]; slot = int(f[4]); o = f[10]; var = int(f[11][1]); model = f[12]; kind = f[13]; ct = f[-1]
        nerr = int(f[f.index('errors') + 1]); n += 1
        P = np.fromfile(f'ctl/{name}_slice.bin', dtype=np.int16).reshape(-1, 97); perm = [int(x) for x in P[slot]]
        hits = [parse(l) for l in open(f'ctl/{name}.out') if l.startswith('FIT')]
        hits = [h for h in hits if h['perm'] == slot and h['o'] == o]; tag = f'V{var}{model}'
        found = False; msg = 'planted ordering not among one-error fits'
        for h in hits:
            if kind == 'per':
                L = int(f[14][1:])
                if L in h['per'][tag]:
                    pt, key, bad = per_decrypt(ct, perm, o, var, model, L)
                    agree = pt is not None and sum(a == b for a, b in zip(pt, PLANT) if a != '?'); unk = pt.count('?') if pt else -1
                    found = pt is not None and agree >= 96 - unk
                    msg = f"{tag} L{L} d={h['d']} key {key} dissent {bad} agree {agree}/{97-unk} -> {pt}"
            else:
                tn, t0 = f[15], f[16][1:]
                m = [r for r in h['rk'] if r.split(':')[1] == tn and r.split(':')[7] == 't' + t0 and r.split(':')[3] == f'V{var}' and r.split(':')[4] == model]
                if m: found = True; msg = f"RK {m}"
        good = found if nerr == 1 else not found
        ok += good; print(name, f"errors {nerr}", 'PASS' if good else 'FAIL', msg)
    print(f"porta controls {ok}/{n}")
elif mode == 'bank':
    ok = n = 0
    for line in open(sys.argv[2]):
        name = line.split(':')[0]; f = line.split(); slot, model, md, tn, o = f[4], f[6], f[8], f[10], f[12]; n += 1
        out = open(f'ctl171b/{name}.out').read().split('\n')
        key = f"perm={slot} model={model} mode={md} text={tn} offset={o}"
        full = [l for l in out if l.startswith('FULL') and key in l]; fit = [l for l in out if l.startswith('FIT23') and key in l]
        if 'expect FIT23' in line:
            mi = line.split('miss=')[1].split()[0]; good = not full and any(l.endswith(f"miss={mi}") for l in fit)
            if '(no visible change!)' in line: good = bool(full)
        elif 'expect FULL' in line: good = bool(full)
        else: good = not full and not fit
        summ = [l for l in out if l.startswith('SUMMARY')][0].split()[3:7]
        ok += good; print(name, 'PASS' if good else 'FAIL', 'FULL' if full else '', fit, ' '.join(summ))
    print(f"bank controls {ok}/{n}")
else:
    ct = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); LMAX = 23
    for fn in sys.argv[4:]:
        for l in open(fn):
            if not l.startswith('FIT'): continue
            h = parse(l); perm = [int(x) for x in P[h['perm']]]
            for tag, Ls in h['per'].items():
                for L in Ls:
                    if L > LMAX: continue
                    var, model = int(tag[1]), tag[2]
                    pt, key, bad = per_decrypt(ct, perm, h['o'], var, model, L)
                    print(f"{fn} perm {h['perm']} {h['o']} d {h['d']} {tag} L{L} key {key} dissent {bad} PT {pt}")
            for r in h['rk']: print(f"{fn} perm {h['perm']} {h['o']} d {h['d']} {r}")
