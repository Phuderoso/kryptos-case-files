import random, sys
sys.path.insert(0, 'tools')
from grille_sat import *
random.seed(4747)
base = "THEDIGGINGWENTSLOWLYUNDERTHEPALEMOONXWALKINGEASTNORTHEASTFROMTHEOLDGATEWEFOUNDTHEBERLINCLOCKSTONEBURIEDINDUSTX"
# put cribs at official positions
pt = list(("SLOWLYTHEDIGGINGWENTONXWE" + "X" * 100)[:N])
for j, ch in CRIBS.items(): pt[j] = ch
filler = "UNDERTHEPALEMOONWEWALKEDFROMTHEOLDGATEANDFOUNDNOTHINGBUTDUSTANDSHADOWSAROUNDTHESTONEWALLBYTHERIVERBANKATNIGHT"
fi = 0
for j in range(N):
    if j not in CRIBS: pt[j] = filler[fi]; fi += 1
pt = "".join(pt)
cfgs = [("A","pt","KA","vig","PALIM"), ("A","ct","AZ","beau","QX"), ("B","pt","AZ","vig","ABSCISSA"), ("B","ct","KA","beau","K")]
for i,(conv,side,tab,mode,key) in enumerate(cfgs):
    o = [random.randrange(4) for _ in range(25)]
    alpha = KA if tab=="KA" else AZ
    ct = encrypt(pt, o, conv, side, alpha, mode, key)
    fn = f"analysis/cycle47_ctl_{i}.txt"; open(fn,"w").write(ct)
    print(fn, conv, side, tab, mode, len(key), key, o)
print(pt)
