"""Cycle 166 summary: per text and cell, distinct configurations (q,dir,ix) and distinct (config, alphabet[, forms])
hits for model T (three independent keys; 'T3' excludes fits that are already two-segment = cycle 162 model S) and
model R (returning key; 'R+' excludes R0 = middle segment without cribs = one key on all cribs).
usage: summarize166.py RUNDIR"""
import sys, glob, os, collections
W = sys.argv[1]; labs = [l.split()[0] for l in open(os.path.join(os.path.dirname(__file__), 'texts166.txt'))]
def parse(files, onlydrop=None):
    c = collections.defaultdict(set)
    for fn in files:
        for line in open(fn):
            f = line.split()
            if f[0].startswith('D'):
                if onlydrop is False: continue
                f = f[1:]
            elif onlydrop is True: continue
            if f[0] == 'T':
                a = int(f[5]); cfg = tuple(f[2:5]); three = f[-1] == '3'
                for cls in (['AZKA'] if a < 2 else []) + ['ALL']:
                    c['T_' + cls].add((cfg, a))
                    if three: c['T3_' + cls].add((cfg, a)); c['T3cfg_' + cls].add(cfg)
            elif f[0] == 'R':
                a = int(f[5]); cfg = tuple(f[2:5]); r0 = f[8] == f[9]
                for cls in (['AZKA'] if a < 2 else []) + ['ALL']:
                    if r0: c['R0_' + cls].add((cfg, a))
                    else: c['R+_' + cls].add((cfg, a, f[6], f[7])); c['R+cfg_' + cls].add(cfg)
    return c
keys = ['T3_AZKA', 'T3_ALL', 'R+_AZKA', 'R+_ALL', 'R0_ALL']
print('cell text ' + ' '.join(keys) + ' T3cfg_AZKA R+cfg_AZKA')
for cell, pat, od in [('D-strict', 'D_%s.txt', False), ('D-1err', 'D_%s.txt', True), ('BA', 'BA_%s_*.txt', None),
                      ('BS', 'BS_%s_*.txt', None), ('BS20', 'BS20_%s_*.txt', None), ('BE', 'BE_%s_*.txt', None)]:
    for l in labs:
        fs = glob.glob(os.path.join(W, pat % l))
        if not fs: continue
        c = parse(fs, od)
        print(cell, l, ' '.join(str(len(c[k])) for k in keys), len(c['T3cfg_AZKA']), len(c['R+cfg_AZKA']), f'files={len(fs)}')
