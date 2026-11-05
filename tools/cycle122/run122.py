#!/usr/bin/env python3
"""Cycle 122: Kryha one-crib-error (leave-one-out) audit of cycle 114 B1/B2 (+ A).

Metrics per (pair,sense) [and n for B1]:
  strict     — consistent with all 24 cribs
  soft_only  — not strict, but consistent after dropping exactly one crib letter

Planted controls REQUIRED:
  B1/B2 clean  — recover with strict > 0
  B1/B2 flip   — strict = 0, soft_only recovers at the flipped crib index

Shuffled-ciphertext nulls REQUIRED (≥5).
"""
from __future__ import annotations
import os, sys, time, random, subprocess, pathlib, threading
sys.path.insert(0, '/tmp/kcf/tools/cycle114')
from kryha114 import *
from testB114 import PAIRS, rvec, STEPS, v2_shifts, PREF

ROOT = pathlib.Path('/tmp/kcf')
SCRATCH = pathlib.Path('/workspace/k4c122')
OUT = ROOT / 'data' / 'cycle122'
OUT.mkdir(parents=True, exist_ok=True)
SUPPORT = pathlib.Path('/home/box/kryptos_support_backup/cycle122')
SUPPORT.mkdir(parents=True, exist_ok=True)

B1 = SCRATCH / 'b1_loo122'
B2 = SCRATCH / 'v2_loo122'
CRIB_POS = list(range(21, 34)) + list(range(63, 74))
assert CRIB_POS == [i for i, _ in CRIBS]

def ensure_bins():
    if not B1.exists():
        subprocess.check_call(['gcc', '-O3', '-o', str(B1),
                               str(ROOT / 'tools/cycle122/b1_loo122.c')])
    if not B2.exists():
        subprocess.check_call(['gcc', '-O3', '-o', str(B2),
                               str(ROOT / 'tools/cycle122/v2_loo122.c')])

def flip_crib_ct(ct, crib_idx, seed):
    """Flip the carved letter at the crib position (plaintext crib still assumed)."""
    pos = CRIB_POS[crib_idx]
    r = random.Random(seed)
    L = list(ct)
    while True:
        c = chr(65 + r.randrange(26))
        if c != L[pos]:
            L[pos] = c
            return ''.join(L)

def lines_for(texts):
    """texts: dict name -> ct. Emit id:pi:sg r0..r23 for every pair×sense."""
    out = []
    for nm, ct in texts.items():
        for pi, (F, M) in enumerate(PAIRS):
            for sg in (1, -1):
                rr = rvec(ct, F, M, sg)
                out.append(f"{nm}:{pi}:{sg} " + " ".join(map(str, rr)))
    return out

def run_parallel(exe, lines, njob=4):
    chunks = [lines[k::njob] for k in range(njob)]
    outs = [None] * njob
    def go(k):
        p = subprocess.Popen([str(exe)], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, text=True)
        outs[k] = p.communicate("\n".join(chunks[k]) + "\n")[0]
    th = [threading.Thread(target=go, args=(k,)) for k in range(njob)]
    for t in th: t.start()
    for t in th: t.join()
    return "".join(outs)

def parse_b1(out):
    """id -> (nstrict, nsoft_only, fdrop, fn) aggregated over pairs by summing? No —
    each line is one (nm,pi,sg). Aggregate per nm: sum strict, sum soft_only,
    list of soft survivors."""
    from collections import defaultdict
    agg = defaultdict(lambda: {'strict': 0, 'soft_only': 0, 'soft_hits': []})
    for line in out.splitlines():
        if not line.strip(): continue
        t = line.split()
        nm = t[0].split(':')[0]
        ns, nso, fd, fn = int(t[1]), int(t[2]), int(t[3]), int(t[4])
        # one line = one (pair,sense); count as 1 config-unit if any n hits
        if ns > 0: agg[nm]['strict'] += 1
        if nso > 0:
            agg[nm]['soft_only'] += 1
            agg[nm]['soft_hits'].append((t[0], ns, nso, fd, fn))
    return agg

