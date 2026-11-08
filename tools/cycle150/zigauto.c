/* Cycle 150: "zig-zag" autokey: the encryption direction changes from letter to letter in a fixed short cycle.
   Sub-layer equation at stream position j:  c_j = s + a*p_j + b*f_j (mod 26), with form F[j mod T]:
     Vigenere (a=+1,b=+1), Beaufort (a=-1,b=+1), variant (a=+1,b=-1); T = 2 or 3, all 9+27 form cycles
     (the 3 uniform cycles are ordinary autokey and serve as a sanity floor).
   Feed f_j = c_{j-L} (ciphertext autokey) or p_{j-L} (plaintext autokey), lag L = 1..96, one global shift s.
   Tableau numbering A-Z or KRYPTOS. Direct, or behind a bank permutation S (both directions):
     ix=0 (model Q, substitution then transposition): stream c[i]=CT[S[i]], crib at stream position i
     ix=1 (carved, transposition then substitution):  stream c = CT, crib p at stream position S[p]
   Exact: every crib position with a known feed gives one value of s; m = size of the largest agreeing set, n = eligible.
   usage: zigauto CT perms.bin|- label lo hi minm_ct minm_pt */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static const char *CRIB="EASTNORTHEASTBERLINCLOCK"; static int cpos[24];
static const char *FN="VBX";
int main(int ac,char**av){
  if(ac<8)return 1; const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]); int minct=atoi(av[6]),minpt=atoi(av[7]);
  {int k=0;for(int i=21;i<=33;i++)cpos[k++]=i;for(int i=63;i<=73;i++)cpos[k++]=i;}
  int A[3]={1,25,1},B[3]={1,1,25};
  int pats[36][3],pT[36],np_=0;
  for(int a=0;a<3;a++)for(int b=0;b<3;b++){pats[np_][0]=a;pats[np_][1]=b;pT[np_++]=2;}
  for(int a=0;a<3;a++)for(int b=0;b<3;b++)for(int c=0;c<3;c++){pats[np_][0]=a;pats[np_][1]=b;pats[np_][2]=c;pT[np_++]=3;}
  long np=1; short*bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np; long cfg=0,printed=0; int bestct=0,bestpt=0,bestctn=0,hist[25]={0};
  for(long q=lo;q<hi;q++)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int nu=0;nu<2;nu++)for(int ix=0;ix<(bank?2:1);ix++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i;
      int c[97],kp[97],kj[24],kv[24]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)c[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++){kj[k]=cpos[k];}}
      else{for(int i=0;i<97;i++)c[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kj[k]=S[cpos[k]];}
      for(int k=0;k<24;k++){kv[k]=idx[CRIB[k]-'A'];kp[kj[k]]=kv[k];}
      for(int feed=0;feed<2;feed++)for(int L=1;L<=96;L++)for(int pi=0;pi<np_;pi++){ cfg++;
        int T=pT[pi],cnt[26]={0},n=0,m=0,sb=0;
        for(int k=0;k<24;k++){int j=kj[k]; if(j<L)continue; int f=feed?kp[j-L]:c[j-L]; if(f<0)continue;
          int F=pats[pi][j%T]; int s=((c[j]-A[F]*kv[k]-B[F]*f)%26+26*26)%26; n++; if(++cnt[s]>m){m=cnt[s];sb=s;}}
        if(!feed){hist[m]++; if(m>bestct){bestct=m;bestctn=n;}} else if(m>bestpt&&m>=2)bestpt=m;
        if((!feed&&m>=minct)||(feed&&m>=minpt&&m>=3)){
          char pt[98]; for(int i=0;i<97;i++)pt[i]='.'; pt[97]=0;
          if(!feed){char out[97]; for(int j=0;j<97;j++){out[j]='?'; if(j<L)continue; int F=pats[pi][j%T]; int v=(c[j]-sb-B[F]*c[j-L])%26; v=(v+26*26)%26; v=(A[F]*v)%26; out[j]=N[v];}
            for(int p=0;p<97;p++)pt[p]=ix==0?out[p]:out[S[p]];}
          char pn[4]={0}; for(int t=0;t<T;t++)pn[t]=FN[pats[pi][t]];
          printf("S %s feed=%s L=%d pat=%s perm=%ld dir=%d ix=%d num=%d s=%d m=%d n=%d %s\n",lab,feed?"PT":"CT",L,pn,q,dir,ix,nu,sb,m,n,pt); printed++;}
      }}}
  printf("C %s cfg=%ld printed=%ld bestCT=%d(n=%d) bestPT=%d hist",lab,cfg,printed,bestct,bestctn,bestpt);
  for(int i=0;i<=24;i++)if(hist[i])printf(" %d:%d",i,hist[i]); printf("\n"); return 0;}
