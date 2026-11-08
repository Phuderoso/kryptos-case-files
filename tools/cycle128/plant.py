"""Cycle 128 planted controls: ACA Sequence Transposition and a Gromark digit substitution driven by the SAME
primer stream (independent textbook encryptor; reuses cycle 127's seqtrans), arbitrary keyword cipher alphabets;
plus shuffled-K4 nulls (seeds 12801-12802)."""
import random,os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cycle127'))
from plant import seqtrans,seq,plain,K4,AZ,KA
def kw_alpha(w):
    s="".join(dict.fromkeys(w+AZ)); return s
def gromark(t,digits,PA,CA,beau):
    return "".join(CA[(d-PA.index(c))%26] if beau else CA[(PA.index(c)+d)%26] for c,d in zip(t,digits))
if __name__=="__main__":
    P=plain(); n=len(P)
    # ctl1: model A (Gromark on plaintext positions, then transposition), PA=A-Z, CA keyed by ENIGMA, Vig form
    pr="31415"; print("ctl1",seqtrans(gromark(P,seq(pr,n),AZ,kw_alpha("ENIGMA"),0),pr,"LANGLEYCIA",0))
    # ctl2: model B (transposition, then Gromark on carved positions), PA=KRYPTOS, CA keyed by SHADOW, Beaufort form
    pr="19902"; print("ctl2",gromark(seqtrans(P,pr,"UNDERWORLD",1),seq(pr,n),KA,kw_alpha("SHADOW"),1))
    # ctl3: model A, PA=KRYPTOS, CA=KRYPTOS (Quagmire-III-like Gromark), Vig form
    pr="08800"; print("ctl3",seqtrans(gromark(P,seq(pr,n),KA,KA,0),pr,"ILLUMINATE",1))
    # ctl4: model B, PA=A-Z, CA=A-Z (plain Gronsfeld-style), Vig form
    pr="77553"; print("ctl4",gromark(seqtrans(P,pr,"CLOCKWORKS",0),seq(pr,n),AZ,AZ,0))
    for s in (1,2):
        l=list(K4); random.Random(12800+s).shuffle(l); print(f"null{s}","".join(l))
