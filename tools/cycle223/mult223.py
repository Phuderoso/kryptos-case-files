"""Cycle 223, descriptive (NOT pre-registered): how much of each text's p 21 raw count R sits in D2 cells of multiplicity >= 24
(many column orders, one crib test), and the largest multiplicity. usage: mult223.py RESDIR (dir with results_*.txt) > mult223.tsv"""
import sys, glob, collections, os
print("text\tR_p21\tR_in_mult_ge24\tshare\tmax_mult")
for f in sorted(glob.glob(os.path.join(sys.argv[1], "results_*.txt"))):
    c = collections.Counter()
    for line in open(f):
        if line.startswith("H "):
            a = line.split()
            if a[8] != "21": continue
            bar = a.index("|"); c[(a[5], a[6], a[7], tuple(a[bar+1:]))] += 1
    tot = sum(c.values()); big = sum(v for v in c.values() if v >= 24)
    print(f"{os.path.basename(f)[8:-4]}\t{tot}\t{big}\t{big/max(tot,1):.4f}\t{max(c.values()) if c else 0}")
