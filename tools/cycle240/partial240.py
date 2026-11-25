"""partial240.py (PREREG240, I-371): shared helpers. Partial-English plaintext under two placement models.
Non-crib positions = the 73 positions outside 0-based 21-33 / 63-73. m = round(f * 73) of them keep the English letter;
the other 73 - m get a uniformly random letter DIFFERENT from the English one (so the English fraction is exact).
  model S (scattered): the m kept positions are a uniform random subset of the 73.
  model B (block):     the m kept positions are consecutive in the non-crib index list, cyclic start uniform in 0..72
                       (wraps 96 -> 0; a block can straddle a crib, the cribs themselves are always English).
NC = mean log10 quadgram (quadgrams.json, floor for unseen) over the 64 quadgrams touching no crib position (as check235)."""
import json
N = 97
POS = list(range(21, 34)) + list(range(63, 74)); CR = 'EASTNORTHEAST' + 'BERLINCLOCK'
CRIB = set(POS); NONCRIB = [i for i in range(N) if i not in CRIB]
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_Q = json.load(open('quadgrams.json')); Q, FLOOR = _Q['q'], _Q['floor']
QI = [i for i in range(N - 3) if not (set(range(i, i + 4)) & CRIB)]
assert len(QI) == 64
def eng_text():
    return ''.join(c for c in open('k123_eng.txt').read().upper() if c.isalpha())
def base_pt(eng, rng):
    s0 = rng.randrange(len(eng) - N); pt = list(eng[s0:s0 + N])
    for p, c in zip(POS, CR): pt[p] = c
    return pt
def partial(pt, f, model, rng):
    m = round(f * 73); pt = list(pt)
    if model == 'S': keep = set(rng.sample(NONCRIB, m))
    else: st = rng.randrange(73); keep = {NONCRIB[(st + j) % 73] for j in range(m)}
    for i in NONCRIB:
        if i not in keep: pt[i] = rng.choice([c for c in AZ if c != pt[i]])
    return ''.join(pt), m
def nc(t):
    return sum(Q.get(t[i:i + 4], FLOOR) for i in QI) / 64.0
