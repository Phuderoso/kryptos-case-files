"""PREREG244 T2: NOT TESTABLE rule for one-error gates (C130, credit Voynich). kb227 conventions: crib seat j sits in key class
S[POS[j]] mod p (S = bank / all.bin row, dir 0 = row, dir 1 = its inverse; direct = identity). Class size n_c = number of the 24 crib seats
in that class. One-error plant: PENDANT n_c 1, TIE n_c 2, MAJ n_c >= 3; (layout, p) NOT TESTABLE for one-error correction iff no seat
has n_c >= 3. Applied to the one-error plants of case 215 (cycle 229) and case 218 (cycle 232); census over all layouts, p 8-24.
usage: seat244.py REPO > seat244.txt   (dir with bank.bin, all.bin)"""
import sys, json, numpy as np
R = sys.argv[1]; N = 97; POS = np.array(list(range(21, 34)) + list(range(63, 74)))
B = {'bank': np.fromfile('bank.bin', dtype=np.int16).reshape(-1, N), 'all': np.fromfile('all.bin', dtype=np.int16).reshape(-1, N)}
def seats(scope, row, d):
    if scope == 'direct': return POS.copy()
    perm = B[scope][row].astype(int)
    if d == 0: return perm[POS]
    inv = np.empty(N, int); inv[perm] = np.arange(N); return inv[POS]
def label(s, p, bad):
    cl = s % p; sz = np.array([np.sum(cl == c) for c in cl])
    lay = 'TESTABLE' if sz.max() >= 3 else 'NOT TESTABLE'
    nb = sz[bad]; st = 'PENDANT' if nb == 1 else 'TIE' if nb == 2 else 'MAJ'
    return st, lay, int(nb), int(sz.max()), int((sz >= 3).sum())
for cyc, case, key in ((229, 215, 'P'), (232, 218, 'pass_ref')):
    S = json.load(open(R + f'/data/cycle{cyc}/summary{cyc}.json'))['plants']; rec = {d['pid']: d for d in S}
    rows = [l.rstrip('\n').split('\t') for l in open(R + f'/data/cycle{cyc}/plants{cyc}.tsv')][1:]
    print(f'## case {case} (cycle {cyc}) one-error plants: pid scope row dir p bad-seat | stratum n_c | layout (max n_c, #MAJ seats) | recovered, gate')
    tally = {}
    for r in rows:
        pid, scope, row, d, p, bad = int(r[0]), r[1], int(r[2]), int(r[3]), int(r[4]), int(r[8])
        if bad < 0: continue
        st, lay, nb, mx, nmaj = label(seats(scope, row, d), p, bad)
        g = rec[pid]; ok = bool(g.get(key)) and bool(g.get('recovered', True))
        tally.setdefault((st, lay), []).append(ok)
        print(f'  {pid:2d} {scope:4s} {row:6d} {d} p {p:2d} seat {bad:2d} | {st:7s} {nb} | {lay:12s} ({mx}, {nmaj}) | rec {g.get("recovered")}, gate {"pass" if ok else "MISS"}')
    for k, v in sorted(tally.items()): print(f'  stratum {k[0]:7s} layout {k[1]:12s}: {sum(v)}/{len(v)}')
    tl = [ok for (st, lay), v in tally.items() for ok in v if lay == 'TESTABLE']
    print(f'  pooled one-error {sum(sum(v) for v in tally.values())}/{sum(len(v) for v in tally.values())}; on TESTABLE layouts {sum(tl)}/{len(tl)}')
print('## census: fraction of layouts with >= 1 MAJ seat (n_c >= 3); mean #seats in classes of size 1 / 2 / >=3')
for scope in ('direct', 'bank', 'all'):
    if scope == 'direct': L = POS[None, :]
    else:
        P = B[scope].astype(np.int32); inv = np.argsort(P, axis=1)
        L = np.concatenate([P[:, POS], inv[:, POS]])
    out = []
    for p in range(8, 25):
        cl = L % p
        sz = (cl[:, :, None] == cl[:, None, :]).sum(2)
        fr = (sz.max(1) >= 3).mean(); m1, m2, m3 = (sz == 1).sum(1).mean(), (sz == 2).sum(1).mean(), (sz >= 3).sum(1).mean()
        out.append(f'p{p}:{fr:.3f}')
        print(f'  {scope:6s} layouts {len(L):7d} p {p:2d}: MAJ-available {fr:.4f}; seats in classes 1 / 2 / >=3: {m1:5.2f} / {m2:5.2f} / {m3:5.2f}')
