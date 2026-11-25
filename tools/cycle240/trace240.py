#!/usr/bin/env python3
"""trace240.py (cycle 240, POST HOC, descriptive; written after analyze240.log): every non-planted H line in a plant file
with NC >= barSH(343) = -6.96338 (and, separately, >= bar218(343) = -6.72457), with
  hd_raw  = Hamming distance of its window key to the planted key (the frozen I-386 metric),
  hd_off  = min over constants c of Hamming(key, planted key + c mod 26) (offset-canonical: Vig/Beau/variant and rotated
            alphabets make key + c an equivalent key),
  ptdiff  = letters differing from the planted plaintext (decrypt distance).
usage: trace240.py WORKDIR"""
import sys
W = sys.argv[1]; BSH, B218 = -6.963380308850821, -6.724569136631808
K = open(W + '/keys233.bin', 'rb').read(); kw = lambda w: K[int(w) * 97:(int(w) + 1) * 97]
tot = dict(sh=0, b=0, eq=0)
for l in open(W + '/plants240.tsv'):
    p = l.rstrip('\n').split('\t'); pid, scope, qi, dr, ix, x, y, f, w, pt = p[0], p[1], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[14]; kp = kw(w)
    for h in open(f'{W}/P/p{pid}.txt'):
        if not h.startswith('H'): continue
        d = dict(kv.split('=') for kv in h.split()[1:]); v = float(d['nc'])
        planted = (int(d['perm']) == int(qi) and d['X'] == x and d['Y'] == y and d['form'] == f and kw(d['w']) == kp
                   and (scope == 'direct' or (d['dir'] == dr and d['ix'] == ix)))
        if planted or v < BSH: continue
        k2 = kw(d['w']); hr = sum(a != b for a, b in zip(k2, kp)); ho = min(sum(a != (b + c) % 26 for a, b in zip(k2, kp)) for c in range(26))
        pd = sum(a != b for a, b in zip(d['pt'], pt)); tot['sh'] += 1; tot['b'] += v >= B218; tot['eq'] += pd == 0
        print(f"plant {pid:>2} {scope:6s} w {d['w']:>4} (planted {w}) X {d['X']} form {d['form']} nc {v:.3f} {'>=B218' if v >= B218 else '<B218 '} hd_raw {hr:2d} hd_off {ho:2d} ptdiff {pd:2d} {d['pt']}")
print(f"# non-planted lines >= barSH {tot['sh']} (>= bar218 {tot['b']}); identical decrypt (equivalent config) {tot['eq']}")
