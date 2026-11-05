import random
K=open('k4.txt').read().strip()
def rep(t,w):
    pr=[(t[i],t[i+w]) for i in range(len(t)-w)]; return len(pr)-len(set(pr))
def best(t): return max(rep(t,w) for w in range(18,25))
noW=K.replace('W','')
print('W positions',[i for i,c in enumerate(K) if c=='W'])
print('K4 width21',rep(K,21),'noW widths 18-24',[rep(noW,w) for w in range(18,25)])
r=random.Random(2); vals=[]
for _ in range(20000):
    drop=set(r.sample(range(97),5)); t=''.join(c for i,c in enumerate(K) if i not in drop)
    vals.append(max(rep(t,w) for w in (20,21)))  # w20/21 because 5 deletions shift spacing
import statistics as st
print('random 5-letter deletion: max(rep w20,w21) mean',round(st.mean(vals),2),'frac >=8',sum(v>=8 for v in vals)/len(vals),'frac <=',max(rep(noW,20),rep(noW,21)),':',sum(v<=max(rep(noW,20),rep(noW,21)) for v in vals)/len(vals))
# doubled letters
print('doubles',[(i,K[i]) for i in range(96) if K[i]==K[i+1]])
