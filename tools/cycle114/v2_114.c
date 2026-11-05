/* Cycle 114: Kryha V2 universal disk (52 sectors, published tooth counts), FIXED alphabet pairs, exact.
   Input (stdin): lines "id r_0 ... r_23" where r = sigma*(m(c_i)-f(p_i)) mod 26 at the 24 crib positions (in CRIBS order).
   Letter i uses open hole H[(a+i) mod K]; ring shift s_i = s0 + P(H[..]) + Ttot*floor((a+i)/K)  (mod 26),
   P(x) = teeth of sectors 0..x-1.  Need s_i == r_i.  For each K (1..52), a (0..K-1), s0 (0..25): required residue
   of P at each hole index (conflict -> no), then greedy earliest increasing holes (exact for existence).
   Output: "id nfeasible [K a s0 holes...]" (first feasible config). */
#include <stdio.h>
#include <string.h>
static const int T[52]={4,3,4,3,3,3,4,3,4,4,3,3, 3,3,4,4,3,3,4,3,3,4,3,3, 4,3,3,4,4,4,3,3,4,3,3,3, 4,3,4,3,3,4,5,3,3,3,3,4, 3,3,4,5};
static const int POS[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
int main(){
  int P[53]; P[0]=0; for(int x=0;x<52;x++) P[x+1]=P[x]+T[x]; int Ttot=P[52];
  char id[64]; int r[24];
  while(scanf("%63s",id)==1){
    for(int k=0;k<24;k++) scanf("%d",&r[k]);
    long nfeas=0; int fK=-1,fa=-1,fs=-1,fH[52];
    for(int K=1;K<=52;K++) for(int a=0;a<K;a++) for(int s0=0;s0<26;s0++){
      int req[52]; memset(req,-1,sizeof req); int ok=1;
      for(int k=0;k<24&&ok;k++){ int t=a+POS[k], j=t%K, w=t/K;
        int v=((r[k]-s0-Ttot*w)%26+26)%26;
        if(req[j]<0) req[j]=v; else if(req[j]!=v) ok=0; }
      if(!ok) continue;
      int H[52], x=0;
      for(int j=0;j<K&&ok;j++){
        while(x<52 && req[j]>=0 && P[x]%26!=req[j]) x++;
        if(x>=52){ok=0;break;} H[j]=x; x++;
        if(j<K-1 && x>=52){ok=0;}
      }
      if(!ok) continue;
      nfeas++; if(fK<0){fK=K;fa=a;fs=s0;memcpy(fH,H,sizeof(int)*K);}
    }
    printf("%s %ld",id,nfeas);
    if(fK>0){printf(" %d %d %d",fK,fa,fs); for(int j=0;j<fK;j++) printf(" %d",fH[j]);}
    printf("\n"); fflush(stdout);
  }
  return 0;
}
