"""Cycle 170 string-level verifier (no bitsets, no code from porta170.c).
ctl  : python3 verify170.py ctl  plants.txt  -> for each control find the planted (slot, ordering, variant, model, L / RK) line in ctl/ctlN.out,
       rebuild the key from the crib letters alone, decrypt all 97 letters and compare with the planted plaintext.
decode: python3 verify170.py decode CT perms.bin OUTFILE... -> for every SURV line with a periodic fit, rebuild key, decrypt, print."""
import sys, re, numpy as np
C1, C2 = "EASTNORTHEAST", "BERLINCLOCK"; CP = list(range(21, 34)) + list(range(63, 74)); CL = C1 + C2
def kval(p, c, o, var):
    ip, ic = o.index(p), o.index(c)
    if (ip < 13) == (ic < 13): return None
    h1, h2 = (ip, ic - 13) if ip < 13 else (ic, ip - 13)
    return (h2 - h1) % 13 if var == 1 else (h2 + h1) % 13
def porta(ch, o, k, var):
    i = o.index(ch)
    if i < 13: return o[13 + ((i + k) % 13 if var == 1 else (k - i) % 13)]
    h = i - 13; return o[(h - k) % 13 if var == 1 else (k - h) % 13]
def periodic_decrypt(ct, perm, o, var, model, L):
    key = {}
    for j, p in zip(CP, CL):
        idx = j if model == 'A' else perm[j]; k = kval(p, ct[perm[j]], o, var)
        if k is None or key.setdefault(idx % L, k) != k: return None, None
    out = ''.join(porta(ct[perm[j]], o, key[(j if model == 'A' else perm[j]) % L], var) if (j if model == 'A' else perm[j]) % L in key else '?' for j in range(97))
    return out, [key.get(r, '?') for r in range(L)]
def parse(line):
    m = re.match(r"SURV perm (\d+) ord (\d+) src_alpha (\d+) split (\w) minL (\d+) (\w+) per (.*?) rk (\d+)(.*)", line)
    per = {}
    for part in m.group(7).split():
        tag, Ls = part.split(':'); per[tag] = [int(x) for x in Ls.split(',') if x]
    return dict(perm=int(m.group(1)), o=m.group(6), per=per, nrk=int(m.group(8)), rk=m.group(9).split())
PLANT = ("THEYCAMEATDAWNANDSTOOD" + "EASTNORTHEAST" + "OFTHEOLDSTONEWALLWHEREWESAWTHE" + "BERLINCLOCK" + "SHININGINTHEEMPTYSQUARETONIGHTX")
PLANT = (PLANT[:21] + C1 + PLANT[34:63] + C2 + PLANT[74:])[:97]
if sys.argv[1] == 'ctl':
    PT = None; ok = 0; n = 0
    for line in open(sys.argv[2]):
        f = line.split(); name = f[0]; slot = int(f[4]); o = f[10]; var = int(f[11][1]); model = f[12]; kind = f[13]; ct = f[-1]; n += 1
        P = np.fromfile(f'ctl/{name}_slice.bin', dtype=np.int16).reshape(-1, 97); perm = [int(x) for x in P[slot]]
        hits = [parse(l) for l in open(f'ctl/{name}.out') if l.startswith('SURV')]
        hits = [h for h in hits if h['perm'] == slot and h['o'] == o]
        good = False; msg = 'planted ordering not among survivors'
        if hits:
            h = hits[0]
            if kind == 'per':
                L = int(f[14][1:]); tag = f'V{var}{model}'
                if L in h['per'][tag]:
                    pt, key = periodic_decrypt(ct, perm, o, var, model, L)
                    good = pt is not None and all(a == '?' or a == b for a, b in zip(pt, PLANT)); unk = pt.count('?') if pt else -1
                    msg = f"{tag} L{L} key {key} unknown-letters {unk} match-plant {good} -> {pt}"
                else: msg = f"{tag} periods {h['per'][tag]} lack L{L}"
            else:
                tn, t0 = f[15], f[16][1:]
                m = [r for r in h['rk'] if r.split(':')[1] == tn and r.endswith(':t' + t0) and r.split(':')[3] == f'V{var}' and r.split(':')[4] == model]
                good = bool(m); msg = f"RK lines {m} (all: {h['rk']})"
        ok += good; print(name, 'PASS' if good else 'FAIL', msg)
    print(f"controls {ok}/{n}")
else:
    ct = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97)
    for fn in sys.argv[4:]:
        for l in open(fn):
            if not l.startswith('SURV'): continue
            h = parse(l); perm = [int(x) for x in P[h['perm']]]
            for tag, Ls in h['per'].items():
                for L in Ls:
                    var, model = int(tag[1]), tag[2]
                    res = sorted({(j if model == 'A' else perm[j]) % L for j in CP}); nchk = 24 - len(res)
                    pt, key = periodic_decrypt(ct, perm, o := h['o'], var, model, L)
                    print(f"perm {h['perm']} {o} {tag} L{L} checks {nchk} key {key} PT {pt}")
