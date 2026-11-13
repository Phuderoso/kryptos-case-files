"""Cycle 212 (I-284) new planted controls for wrj.c, X and Y drawn from the 136 themed alphabets OUTSIDE case 197's 8 words.
Derived from cycle 210's plant210.py (independent encoder, written from the model text, not from wrq.c).
Plaintext = English words; R1: key index = position inside the plaintext word mod L (+ nothing else); Quagmire tableau (X plain, Y cipher):
  vig: c = Y[(X.index(p) + key[i]) % 26];  beau: c = Y[(key[i] - X.index(p)) % 26]
then model Q: carved[S[i]] = layer[i], S = family row (dir 0) or its inverse (dir 1).
Writes plants.tsv: id fam row dir ix iy form L segE segB o1 o2 key ciphertext."""
import random, struct, sys
SEED = int(sys.argv[1]); r = random.Random(SEED)
AL = [l.split()[0] for l in open("alpha_themed180.txt")]
OUT8 = {0, 1, 2, 3, 4, 9, 13, 26}   # AZ KA PALIMPSEST ABSCISSA BERLINCLOCK SHADOW IQLUSION LAYERTWO (case 197)
POOL = [i for i in range(len(AL)) if i not in OUT8]
WORDS = ("THE OF AND A TO IN IS WAS THAT HE FOR IT WITH AS HIS ON BE AT BY HAD NOT ARE BUT FROM OR HAVE AN THEY WHICH ONE YOU WERE HER ALL "
         "SHE THERE WOULD THEIR WE HIM BEEN HAS WHEN WHO WILL MORE NO IF OUT SO SAID WHAT UP ITS ABOUT INTO THAN THEM CAN ONLY OTHER NEW SOME "
         "TIME COULD THESE TWO MAY THEN DO FIRST ANY MY NOW SUCH LIKE OUR OVER MAN ME EVEN MOST MADE AFTER ALSO DID MANY BEFORE MUST THROUGH "
         "BACK YEARS WHERE MUCH YOUR WAY WELL DOWN SHOULD BECAUSE EACH JUST THOSE PEOPLE HOW TOO LITTLE STATE GOOD VERY MAKE WORLD STILL OWN "
         "SEE MEN WORK LONG GET HERE BETWEEN BOTH LIFE BEING UNDER NEVER DAY SAME ANOTHER KNOW WHILE LAST MIGHT GREAT OLD YEAR OFF COME SINCE "
         "AGAINST GO CAME RIGHT USED TAKE THREE SLOWLY DESPERATELY CHAMBER CANDLE FLICKER WALL PASSAGE DEBRIS REMAINS LOWER CORNER").split()
def fill(n):
    """n letters of words; the last word may be cut (it then continues past the window, as in real text)"""
    out, ws = [], []
    while sum(map(len, ws)) < n: ws.append(r.choice(WORDS))
    return ws
def read_perm(fn, row):
    with open(fn, "rb") as f: f.seek(row * 194); return list(struct.unpack("<97h", f.read(194)))
SEGE = {"EASTNORTHEAST": ["EASTNORTHEAST"], "EAST|NORTHEAST": ["EAST", "NORTHEAST"], "EASTNORTH|EAST": ["EASTNORTH", "EAST"], "EAST|NORTH|EAST": ["EAST", "NORTH", "EAST"]}
SEGB = {"BERLINCLOCK": ["BERLINCLOCK"], "BERLIN|CLOCK": ["BERLIN", "CLOCK"]}
def build(segE, segB, o1, o2):
    # word list covering 0..96 with: a word starting at 21-o1 whose text is o1 filler letters + first crib word, etc.
    words = []
    def pad_to(target):            # fill words so that total length == target exactly (all words >= 1 letter)
        cur = sum(map(len, words))
        while target - cur > 0:
            w = r.choice(WORDS)
            if len(w) > target - cur: w = w[:target - cur]   # truncated filler word still counts as one word
            words.append(w); cur += len(w)
    pad_to(21 - o1)
    pre = "".join(r.choice("ETAOINSHRDLU") for _ in range(o1))
    ce = SEGE[segE]; words.append(pre + ce[0]); words.extend(ce[1:])
    # the last E-crib word may continue: append nothing (word boundary after crib) -- keep simple
    pad_to(63 - o2)
    pre = "".join(r.choice("ETAOINSHRDLU") for _ in range(o2))
    cb = SEGB[segB]; words.append(pre + cb[0]); words.extend(cb[1:])
    pad_to(97)
    return words
rows = []
FAM = {"bank": ("bank.bin", 165065), "all": ("all.bin", 165782)}
specs = []
for i in range(8):
    fam = "bank" if i % 2 == 0 else "all"
    L = [8, 11, 13, 14, 15, 16, 12, 10][i]
    ix = r.choice(POOL); iy = r.choice(POOL)
    segE = r.choice(list(SEGE)); segB = r.choice(list(SEGB))
    o1 = r.randrange(L); o2 = r.randrange(L)
    if i in (2, 5, 6): o2 = r.randrange(max(0, L - 10), L)   # BERLINCLOCK key indices wrap mod L
    o1 = min(o1, 21); o2 = min(o2, 29)
    specs.append((i, fam, L, ix, iy, segE, segB, o1, o2, r.choice(["vig", "beau"])))
with open("plants212.tsv", "w") as f:
    for i, fam, L, ix, iy, segE, segB, o1, o2, form in specs:
        fn, nr = FAM[fam]; row = r.randrange(nr); d = r.randrange(2)
        words = build(segE, segB, o1, o2); pt = "".join(words); assert len(pt) == 97, len(pt)
        assert pt[21:34] == "EASTNORTHEAST" and pt[63:74] == "BERLINCLOCK", pt
        key = [r.randrange(26) for _ in range(L)]
        lay = []
        for w in words:
            for j, ch in enumerate(w):
                xi = AL[ix].index(ch); k = key[j % L]
                lay.append(AL[iy][(xi + k) % 26] if form == "vig" else AL[iy][(k - xi) % 26])
        s = read_perm(fn, row)
        S = s if d == 0 else [s.index(i_) for i_ in range(97)]
        carved = [None] * 97
        for i_ in range(97): carved[S[i_]] = lay[i_]
        ct = "".join(carved)
        f.write("\t".join(map(str, [i, fam, row, d, ix, iy, form, L, segE, segB, o1, o2, "".join(AL[iy][k] for k in key), ct, pt])) + "\n")
print(open("plants212.tsv").read())
