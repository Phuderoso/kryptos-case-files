/* Cycle 122: Kryha V2 leave-one-out — optimized.
   For each (K,a,s0): build per-crib (j,v); detect conflicts; test hole placement
   only when residue constraints are conflict-free under the chosen drop set.
   Output: id nstrict nsoft_only first_soft_drop [K a s0 holes...]
*/
#include <stdio.h>
#include <string.h>
static const int T[52]={4,3,4,3,3,3,4,3,4,4,3,3, 3,3,4,4,3,3,4,3,3,4,3,3, 4,3,3,4,4,4,3,3,4,3,3,3, 4,3,4,3,3,4,5,3,3,3,3,4, 3,3,4,5};
static const int POS[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};

/* Place holes given req[0..K) where -1 = free. Returns 1 and fills H on success. */
static int place(const int *req, int K, const int *P, int *H){
  int x=0;
  for(int j=0;j<K;j++){
    while(x<52 && req[j]>=0 && P[x]%26!=req[j]) x++;
    if(x>=52) return 0;
    H[j]=x; x++;
    if(j<K-1 && x>=52) return 0;
  }
  return 1;
}

int main(){
  int P[53]; P[0]=0; for(int x=0;x<52;x++) P[x+1]=P[x]+T[x]; int Ttot=P[52];
  char id[64]; int r[24];
  while(scanf("%63s",id)==1){
    for(int k=0;k<24;k++) if(scanf("%d",&r[k])!=1) return 0;
    long nstrict=0, nsoft_only=0;
    int fdrop=-1,fK=-1,fa=-1,fs=-1,fH[52];
    for(int K=1;K<=52;K++) for(int a=0;a<K;a++) for(int s0=0;s0<26;s0++){
      int jj[24], vv[24];
      for(int k=0;k<24;k++){
        int t=a+POS[k]; jj[k]=t%K; int w=t/K;
        vv[k]=((r[k]-s0-Ttot*w)%26+26)%26;
      }
      /* build strict req; track conflict crib pairs */
      int req[52]; memset(req,-1,sizeof req);
      int conflict=0;
      int who[52]; memset(who,-1,sizeof who); /* first crib claiming each hole */
      for(int k=0;k<24;k++){
        int j=jj[k];
        if(req[j]<0){ req[j]=vv[k]; who[j]=k; }
        else if(req[j]!=vv[k]){ conflict=1; break; }
      }
      if(!conflict){
        int H[52];
        if(place(req,K,P,H)){
          nstrict++;
          continue; /* strict success: not soft_only */
        }
        /* residue OK but placement failed — soft can't help residues; placement with fewer
           constraints (drop one) might free a hole requirement. Try drops. */
      }
      /* soft: try each drop */
      for(int d=0;d<24;d++){
        memset(req,-1,sizeof req);
        int ok=1;
        for(int k=0;k<24;k++){
          if(k==d) continue;
          int j=jj[k];
          if(req[j]<0) req[j]=vv[k];
          else if(req[j]!=vv[k]){ ok=0; break; }
        }
        if(!ok) continue;
        int H[52];
        if(!place(req,K,P,H)) continue;
        nsoft_only++;
        if(fdrop<0){ fdrop=d; fK=K; fa=a; fs=s0; memcpy(fH,H,sizeof(int)*K); }
        break;
      }
    }
    printf("%s %ld %ld %d",id,nstrict,nsoft_only,fdrop);
    if(fdrop>=0){ printf(" %d %d %d",fK,fa,fs); for(int j=0;j<fK;j++) printf(" %d",fH[j]); }
    printf("\n"); fflush(stdout);
  }
  return 0;
}
