#!/usr/bin/env python3
"""Cycle 120 driver: Quagmire I/II/III one-crib-error audit.
Runs planted controls, K4 (identity / bank M=2 / bank M=264), and 5 shuffled nulls.
"""
from __future__ import annotations
import os, sys, time, random, subprocess, pathlib, shutil

ROOT = pathlib.Path('/tmp/kcf')
SCRATCH = pathlib.Path('/workspace/k4c120')
BIN = SCRATCH / 'q1crib120'
ALPHA = pathlib.Path('/home/box/kryptos_support_backup/alpha.bin')
PERMS = pathlib.Path('/home/box/kryptos_support_backup/perms97.bin')
OUT = ROOT / 'data' / 'cycle120'
OUT.mkdir(parents=True, exist_ok=True)

K4 = (ROOT / 'data' / 'k4.txt').read_text().strip()
assert len(K4) == 97
PT = ['X'] * 97
for i, ch in enumerate('EASTNORTHEAST'):
    PT[21 + i] = ch
for i, ch in enumerate('BERLINCLOCK'):
    PT[63 + i] = ch
CI = list(range(21, 34)) + list(range(63, 74))

def load_alpha(m=264):
    raw = ALPHA.read_bytes()
    return [bytes(raw[i*26:(i+1)*26]) for i in range(len(raw)//26)][:m]

def encrypt_qiii(pt, key, period, alphabet, mode='vig'):
    al = list(alphabet)
    inv = [0]*26
    for j, b in enumerate(al):
        inv[b] = j
    out = ['A']*97
    for j in range(97):
        pj = inv[ord(pt[j]) - 65]
        kj = ord(key[j % period]) - 65
        cj = (kj - pj) % 26 if mode == 'beau' else (pj + kj) % 26
        out[j] = chr(65 + al[cj])
    return ''.join(out)

def apply_perm(text97, perm):
    carved = ['?']*97
    for j in range(97):
        carved[int(perm[j])] = text97[j]
    return ''.join(carved)

def run_tool(ct, perm_path, M, PMAX, print_cap=0, tag=''):
    cmd = [str(BIN), str(ALPHA), str(perm_path), ct, str(M), str(PMAX), str(print_cap)]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    out = r.stdout
    (OUT / f'{tag}.out').write_text(out + f'\n# wall_sec {dt:.3f}\n# rc {r.returncode}\n')
    if r.returncode != 0:
        print(f'FAIL {tag} rc={r.returncode} stderr={r.stderr[:200]}', file=sys.stderr)
    return out, dt

def parse_totals(out: str):
    d = {}
    for line in out.splitlines():
        if line.startswith('TOTAL_'):
            parts = line.split()
            for i in range(0, len(parts)-1, 2):
                if parts[i].startswith('TOTAL_'):
                    d[parts[i]] = int(parts[i+1])
        if line.startswith('HIST_'):
            name, *rest = line.split()
            d[name] = {int(a): int(b) for a, b in (x.split(':') for x in rest)}
    return d

def make_ident():
    import numpy as np
    path = SCRATCH / 'ident97.bin'
    np.arange(97, dtype=np.int16).tofile(path)
    return path

def make_single_perm(perm, path):
    import numpy as np
    np.asarray(perm, dtype=np.int16).tofile(path)
    return path

def plant_control(period=5, key='KRYPT', mode='vig', alpha_idx=1, flip_crib=None, perm=None):
    alph = load_alpha(264)[alpha_idx]
    rng = random.Random(120)
    pt = PT[:]
    for i in range(97):
        if pt[i] == 'X':
            pt[i] = chr(65 + rng.randrange(26))
    ct_pt = encrypt_qiii(pt, key, period, alph, mode=mode)
    if perm is None:
        perm = list(range(97))
    ct = apply_perm(ct_pt, perm)
    if flip_crib is not None:
        pos = int(perm[CI[flip_crib]])
        old = ct[pos]
        ct = ct[:pos] + chr(65 + (ord(old) - 65 + 1) % 26) + ct[pos+1:]
    return ct, perm, alph

def main():
    if not BIN.exists():
        subprocess.check_call(['gcc','-O3','-fopenmp','-o',str(BIN),
            str(ROOT/'tools/cycle120/q1crib120.c')])
    log = []
    def L(s):
        print(s, flush=True); log.append(s)
    t0 = time.time()
    import numpy as np
    ident = make_ident()
    all_perms = np.fromfile(PERMS, dtype=np.int16).reshape(-1, 97)
    plant_perm = all_perms[1000].tolist()
    controls = []

    L('=== CONTROLS ===')
    for name, kwargs, M, PMAX, expect in [
        ('ctl_clean_ident', dict(period=5,key='KRYPT',mode='vig',alpha_idx=1,flip_crib=None,perm=list(range(97))), 2, 8, 'strict'),
        ('ctl_clean_perm', dict(period=5,key='KRYPT',mode='vig',alpha_idx=1,flip_crib=None,perm=plant_perm), 2, 8, 'strict'),
        ('ctl_flip_perm', dict(period=5,key='KRYPT',mode='vig',alpha_idx=1,flip_crib=3,perm=plant_perm), 2, 8, 'soft_only'),
        ('ctl_beau_ident', dict(period=4,key='FIRE',mode='beau',alpha_idx=0,flip_crib=None,perm=list(range(97))), 1, 6, 'strict'),
    ]:
        ct, perm, _ = plant_control(**kwargs)
        path = SCRATCH / f'{name}.bin'
        make_single_perm(perm, path)
        out, dt = run_tool(ct, path, M, PMAX, 20 if expect=='soft_only' else 5, name)
        tot = parse_totals(out)
        if expect == 'strict':
            ok = tot.get('TOTAL_STRICT', 0) > 0
        else:
            ok = tot.get('TOTAL_SOFT', 0) > 0 and tot.get('TOTAL_STRICT', 0) == 0
        controls.append((name, ok, tot, dt))
        L(f'{name}: strict={tot.get("TOTAL_STRICT")} soft={tot.get("TOTAL_SOFT")} soft_only={tot.get("TOTAL_SOFT_ONLY")} PASS={ok} {dt:.2f}s')

    L('=== K4 identity M=264 ===')
    out, dt = run_tool(K4, ident, 264, 16, 40, 'k4_ident_m264')
    k4_id = parse_totals(out)
    L(f'K4 ident: strict={k4_id.get("TOTAL_STRICT")} soft_only={k4_id.get("TOTAL_SOFT_ONLY")} {dt:.2f}s')

    L('=== K4 bank M=2 ===')
    out, dt = run_tool(K4, PERMS, 2, 16, 30, 'k4_bank_m2')
    k4_m2 = parse_totals(out)
    L(f'K4 M2: strict={k4_m2.get("TOTAL_STRICT")} soft_only={k4_m2.get("TOTAL_SOFT_ONLY")} {dt:.2f}s')

    L('=== K4 bank M=264 ===')
    out, dt = run_tool(K4, PERMS, 264, 16, 40, 'k4_bank_m264')
    k4_m264 = parse_totals(out)
    L(f'K4 M264: strict={k4_m264.get("TOTAL_STRICT")} soft={k4_m264.get("TOTAL_SOFT")} soft_only={k4_m264.get("TOTAL_SOFT_ONLY")} {dt:.2f}s')

    def nulls(tag, perm_path, M):
        stats = []
        rng = random.Random(20261105)
        for n in range(5):
            s = list(K4); rng.shuffle(s)
            out, dt = run_tool(''.join(s), perm_path, M, 16, 0, f'null{n}_{tag}')
            tot = parse_totals(out); stats.append(tot)
            L(f'null{n} {tag}: strict={tot.get("TOTAL_STRICT")} soft_only={tot.get("TOTAL_SOFT_ONLY")} {dt:.2f}s')
        return stats

    L('=== NULLS ===')
    nulls_m2 = nulls('bank_m2', PERMS, 2)
    nulls_id = nulls('ident_m264', ident, 264)
    nulls_m264 = nulls('bank_m264', PERMS, 264)

    L('=== SUMMARY ===')
    ctl_pass = all(c[1] for c in controls)
    L(f'K4 M264 soft_only={k4_m264.get("TOTAL_SOFT_ONLY")} nulls={[n.get("TOTAL_SOFT_ONLY") for n in nulls_m264]}')
    L(f'controls_pass={ctl_pass} wall={time.time()-t0:.1f}s')
    (OUT / 'run120.log').write_text('\n'.join(log) + '\n')
    lines = [
        '# cycle 120 histograms and totals',
        f'K4_IDENT_STRICT {k4_id.get("TOTAL_STRICT")}',
        f'K4_IDENT_SOFT_ONLY {k4_id.get("TOTAL_SOFT_ONLY")}',
        f'K4_BANK_M2_STRICT {k4_m2.get("TOTAL_STRICT")}',
        f'K4_BANK_M2_SOFT_ONLY {k4_m2.get("TOTAL_SOFT_ONLY")}',
        f'K4_BANK_M264_STRICT {k4_m264.get("TOTAL_STRICT")}',
        f'K4_BANK_M264_SOFT {k4_m264.get("TOTAL_SOFT")}',
        f'K4_BANK_M264_SOFT_ONLY {k4_m264.get("TOTAL_SOFT_ONLY")}',
        f'K4_BANK_M264_HIST_STRICT {k4_m264.get("HIST_STRICT")}',
        f'K4_BANK_M264_HIST_SOFT {k4_m264.get("HIST_SOFT")}',
        f'K4_BANK_M264_HIST_SOFT_ONLY {k4_m264.get("HIST_SOFT_ONLY")}',
    ]
    for i, n in enumerate(nulls_m264):
        lines += [f'NULL{i}_M264_STRICT {n.get("TOTAL_STRICT")}',
                  f'NULL{i}_M264_SOFT {n.get("TOTAL_SOFT")}',
                  f'NULL{i}_M264_SOFT_ONLY {n.get("TOTAL_SOFT_ONLY")}',
                  f'NULL{i}_M264_HIST_SOFT_ONLY {n.get("HIST_SOFT_ONLY")}']
    for i, n in enumerate(nulls_m2):
        lines.append(f'NULL{i}_M2_STRICT {n.get("TOTAL_STRICT")} SOFT_ONLY {n.get("TOTAL_SOFT_ONLY")}')
    for i, n in enumerate(nulls_id):
        lines.append(f'NULL{i}_IDENT_STRICT {n.get("TOTAL_STRICT")} SOFT_ONLY {n.get("TOTAL_SOFT_ONLY")}')
    for name, ok, tot, dt in controls:
        lines.append(f'CTL {name} PASS={ok} strict={tot.get("TOTAL_STRICT")} soft={tot.get("TOTAL_SOFT")} soft_only={tot.get("TOTAL_SOFT_ONLY")} {dt:.2f}s')
    lines += [f'CONTROLS_PASS {ctl_pass}', f'WALL_DRIVER_SEC {time.time()-t0:.1f}']
    (OUT / 'histograms.txt').write_text('\n'.join(lines) + '\n')
    (OUT / 'controls.txt').write_text(
        '# Cycle 120 planted controls\n' +
        '\n'.join(f'{n} PASS={ok} strict={t.get("TOTAL_STRICT")} soft={t.get("TOTAL_SOFT")} soft_only={t.get("TOTAL_SOFT_ONLY")}'
                  for n,ok,t,_ in controls) +
        f'\nCONTROLS_PASS {sum(c[1] for c in controls)}/{len(controls)}\n')

if __name__ == '__main__':
    main()
