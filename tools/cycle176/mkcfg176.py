"""Cycle 176: inputs for gm176 / pg176.
  cfg  -> ACA Periodic Gromark key streams (cycle 129's mkcfg construction, which reproduces the ACA ENIGMA example),
          cipher alphabet variants aca (ACA columnar), mix (keyword+A-Z), ka (KRYPTOS) and NEW kmix (keyword+KRYPTOS order);
          plaintext alphabet A-Z or KRYPTOS.  Line: label CA PA k0..k96 (key numbers as letters, A=0).
  primers -> named primers for ordinary Gromark: ACA numerical key (1-based ranks, ties left to right, 10->0) of each
          vocabulary word, raw and with repeats removed, L 3-16; plus a short list of dates/coordinates.
Vocabulary = the themed list of tools/dcol_gen.py + data/cycle56/words56.txt (10,056 words) + themed pairs (cycle 129's)."""
import os,re,sys
HERE=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(HERE,'..','..')
sys.path.insert(0,os.path.join(HERE,'..','cycle129'))
from mkcfg import dedupe,ranks,aca_ca,stream,AZ,KA
def words():
    src=open(os.path.join(R,'tools','dcol_gen.py')).read()
    th=re.search(r'THEMED="""(.*?)"""',src,re.S).group(1).split()
    voc=[l.split()[0].upper() for l in open(os.path.join(R,'data','cycle56','words56.txt')) if l.strip()]
    return list(dict.fromkeys([w for w in th+voc if w.isalpha()]+[a+b for a in th for b in th if a!=b]))
DATES={"K2COORD":"3857065770844","K2LAT":"385765","K2LON":"770844","CIA1990":"1990","DEDIC":"11031990","DEDIC2":"19901103",
 "WALL":"11091989","WALL2":"19891109","WALL3":"09111989","TUT":"26111922","TUT2":"19221126","CARTER":"1922","BERLIN89":"1989",
 "SANBORN45":"1945","K4LEN":"97","LANGLEY":"38951","N38":"385706","W77":"770844"}
if __name__=="__main__":
    W=words()
    if sys.argv[1]=="cfg":
        ws=sys.argv[2:] or W; seen=set(); n=0
        for w in ws:
            kw=dedupe(w)
            if not (3<=len(kw)<=12) or kw in seen: continue
            seen.add(kw)
            for caname,CA in (("aca",aca_ca(kw)),("mix",dedupe(kw+AZ)),("ka",KA),("kmix",dedupe(kw+KA))):
                k="".join(AZ[x] for x in stream(kw,CA))
                for paname,PA in (("az",AZ),("ka",KA)): print(f"{w}/{caname}/{paname}",CA,PA,k); n+=1
        print(n,file=sys.stderr)
    elif sys.argv[1]=="primers":
        seen=set()
        for w in W:
            for tag,x in (("r",w),("d",dedupe(w))):
                if 3<=len(x)<=16:
                    p="".join(str(r%10) for r in ranks(x))
                    if p not in seen: seen.add(p); print(f"{w}/{tag}",p)
        for k,v in DATES.items():
            if v not in seen: seen.add(v); print(k,v)
