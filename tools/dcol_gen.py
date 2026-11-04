"""Cycle 52: keyword orders for exact double keyed columnar. Words = themed K1-K3/Kryptos vocabulary + K1-K3
plaintext words + the most frequent English words (length 4-14) from five Gutenberg novels already in data/.
Column order = stable alphabetic rank of the keyword letters (ties left to right). Duplicated orders merged."""
import re,collections,sys
sys.path.insert(0,'/workspace/kcl/tools')
THEMED="""KRYPTOS PALIMPSEST ABSCISSA BERLIN CLOCK BERLINCLOCK EASTNORTHEAST NORTHEAST SHADOW SHADOWFORCES LAYER
LAYERTWO UNDERGROUND IDBYROWS INVISIBLE MAGNETIC LODESTONE TUTANKHAMEN CARTER HOWARDCARTER CANDLE SLOWLY
DESPARATLY CHAMBER TOMB EGYPT LANGLEY SANBORN SCHEIDT WEBSTER ILLUSION IQLUSION NUANCE DIGETAL VIRTUALLY
TRANSPOSE TRANSPOSITION COLUMN COLUMNAR DOUBLE GRID MATRIX SQUARE TABLEAU VIGENERE QUAGMIRE KEYWORD CIPHER
COMPASS LATITUDE LONGITUDE MERIDIAN WELTZEITUHR URANIA ALEXANDERPLATZ WALL DELIVERING MESSAGE POSITION
SECRET HIDDEN BURIED LOCATION COORDINATES WHATSTHEPOINT POINT ANTIPODES MORSE OBELISK PETRIFIED QUARTZ
COPPER SCULPTURE AGENCY CENTRAL INTELLIGENCE TRUTH FREEDOM VERDIGRIS WHIRLPOOL SHELL STONE LIGHT DARKNESS
NORTH SOUTH EAST WEST BERLINWALL CHECKPOINT CHARLIE SPY DEADDROP REMINDER ENIGMA HIEROGLYPH ROSETTA""".split()
words=collections.Counter()
for g in ["g84","g1342","g1661","g2701","g98"]:
    t=open(f'/workspace/kcl/data/{g}.txt',errors='ignore').read().upper()
    words.update(w for w in re.findall(r"[A-Z]+",t) if 4<=len(w)<=14)
from carved_texts import P1,P2f,P3
def S(x): return x if isinstance(x,str) else ''.join(chr(65+v) if isinstance(v,int) else v for v in x)
NTOP=int(sys.argv[1]) if len(sys.argv)>1 else 3000
lst=list(dict.fromkeys(THEMED+[w for w,_ in words.most_common(NTOP)]))
def order(w): return tuple(sorted(range(len(w)),key=lambda i:(w[i],i)))
seen={}
for w in lst:
    if not(4<=len(w)<=14): continue
    o=order(w)
    if o not in seen: seen[o]=w
with open('orders.txt','w') as f:
    for o,w in seen.items(): f.write(f"{w} {len(o)} {' '.join(map(str,o))}\n")
print(len(lst),"words ->",len(seen),"distinct orders")
