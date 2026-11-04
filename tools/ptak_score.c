/* Cycle 23: plaintext-fed autokey behind a transposition, scored by English where algebra is blind.
   For every fully crib-consistent configuration, the chains fixed by the 24 crib letters give
   derived plaintext letters. Score = mean quadgram log-prob over every 4-window of known letters
   that contains at least one derived (non-crib) letter. Needs >= MINW such windows.
   Models A/B as in ptak_chain.c. Usage: ptak_score CARVED perms.bin qg.bin MINW LMIN LMAX TOPN [STRICT: 1 = windows of derived letters only] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *CR1="EASTNORTHEAST", *CR2="BERLINCLOCK";
typedef struct {double s; int p,t,m,mode,L,nw,ck; char pt[N+1];} R;
int ix(const char*A,char c){for(int i=0;i<26;i++)if(A[i]==c)return i;return -1;}
int cmp(const void*a,const void*b){double x=((R*)a)->s,y=((R*)b)->s;return x<y?1:x>y?-1:0;}
int main(int argc,char**argv){
  const char*carved=argv[1]; int minw=atoi(argv[4]),lmin=atoi(argv[5]),lmax=atoi(argv[6]),topn=atoi(argv[7]); int strict=argc>8?atoi(argv[8]):0;
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); rewind(f);
  int np=sz/(2*N); short*perms=malloc(sz); fread(perms,2,np*N,f); fclose(f);
  float*qg=malloc(sizeof(float)*456976); f=fopen(argv[3],"rb"); fread(qg,4,456976,f); fclose(f);
  int cpos[24],ccha[24],nc=0; int iscrib[N]={0};
  for(int i=0;i<13;i++){cpos[nc]=21+i;ccha[nc++]=CR1[i];}
  for(int i=0;i<11;i++){cpos[nc]=63+i;ccha[nc++]=CR2[i];}
  for(int j=0;j<nc;j++)iscrib[cpos[j]]=1;
  int cap=topn*50; R*top=malloc(sizeof(R)*cap); int ntop=0; long tests=0,scored=0;
  for(int p=0;p<np;p++){ short*P=perms+p*N; int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
   for(int t=0;t<2;t++){const char*A=t?AZ:KA; int cv[N]; for(int k=0;k<N;k++)cv[k]=ix(A,carved[k]);
    for(int model=0;model<2;model++){ int C[N],kv[N],pos[N];
     for(int k=0;k<N;k++)kv[k]=-1;
     if(model==0){for(int i=0;i<N;i++){C[i]=cv[P[i]];pos[i]=i;} for(int j=0;j<nc;j++)kv[cpos[j]]=ix(A,ccha[j]);}
     else {for(int i=0;i<N;i++){C[i]=cv[i];pos[i]=P[i];} for(int j=0;j<nc;j++)kv[inv[cpos[j]]]=ix(A,ccha[j]);}
     for(int mode=0;mode<3;mode++) for(int L=lmin;L<=lmax;L++){ tests++;
      int val[N]; for(int i=0;i<N;i++)val[i]=-1; int ok=1,checks=0;
      for(int r=0;r<L&&ok;r++){ /* find first crib on chain, propagate forward and backward */
        int first=-1; for(int i=r;i<N;i+=L)if(kv[i]>=0){first=i;break;} if(first<0)continue;
        int v=kv[first]; val[first]=v;
        for(int i=first+L;i<N;i+=L){int c=C[i]; v= mode==0?(c-v+26)%26: mode==1?(v-c+26)%26:(c+v)%26;
          if(kv[i]>=0){checks++; if(kv[i]!=v){ok=0;break;}} val[i]=v;}
        if(!ok)break; v=kv[first];
        for(int i=first;i-L>=0;i-=L){int c=C[i]; /* P[i]=dec(C[i],P[i-L]) -> solve P[i-L] */
          int pr= mode==0?(c-v+26)%26: mode==1?(c+v)%26:(v-c+26)%26; val[i-L]=pr; v=pr;}
      }
      if(!ok)continue;
      int lt[N]; int der[N]; for(int i=0;i<N;i++){lt[i]=-1;der[i]=0;}
      for(int i=0;i<N;i++) if(val[i]>=0){ int q=pos[i]; lt[q]=A[val[i]]-'A'; der[q]=!iscrib[q]; }
      double s=0; int nw=0;
      for(int q=0;q+3<N;q++){ if(lt[q]<0||lt[q+1]<0||lt[q+2]<0||lt[q+3]<0)continue;
        if(strict? !(der[q]&&der[q+1]&&der[q+2]&&der[q+3]) : !(der[q]||der[q+1]||der[q+2]||der[q+3]))continue;
        s+=qg[((lt[q]*26+lt[q+1])*26+lt[q+2])*26+lt[q+3]]; nw++; }
      if(nw<minw)continue; scored++; s/=nw;
      if(ntop<cap||s>top[cap-1].s){ R r; r.s=s;r.p=p;r.t=t;r.m=model;r.mode=mode;r.L=L;r.nw=nw;r.ck=checks;
        for(int q=0;q<N;q++)r.pt[q]=lt[q]<0?'.':(char)('A'+lt[q]); r.pt[N]=0;
        if(ntop<cap)top[ntop++]=r; else top[cap-1]=r; qsort(top,ntop,sizeof(R),cmp);} }
   }}}
  printf("tests=%ld scored(windows>=%d)=%ld\n",tests,minw,scored);
  for(int k=0;k<topn&&k<ntop;k++){R*r=top+k; printf("%.3f perm=%d tab=%s model=%c mode=%d L=%d windows=%d checks=%d %s\n",
    r->s,r->p,r->t?"AZ":"KA",r->m?'B':'A',r->mode,r->L,r->nw,r->ck,r->pt);}
  return 0;}