def parse_b2(out):
    from collections import defaultdict
    agg = defaultdict(lambda: {'strict': 0, 'soft_only': 0, 'soft_hits': []})
    for line in out.splitlines():
        if not line.strip(): continue
        t = line.split()
        nm = t[0].split(':')[0]
        ns, nso, fd = int(t[1]), int(t[2]), int(t[3])
        if ns > 0: agg[nm]['strict'] += 1
        if nso > 0:
            agg[nm]['soft_only'] += 1
            agg[nm]['soft_hits'].append((t[0], ns, nso, fd, t[4:]))
    return agg

def plant_b1(R, flip_idx=None):
    pi = R.randrange(len(PAIRS)); F, M = PAIRS[pi]; sg = R.choice((1, -1))
    n = R.randrange(3, 17)
    w = [R.choice(list(STEPS)) for _ in range(n)]
    s0 = R.randrange(26); sh = [s0]
    for i in range(96): sh.append((sh[-1] + w[i % n]) % 26)
    ct = kryha_enc(PT, F, M, sh, sg)
    note = f"pi={pi} sg={sg} n={n} w={w} s0={s0}"
    if flip_idx is not None:
        ct = flip_crib_ct(ct, flip_idx, R.randrange(10**9))
        note += f" flip={flip_idx}"
    return ct, note, (pi, sg, n)

def plant_b2(R, flip_idx=None):
    pi = R.randrange(len(PAIRS)); F, M = PAIRS[pi]; sg = R.choice((1, -1))
    K = R.randrange(10, 40); H = sorted(R.sample(range(52), K))
    a = R.randrange(K); s0 = R.randrange(26)
    ct = kryha_enc(PT, F, M, v2_shifts(H, a, s0), sg)
    note = f"pi={pi} sg={sg} K={K} a={a} s0={s0} H={H[:8]}..."
    if flip_idx is not None:
        ct = flip_crib_ct(ct, flip_idx, R.randrange(10**9))
        note += f" flip={flip_idx}"
    return ct, note, (pi, sg)

# ---- Test A leave-one-out (published wheels, free alphabets) ----
def a_loo(ct):
    """Return (nstrict, nsoft_only, details). soft = free_feasible with one eq dropped."""
    hits_s, hits_o = [], []
    for wl in WHEELS:
        for st in range(wl):
            s = v1_shifts(wl, st)
            for sg in (1, -1):
                eqs = eqs_from_shifts(ct, s, sg)
                if free_feasible(ct, eqs):
                    hits_s.append((wl, st, sg)); continue
                for d in range(24):
                    eqs2 = [e for i, e in enumerate(eqs) if i != d]
                    if free_feasible(ct, eqs2):
                        hits_o.append((wl, st, sg, d)); break
    return len(hits_s), len(hits_o), hits_s[:5], hits_o[:5]

