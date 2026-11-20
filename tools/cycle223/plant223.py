"""Cycle 223 (I-318 audit) plants (seed 209255) and shuffled-K4 nulls (seeds 209256-209415).
Plants reuse the independent textbook encryptor of tools/cycle219/plant219.py (imported, unchanged), with the period forced
to 21 (ids 0-15) or 20 (ids 16-19), everything else random as in cycle 219; odd ids carry one wrong carved crib letter.
Nulls: random.Random(seed).shuffle(list(K4)), the same construction as cycles 219-222.
usage: plant223.py k123_eng.txt > plants223.tsv ; plant223.py --nulls k4.txt > nulls223.tsv"""
import random, sys, os
sys.path.insert(0, os.environ.get("C219", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle219")))
from plant219 import transpose, sub, carved_pos_of_layer, KA, AZ, CRP, CRS
def make(eng, seed=209255, n=20):
    R = random.Random(seed); rows = []
    for pid in range(n):
        w = 9 if pid % 4 < 2 else 10
        pi = list(range(w)); R.shuffle(pi)
        mode = R.randrange(2); dir_ = R.randrange(2); al = R.randrange(2); form = R.randrange(3); model = R.randrange(2)
        p = 21 if pid < 16 else 20
        A = AZ if al == 0 else KA; key = [R.randrange(26) for _ in range(p)]
        st = R.randrange(len(eng) - 97); P = list(eng[st:st+97])
        for t, i in enumerate(CRP): P[i] = CRS[t]
        P = "".join(P)
        C = transpose(sub(P, key, A, form), w, pi, mode, dir_) if model == 0 else sub(transpose(P, w, pi, mode, dir_), key, A, form)
        seat = -1
        if pid % 2 == 1:
            seat = R.randrange(24); pos = carved_pos_of_layer(w, pi, mode, dir_)[CRP[seat]]
            C = list(C); old = C[pos]; C[pos] = R.choice([x for x in AZ if x != old]); C = "".join(C)
        rows.append(dict(pid=pid, w=w, mode=mode, dir=dir_, al=al, form=form, model=model, p=p, key=key, pi=pi, seat=seat, start=st, P=P, C=C))
    return rows
if __name__ == "__main__":
    if sys.argv[1] == "--nulls":
        K4 = open(sys.argv[2]).read().strip(); print("seed\tct")
        for s in range(209256, 209416):
            l = list(K4); random.Random(s).shuffle(l); print(f"{s}\t{''.join(l)}")
    else:
        eng = open(sys.argv[1]).read().strip()
        print("pid\tw\tmode\tdir\tal\tform\tmodel\tp\tkey\tpi\tseat\tstart\tP\tC")
        for r in make(eng):
            print("\t".join(str(r[k]) if not isinstance(r[k], list) else ",".join(map(str, r[k])) for k in
                  ["pid","w","mode","dir","al","form","model","p","key","pi","seat","start","P","C"]))
