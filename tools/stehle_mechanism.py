#!/usr/bin/env python3
"""Cycle 42: preregistered test of the Stehle lag-4 regularity in K4 (carved positions 55-63, 0-based,
c[i+4]-c[i] = 5 (mod 26, A-Z numbering) for i = 55..59).
T1  significance: narrow (lag 4, A-Z) and look-elsewhere-corrected (lags 1-24, A-Z and KRYPTOS numbering)
    longest run of equal consecutive lag-d differences, K4 vs shuffled K4 (same letters).
T2  English pass-through: under any additive key whose period divides 4 (or whose lag-4 difference is constant,
    e.g. a progressive period-4 key) the carved lag-4 differences equal the plaintext's (plus a constant), so the
    run would have to be in the plaintext. Rate of such runs in English vs shuffled English.
T3  crib-anchored: if the run is a property of the key, the key recovered at the 24 crib letters should show
    runs of equal lag-d differences more than chance. K4 vs shuffled-K4 nulls; Vigenere/Beaufort x A-Z/KRYPTOS.
T4  calibration: the same T1 statistic on K1, K2, K3 ciphertexts (known mechanisms)."""
import sys, re, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kryptos_text import K1, K2, K3, K4, KA
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rng = np.random.default_rng(42)
CRIBS = {21: 'EASTNORTHEAST', 63: 'BERLINCLOCK'}
PT = {}
for s, w in CRIBS.items():
    for j, ch in enumerate(w): PT[s + j] = ch

def num(t, al): return np.array([al.index(c) for c in t if c in al], dtype=np.int16)

def longest_run(x, lag):
    """x: (..., n) int array. Longest run (in differences) of equal consecutive lag-d differences, and its start."""
    d = (x[..., lag:] - x[..., :-lag]) % 26
    eq = d[..., 1:] == d[..., :-1]
    best = np.zeros(x.shape[:-1], dtype=np.int16); cur = np.zeros_like(best)
    for k in range(eq.shape[-1]):
        cur = np.where(eq[..., k], cur + 1, 0); best = np.maximum(best, cur)
    return best + 1  # number of equal differences in the run

def t1(text, nshuf, lags=range(1, 25), label='K4'):
    out = []
    xs = {nm: num(text, al) for nm, al in (('AZ', AZ), ('KA', KA))}
    obs4 = int(longest_run(xs['AZ'], 4))
    obsw = max(int(longest_run(xs[n], L)) for n in xs for L in lags)
    perm = np.argsort(rng.random((nshuf, len(xs['AZ']))), axis=1)
    sh4 = longest_run(xs['AZ'][perm], 4)
    shw = np.max([longest_run(xs[n][perm], L) for n in xs for L in lags], axis=0)
    p4 = (np.sum(sh4 >= obs4) + 1) / (nshuf + 1); pw = (np.sum(shw >= obsw) + 1) / (nshuf + 1)
    out.append(f'{label}: narrow (lag 4, A-Z) longest run = {obs4}; shuffles >= : p = {p4:.5f}')
    out.append(f'{label}: wide (lags 1-24, A-Z+KA) longest run = {obsw}; shuffles >= : p = {pw:.5f}'
               f'  (null run distribution: ' + ', '.join(f'{v}:{np.sum(shw==v)}' for v in sorted(set(shw.tolist()))) + ')')
    return out, obs4, obsw

def t2(nwin=200000):
    txt = ''
    for f in ('g84', 'g98', 'g1342', 'g1661', 'g2701'):
        raw = open(__file__.rsplit('/', 2)[0] + f'/data/{f}.txt', encoding='utf-8', errors='ignore').read()
        raw = raw[raw.find('*** START'):raw.find('*** END')]
        txt += re.sub('[^A-Z]', '', raw.upper())
    x = num(txt, AZ)
    starts = rng.integers(0, len(x) - 97, nwin)
    win = x[starts[:, None] + np.arange(97)]
    eng = longest_run(win, 4)
    shuf = longest_run(np.take_along_axis(win, np.argsort(rng.random(win.shape), axis=1), axis=1), 4)
    # constant-0 runs (repeated 4-letter block) are the only common English case; count separately
    d = (win[:, 4:] - win[:, :-4]) % 26
    out = [f'T2 English, {len(txt):,} letters, {nwin:,} random 97-letter windows, lag 4 A-Z:']
    for r in range(3, 8):
        out.append(f'  P(run >= {r}): English {np.mean(eng >= r):.5f}   shuffled English {np.mean(shuf >= r):.5f}')
    # where English produces runs >= 5, what is the constant?
    consts = {}
    for i in np.where(eng >= 5)[0][:2000]:
        dd = d[i]
        for k in range(len(dd) - 4):
            if np.all(dd[k:k + 5] == dd[k]): consts[int(dd[k])] = consts.get(int(dd[k]), 0) + 1; break
    out.append('  constants of English runs >= 5 (diff: count): ' + str(dict(sorted(consts.items()))))
    return out

def keystream(c, mode, al):
    k = {}
    for i, p in PT.items():
        ci, pi = al.index(c[i]), al.index(p)
        k[i] = (ci - pi) % 26 if mode == 'V' else (ci + pi) % 26
    return k

def known_key_run(c, mode, al, lags=range(1, 13)):
    k = keystream(c, mode, al); best = 0
    for L in lags:
        ds = {i: (k[i + L] - k[i]) % 26 for i in k if i + L in k}
        run = 1
        for i in sorted(ds):
            run = run + 1 if (i - 1 in ds and ds[i - 1] == ds[i]) else 1
            best = max(best, run)
    return best

def t3(nnull=20000):
    out = ['T3 crib-anchored key regularity (longest run of equal consecutive lag-d key differences, lags 1-12):']
    for mode in 'VB':
        for nm, al in (('AZ', AZ), ('KA', KA)):
            obs = known_key_run(K4, mode, al)
            nul = []
            for _ in range(nnull):
                s = list(K4); rng.shuffle(s); nul.append(known_key_run(''.join(s), mode, al))
            nul = np.array(nul)
            out.append(f'  {mode} {nm}: K4 {obs}; nulls >= : p = {(np.sum(nul >= obs) + 1) / (nnull + 1):.4f}; '
                       f'null dist ' + ', '.join(f'{v}:{np.sum(nul == v)}' for v in sorted(set(nul.tolist()))))
    return out

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    lines, o4, ow = t1(K4, N)
    print('\n'.join(lines))
    x = num(K4, AZ); print('K4 A-Z lag-4 diffs 52-62:', [int((x[i + 4] - x[i]) % 26) for i in range(52, 63)])
    for lab, t in (('K1', K1), ('K2', K2.replace('?', '')), ('K3', K3.replace('?', ''))):
        print('\n'.join(t1(t, 20000, label=f'T4 {lab}')[0]))
    print('\n'.join(t2()))
    print('\n'.join(t3()))
