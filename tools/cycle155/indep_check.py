"""Cycle 155 independent recount (no code shared with gromark1e.c): for each primer and setting, try ALL 24 single
drops (no certificate pruning) and test the 23 remaining equations by graph propagation (BFS assigns values from a
root, checks every edge, then checks injectivity of the letter nodes per component).
usage: indep_check.py CT L label model(P|G) [primer]   -> counts over all 10^L digit primers (or the given primer)"""
import sys
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
CR=[(21+i,c) for i,c in enumerate("EASTNORTHEAST")]+[(63+i,c) for i,c in enumerate("BERLINCLOCK")]
def ok(edges):
    adj={}
    for a,b,w in edges: adj.setdefault(a,[]).append((b,w)); adj.setdefault(b,[]).append((a,-w))
    val={}
    for s in adj:
        if s in val: continue
        val[s]=0; comp=[s]; st=[s]
        while st:
            x=st.pop()
            for y,w in adj[x]:
                want=(val[x]-w)%26          # edge a-b: v(a)-v(b)=w  => v(b)=v(a)-w
                if y in val:
                    if val[y]!=want: return False
                else: val[y]=want; comp.append(y); st.append(y)
        letters=[val[x] for x in comp if x[0]=='c']
        if len(letters)!=len(set(letters)): return False
    return True
def main():
    ct=sys.argv[1]; L=int(sys.argv[2]); lab=sys.argv[3]; per=sys.argv[4]=='P'
    prs=[sys.argv[5]] if len(sys.argv)>5 else [str(i).zfill(L) for i in range(10**L)]
    strict=one=pairs=0
    for pr in prs:
        d=[int(c) for c in pr]
        while len(d)<74: d.append((d[-L]+d[-L+1])%10)
        for PA in (AZ,KA):
            for f in (0,1):
                eq=[]
                for i,p in CR:
                    w=(PA.index(p)+d[i]) if f==0 else (d[i]-PA.index(p))
                    eq.append((('c',ct[i]),('o',(i//L)%L if per else 0),w%26))
                if ok(eq): strict+=1; continue
                g=sum(ok(eq[:t]+eq[t+1:]) for t in range(24))
                pairs+=g; one+=g>0
                if g and len(prs)==1: print("hit",lab,pr,PA[:3],f,[t for t in range(24) if ok(eq[:t]+eq[t+1:])])
    print(f"I {lab} {'P' if per else 'G'} L={L} primers={len(prs)} strict={strict} one={one} pairs={pairs}")
main()
