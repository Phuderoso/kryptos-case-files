"""Cycle 167: recovery table for the planted controls (run167/ctl).  A plant is recovered iff shift3 reports the true
alphabet with the true form triple, true layer (dir, ix), and a 3-segment fit (n3 > 0); error plants in drop mode.
Decoys (model T, three independent keys) pass iff the true alphabet has NO 3-segment fit."""
import sys, os
W = sys.argv[1] if len(sys.argv) > 1 else "/workspace/k4c167/run167"
H = os.path.dirname(os.path.abspath(__file__)); ok = tot = 0
for line in open(os.path.join(H, "plants167.txt")):
    w = line.split(); lab, kind, layer, q, d, a, f = w[0], w[2], w[3], int(w[4]), int(w[5]), int(w[6]), w[9]
    ix = {"direct": 0, "Q": 0, "carved": 1}[layer]; dd = d if layer != "direct" else 0; qq = q if q >= 0 else 0
    fn = os.path.join(W, "ctl", lab + (".drop.txt" if lab.startswith("e") else ".txt"))
    S = [l.split() for l in open(fn) if l.startswith("S ")]
    hit = [s for s in S if int(s[2]) == qq and int(s[3]) == dd and int(s[4]) == ix and int(s[5]) == a and s[6] + s[7] + s[8] == f and int(s[10]) > 0]
    nfit = sum(1 for s in S if int(s[10]) > 0)
    good = (len(hit) > 0) if kind == "S" else (len(hit) == 0)
    extra = ""
    if lab.startswith("e"):
        S0 = [l.split() for l in open(os.path.join(W, "ctl", lab + ".txt")) if l.startswith("S ")]
        extra = f" strict_true={sum(1 for s in S0 if int(s[5]) == a and s[6]+s[7]+s[8] == f and int(s[10]) > 0)}"
    tot += 1; ok += good
    print(f"{lab} {kind} {layer} a={a} forms={f} true_fit={len(hit)} all_3seg_fits={nfit}{extra} {'OK' if good else 'FAIL'}")
print(f"controls {ok}/{tot}")