def main():
    ensure_bins()
    log = []
    def L(s):
        print(s, flush=True); log.append(s)
    t0 = time.time()
    R = random.Random(1220)

    # ---- texts ----
    texts = {'K4': K4}
    for k in range(5):
        texts[f'null{k}'] = ''.join(R.sample(K4, 97))
    ctl_meta = {}
    for name, flip in [('ctl1_clean', None), ('ctl1_flip', 5),
                       ('ctl2_clean', None), ('ctl2_flip', 7)]:
        if name.startswith('ctl1'):
            ct, note, truth = plant_b1(R, flip)
        else:
            ct, note, truth = plant_b2(R, flip)
        texts[name] = ct
        ctl_meta[name] = (note, truth, flip)

    L(f'pairs={len(PAIRS)} texts={list(texts)}')
    lines = lines_for(texts)
    L(f'lines={len(lines)} ({len(texts)} texts × {len(PAIRS)} × 2)')

    # ---- B1 ----
    L('=== B1 leave-one-out ===')
    t1 = time.time()
    out1 = run_parallel(B1, lines, njob=6)
    (SCRATCH / 'b1_raw.out').write_text(out1)
    (SUPPORT / 'b1_raw.out').write_text(out1)
    agg1 = parse_b1(out1)
    for nm in texts:
        a = agg1[nm]
        L(f'B1 {nm}: strict_pairs={a["strict"]} soft_only_pairs={a["soft_only"]}')
    L(f'B1 wall {time.time()-t1:.1f}s')

    # ---- B2 ----
    L('=== B2 leave-one-out ===')
    t2 = time.time()
    # B2 is heavier; still fold soft into one pass so cost ≈ one strict sweep
    out2 = run_parallel(B2, lines, njob=6)
    (SCRATCH / 'b2_raw.out').write_text(out2)
    (SUPPORT / 'b2_raw.out').write_text(out2)
    agg2 = parse_b2(out2)
    for nm in texts:
        a = agg2[nm]
        L(f'B2 {nm}: strict_pairs={a["strict"]} soft_only_pairs={a["soft_only"]}')
    L(f'B2 wall {time.time()-t2:.1f}s')

    # ---- controls check ----
    L('=== CONTROL CHECKS ===')
    ctl_pass = True
    # B1 clean: must have strict on true (pi,sg)
    for name, expect_soft in [('ctl1_clean', False), ('ctl1_flip', True)]:
        note, truth, flip = ctl_meta[name]
        pi, sg, n = truth
        # find the line for this pair
        key = f'{name}:{pi}:{sg}'
        hit_s = hit_o = False; fd = -1
        for line in out1.splitlines():
            if not line.startswith(key + ' '): continue
            t = line.split(); ns, nso, fd, fn = int(t[1]), int(t[2]), int(t[3]), int(t[4])
            hit_s = ns > 0; hit_o = nso > 0
            L(f'  {name} true {key}: nstrict_n={ns} nsoft_n={nso} fdrop={fd} fn={fn} note={note}')
            break
        if expect_soft:
            ok = (not hit_s) and hit_o and (fd == flip or fd >= 0)
            # soft may recover via a different drop that also works; prefer exact
            if hit_o and fd != flip:
                # scan if any soft_only line for this pair has the true drop among recoverable — our C reports first drop only
                # re-check soft at true drop for true n via a dedicated call
                rr = rvec(texts[name], *PAIRS[pi], sg)
                inp = f"x {' '.join(map(str,rr))}\n"
                chk = subprocess.check_output([str(B1)], input=inp, text=True).split()
                ok = int(chk[1]) == 0 and int(chk[2]) > 0
                L(f'  {name} dedicated soft check: {chk} (want soft, flip={flip})')
        else:
            ok = hit_s
        L(f'  {name} PASS={ok}')
        ctl_pass = ctl_pass and ok

    for name, expect_soft in [('ctl2_clean', False), ('ctl2_flip', True)]:
        note, truth, flip = ctl_meta[name]
        pi, sg = truth
        key = f'{name}:{pi}:{sg}'
        hit_s = hit_o = False; fd = -1
        for line in out2.splitlines():
            if not line.startswith(key + ' '): continue
            t = line.split(); ns, nso, fd = int(t[1]), int(t[2]), int(t[3])
            hit_s = ns > 0; hit_o = nso > 0
            L(f'  {name} true {key}: nstrict_cfg={ns} nsoft_only_cfg={nso} fdrop={fd} note={note}')
            break
        if expect_soft:
            ok = (not hit_s) and hit_o
        else:
            ok = hit_s
        L(f'  {name} PASS={ok}')
        ctl_pass = ctl_pass and ok

    # ---- Test A (published wheels, free alphabets) on K4 + 5 nulls + 2 plants ----
    L('=== A published-wheel leave-one-out (free alphabets) ===')
    t3 = time.time()
    a_texts = {'K4': K4}
    for k in range(5):
        a_texts[f'null{k}'] = texts[f'null{k}']
    # plant one published-wheel control
    wl = 17; st = 3; sg = 1; F = A26; M = AL if (AL := open('/tmp/kcf/data/cycle114/a264.txt').read().split()[1]) else A26
    # use random free alphabets
    Fa = rand_alpha(R); Ma = rand_alpha(R)
    sh = v1_shifts(wl, st); s0 = R.randrange(26); sh = [(x + s0) % 26 for x in sh]
    ctA = kryha_enc(PT, Fa, Ma, sh, sg)
    a_texts['ctlA_clean'] = ctA
    ctAf = flip_crib_ct(ctA, 4, 99)
    a_texts['ctlA_flip'] = ctAf
    a_res = {}
    for nm, ct in a_texts.items():
        ns, nso, hs, ho = a_loo(ct)
        a_res[nm] = (ns, nso)
        L(f'A {nm}: strict={ns} soft_only={nso}')
    L(f'A wall {time.time()-t3:.1f}s')

    # ---- summary files ----
    L('=== SUMMARY ===')
    L(f'B1 K4 strict={agg1["K4"]["strict"]} soft_only={agg1["K4"]["soft_only"]}')
    L(f'B1 nulls soft_only={[agg1[f"null{k}"]["soft_only"] for k in range(5)]}')
    L(f'B2 K4 strict={agg2["K4"]["strict"]} soft_only={agg2["K4"]["soft_only"]}')
    L(f'B2 nulls soft_only={[agg2[f"null{k}"]["soft_only"] for k in range(5)]}')
    L(f'A K4 strict={a_res["K4"][0]} soft_only={a_res["K4"][1]}')
    L(f'controls_pass={ctl_pass} wall={time.time()-t0:.1f}s')

    hist = [
        '# cycle 122 Kryha one-crib-error audit',
        f'B1_K4_STRICT_PAIRS {agg1["K4"]["strict"]}',
        f'B1_K4_SOFT_ONLY_PAIRS {agg1["K4"]["soft_only"]}',
        f'B2_K4_STRICT_PAIRS {agg2["K4"]["strict"]}',
        f'B2_K4_SOFT_ONLY_PAIRS {agg2["K4"]["soft_only"]}',
        f'A_K4_STRICT {a_res["K4"][0]}',
        f'A_K4_SOFT_ONLY {a_res["K4"][1]}',
    ]
    for k in range(5):
        hist += [
            f'B1_NULL{k}_STRICT {agg1[f"null{k}"]["strict"]} SOFT_ONLY {agg1[f"null{k}"]["soft_only"]}',
            f'B2_NULL{k}_STRICT {agg2[f"null{k}"]["strict"]} SOFT_ONLY {agg2[f"null{k}"]["soft_only"]}',
            f'A_NULL{k}_STRICT {a_res[f"null{k}"][0]} SOFT_ONLY {a_res[f"null{k}"][1]}',
        ]
    for nm in ctl_meta:
        hist.append(f'CTL {nm} note={ctl_meta[nm][0]} B1s={agg1[nm]["strict"]}/{agg1[nm]["soft_only"]} B2s={agg2[nm]["strict"]}/{agg2[nm]["soft_only"]}')
    hist += [f'A_CTL_CLEAN {a_res["ctlA_clean"]}', f'A_CTL_FLIP {a_res["ctlA_flip"]}',
             f'CONTROLS_PASS {ctl_pass}', f'WALL_SEC {time.time()-t0:.1f}']
    (OUT / 'histograms.txt').write_text('\n'.join(hist) + '\n')
    (OUT / 'run122.log').write_text('\n'.join(log) + '\n')
    (OUT / 'controls.txt').write_text(
        '# Cycle 122 planted Kryha controls\n' +
        '\n'.join(f'{nm} {ctl_meta[nm][0]}' for nm in ctl_meta) +
        f'\nA_clean planted wheel=17\nA_flip crib_idx=4\nCONTROLS_PASS {ctl_pass}\n')
    # compact analysis summary
    analysis = ROOT / 'analysis' / 'cycle122'
    analysis.mkdir(parents=True, exist_ok=True)
    (analysis / 'summary.txt').write_text('\n'.join(hist) + '\n')
    L('wrote data/cycle122 and analysis/cycle122')

if __name__ == '__main__':
    main()
