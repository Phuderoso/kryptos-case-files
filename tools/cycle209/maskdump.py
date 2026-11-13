import sys, json, numpy as np
sys.path.insert(0, "/workspace/k4c209"); import lib209 as Q, lib201 as L
out = {}
for P in (8,):
    M4, st = Q.c4_mask(P, L.K4); M3 = Q.c3_mask_for(P, L.K4)
    f4 = {x for x in range(97) if M4[x].sum() == 1 and x not in L.CRIBPOS}; f3 = {x for x in range(97) if M3[x].sum() == 1 and x not in L.CRIBPOS}
    extra = [(x, L.AZ[p]) for x in range(97) for p in range(26) if M3[x, p] and not M4[x, p]]
    out[P] = dict(stats=st, forced_c3=sorted(f3), forced_c4=sorted(f4), new_forced=sorted(f4 - f3), extra_bans=extra)
    print(P, st, "new forced", sorted(f4 - f3), "min allowed", int(M4[[x for x in range(97) if x not in L.CRIBPOS]].sum(1).min()))
json.dump(out, open("mask209_P8.json", "w"), indent=0)
