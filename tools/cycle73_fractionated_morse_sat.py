#!/usr/bin/env python3
"""Cycle 73 — Fractionated Morse (new family). Key-agnostic exact SAT test.
Model: plaintext -> Morse, 'x' after each letter, extra 'x' between words (spaced variant),
symbol stream cut into trigraphs over {.,-,x}; each of the 26 trigraphs != 'xxx' is mapped to a letter
by an unknown (arbitrary) bijection. Question: is there ANY bijection under which K4's consecutive-letter
triples decode to a legal Morse stream? Constraints come only from the CT itself (no cribs).
Legal stream: no 'xxx'; (unspaced variant: no 'xx'); every complete maximal dot/dash run is a valid code of
the allowed character set; runs cut by the window edge must be a suffix/prefix of some valid code."""
import itertools, sys, random, json
from pysat.solvers import Cadical153
MORSE = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-',
'V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..'}
DIG = {str(i): ('.'*i+'-'*(5-i)) if i<=5 else ('-'*(i-5)+'.'*(10-i)) for i in range(10)}
DIG['0']='-----'
PUNCT = {'.':'.-.-.-',',':'--..--','?':'..--..'}
TRIG = [''.join(t) for t in itertools.product('.-x',repeat=3) if ''.join(t)!='xxx']
def codeset(level):
    s=set(MORSE.values())
    if level>=1: s|=set(DIG.values())
    if level>=2: s|=set(PUNCT.values())
    return s
def make_legal(codes, spaced):
    pre={c[:i] for c in codes for i in range(1,len(c)+1)}
    suf={c[i:] for c in codes for i in range(len(c))}
    def legal(s):
        if 'xxx' in s: return False
        if not spaced and 'xx' in s: return False
        runs=s.split('x')
        for k,r in enumerate(runs):
            if not r: continue
            left = (k==0); right=(k==len(runs)-1)
            if left and right:
                if not any(r in c for c in codes): return False
            elif left:
                if r not in suf: return False
            elif right:
                if r not in pre: return False
            elif r not in codes: return False
        return True
    return legal
def fm_encrypt(pt_words, perm, spaced=True):
    s=''
    for w in pt_words:
        for ch in w: s+=MORSE[ch]+'x'
        if spaced: s+='x'
    s=s[:len(s)-len(s)%3]
    m={t:perm[i] for i,t in enumerate(TRIG)}
    return ''.join(m[s[i:i+3]] for i in range(0,len(s),3))
_cache={}
def tables(legal):
    k=id(legal)
    if k not in _cache:
        T1=[legal(t) for t in TRIG]
        T2=[[legal(TRIG[a]+TRIG[b]) for b in range(26)] for a in range(26)]
        T3={(a,b,c) for a in range(26) for b in range(26) if T2[a][b] for c in range(26) if T2[b][c] and not legal(TRIG[a]+TRIG[b]+TRIG[c])}
        _cache[k]=(T1,T2,T3)
    return _cache[k]
def solve(ct, legal, want_model=False):
    T1,T2,T3=tables(legal)
    L=sorted(set(ct)); A={c:i for i,c in enumerate(L)}
    if len(L)>sum(1 for t in TRIG if legal(t)): return False,None
    v=lambda a,t: a*26+t+1
    S=Cadical153()
    for a in range(len(L)):
        S.add_clause([v(a,t) for t in range(26)])
        for t1,t2 in itertools.combinations(range(26),2): S.add_clause([-v(a,t1),-v(a,t2)])
    for t in range(26):
        for a1,a2 in itertools.combinations(range(len(L)),2): S.add_clause([-v(a1,t),-v(a2,t)])
    for t in range(26):
        if not T1[t]:
            for a in range(len(L)): S.add_clause([-v(a,t)])
    pairs={(ct[i],ct[i+1]) for i in range(len(ct)-1)}
    for a,b in pairs:
        for t1 in range(26):
            for t2 in range(26):
                if t1!=t2 or a==b:
                    if (a==b)!=(t1==t2): continue
                    if not T2[t1][t2]: S.add_clause([-v(A[a],t1),-v(A[b],t2)])
    triples={tuple(ct[i:i+3]) for i in range(len(ct)-2)}
    for a,b,c in triples:
        for (t1,t2,t3) in T3:
            if (a==b)!=(t1==t2) or (b==c)!=(t2==t3) or (a==c)!=(t1==t3): continue
            S.add_clause([-v(A[a],t1),-v(A[b],t2),-v(A[c],t3)])
    r=S.solve(); mdl=None
    if r and want_model:
        M=set(x for x in S.get_model() if x>0)
        mdl={L[a]:TRIG[t] for a in range(len(L)) for t in range(26) if v(a,t) in M}
    S.delete(); return r,mdl
if __name__=='__main__':
    K4=open('/workspace/kcl/data/k4.txt').read().strip()
    out={}
    rnd=random.Random(73)
    words=open('/workspace/k4c73/ctrl_text.txt').read().split()
    for spaced in (True,False):
        for level in (0,1,2):
            legal=make_legal(codeset(level),spaced)
            tag=f"{'spaced' if spaced else 'unspaced'}_L{level}"
            nT=sum(1 for t in TRIG if legal(t))
            k4,_=solve(K4,legal); k4r,_=solve(K4[::-1],legal)
            nulls=[]
            for j in range(6):
                l=list(K4); rnd.shuffle(l); nulls.append(solve(''.join(l),legal)[0])
            ctr=[]
            for j in range(6):
                st=rnd.randrange(0,len(words)-60); perm=[chr(65+i) for i in range(26)]; rnd.shuffle(perm)
                ct=fm_encrypt(words[st:st+60],perm,spaced)[:97]
                ok,m=solve(ct,legal,True); ctr.append((ok,len(set(ct))))
            out[tag]=dict(usable_trigraphs=nT,K4=k4,K4_reversed=k4r,shuffled_nulls=nulls,controls=ctr)
            print(tag,out[tag],flush=True)
    json.dump(out,open('fm_results.json','w'),indent=1)
