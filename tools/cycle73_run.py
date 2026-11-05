import time,random,json
from cycle73_fractionated_morse_sat import *
K4=open('/workspace/kcl/data/k4.txt').read().strip()
rnd=random.Random(73); words=open('ctrl_text.txt').read().split()
res={'K4_distinct_letters':len(set(K4))}
for spaced in (True,False):
    legal=make_legal(codeset(0),spaced); res[f'usable_trigraphs_{"spaced" if spaced else "unspaced"}']=sum(1 for t in TRIG if legal(t))
# unspaced: distinct letters in 200 FM controls
mx=0
for j in range(200):
    st=rnd.randrange(0,len(words)-80); perm=[chr(65+i) for i in range(26)]; rnd.shuffle(perm)
    mx=max(mx,len(set(fm_encrypt(words[st:st+80],perm,False)[:97])))
res['unspaced_controls_max_distinct_letters']=mx
legal=make_legal(codeset(0),True); ctr=[]
for j in range(2):
    st=rnd.randrange(0,len(words)-80); perm=[chr(65+i) for i in range(26)]; rnd.shuffle(perm)
    ct=fm_encrypt(words[st:st+80],perm,True)[:97]; t=time.time(); ok,m=solve(ct,legal,True)
    ctr.append({'sat':ok,'secs':round(time.time()-t,1)}); print('ctrl',ctr[-1],flush=True)
res['spaced_controls']=ctr
nl=[]
for j in range(2):
    l=list(K4); rnd.shuffle(l); t=time.time(); ok,_=solve(''.join(l),legal); nl.append({'sat':ok,'secs':round(time.time()-t,1)}); print('null',nl[-1],flush=True)
res['spaced_shuffled_nulls']=nl
t=time.time(); res['K4_spaced']=solve(K4,legal)[0]; res['K4_spaced_secs']=round(time.time()-t,1)
# positional crib counting
def need(w): return sum(len(MORSE[c]) for c in w)+len(w)-1
res['crib_symbols_needed']={'EASTNORTHEAST':need('EASTNORTHEAST'),'BERLINCLOCK':need('BERLINCLOCK')}
res['crib_symbols_available']={'EASTNORTHEAST':13*3,'BERLINCLOCK':11*3}
json.dump(res,open('fm_results.json','w'),indent=1); print(json.dumps(res))
