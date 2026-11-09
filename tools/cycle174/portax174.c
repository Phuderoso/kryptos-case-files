/* Cycle 174 (IDEAS I-108): Portax (ACA period-pair digraphic on a Porta slide, any key of period p) behind each of
   the 165,782 K3-law decimations / routes of all.bin, both layer orders, A-Z and KRYPTOS-keyed numbering, p 1..PMAX.
   Portax core (ptx, column test) copied from tools/portax.c (cycle 58, case 56).  Convention as q4d172:
     ix 0: CT = T(Portax(P)): Portax on plaintext order, its ciphertext at index i is C[S[i]], cribs at 21-33, 63-73.
     ix 1: CT = Portax(T(P)): Portax on carved order (c2 = C), known letters at S[crib index].
   A config is consistent if every column has a slide k in 0..12 matching every known letter of its pairs
   (pairs (t, t+p), t = j, j+2p, ...; a tail letter without a partner is free).  "pairs" = pairs holding >= 1 crib letter;
   "bits" = sum over columns of log2(13 / #slides that fit) - a measure of how much the cribs constrained the key.
   usage: portax174 CT perms.bin label qlo qhi PMAX
   Output: X lab q num ix p pairs bits key PT (consistent configs with pairs >= 12) ; H lab num ix p configs consistent ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK"; static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static inline void ptx(int a,int b,int k,int*o1,int*o2){
  int r1,c1; if(a<13){r1=0;c1=a;} else {r1=1;c1=((a-13-k)%13+13)%13;}
  int c2=b>>1,r2=b&1;
  #define UP(r,c) ((r)==0?(c):13+((c)+k)%13)
  if(c1!=c2){*o1=UP(r1,c2);*o2=2*c1+r2;} else {*o1=UP(1-r1,c1);*o2=2*c1+(1-r2);}
}
static int test(const int*ct,const int*want,int p,int*key,int*npairs,double*bits){
  int np=0; double bt=0;
  for(int j=0;j<p;j++){ int first=-1,nk=0; int any=0;
    for(int k=0;k<13;k++){ int good=1;
      for(int t=j;t+p<N&&good;t+=2*p){ int s=t+p; if(want[t]<0&&want[s]<0) continue; any=1;
        int o1,o2; ptx(ct[t],ct[s],k,&o1,&o2);
        if(want[t]>=0&&o1!=want[t]) good=0; if(want[s]>=0&&o2!=want[s]) good=0; }
      if(good){nk++; if(first<0)first=k;} }
    if(!nk) return 0; key[j]=first; if(any) bt+=log2(13.0/nk); }
  for(int j=0;j<p;j++) for(int t=j;t+p<N;t+=2*p) if(want[t]>=0||want[t+p]>=0) np++;
  *npairs=np; *bits=bt; return 1;
}
int main(int argc,char**argv){
  if(argc<7)return 1; const char*Cs=argv[1]; if(strlen(Cs)!=N)return 1;
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); long np=ftell(f)/(2*N); rewind(f); short*PM=malloc(np*N*2); if(fread(PM,2,np*N,f)!=(size_t)(np*N))return 2; fclose(f);
  const char*lab=argv[3]; long qlo=atol(argv[4]),qhi=atol(argv[5]); int PMAX=atoi(argv[6]); if(qhi>np)qhi=np;
  static long long H[2][2][64][2]; memset(H,0,sizeof H);
  int nt[2][26],al[2][26]; for(int i=0;i<26;i++){nt[0][i]=i;al[0][i]=i;nt[1][KA[i]-'A']=i;al[1][i]=KA[i]-'A';}
  for(long q=qlo;q<qhi;q++){const short*S=PM+q*N;
   for(int num=0;num<2;num++){ int ct[N]; for(int i=0;i<N;i++)ct[i]=nt[num][Cs[i]-'A'];
    for(int ix=0;ix<2;ix++){ int c2[N],want[N]; for(int i=0;i<N;i++)want[i]=-1;
      if(ix==1){memcpy(c2,ct,sizeof c2); for(int i=0;i<24;i++) want[S[CI[i]]]=nt[num][PT[i]-'A'];}
      else {for(int i=0;i<N;i++)c2[i]=ct[S[i]]; for(int i=0;i<24;i++) want[CI[i]]=nt[num][PT[i]-'A'];}
      for(int p=1;p<=PMAX;p++){ int key[64],npairs; double bits; H[num][ix][p][0]++;
        if(!test(c2,want,p,key,&npairs,&bits)) continue; H[num][ix][p][1]++;
        if(npairs>=12){ int out[N]; memcpy(out,c2,sizeof out);
          for(int j=0;j<p;j++) for(int s=j;s+p<N;s+=2*p) ptx(c2[s],c2[s+p],key[j],&out[s],&out[s+p]);
          char pt[N+1]; for(int i=0;i<N;i++){int v=(ix==1)?out[S[i]]:out[i]; pt[i]='A'+al[num][v];} pt[N]=0;
          char ks[65]; for(int j=0;j<p;j++) ks[j]='A'+2*key[j]; ks[p]=0;
          printf("X %s %ld %s %d %d %d %.1f %s %s\n",lab,q,num?"KA":"AZ",ix,p,npairs,bits,ks,pt);} } } } }
  for(int num=0;num<2;num++)for(int ix=0;ix<2;ix++)for(int p=1;p<=PMAX;p++) printf("H %s %s %d %d %lld %lld\n",lab,num?"KA":"AZ",ix,p,H[num][ix][p][0],H[num][ix][p][1]);
  printf("END %s\n",lab); return 0; }
