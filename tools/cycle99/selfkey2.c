/* Cycle 99: self-keying by transposition + a periodic keyword added on top.
   Model C: P_i = dec(C_i - k[i%L], C_s(i))  (ciphertext self-key, keyword unknown, L 1..LC) -- crib algebra per residue
   Model P: C_i = enc(P_i, P_s(i)) + k[i%L]   (plaintext self-key), keyword enumerated: all 26^L for L<=LP
   Tableau AZ/KA (index arithmetic), modes Vig/Beau/Var for the self-key; keyword additive on indices.
   Usage: ./selfkey2 CT LC LP perms.bin...   Each perm used as s and s^-1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char*AL[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
int ix[2][26]; int crib[97]; int cp[24];
static inline int md(int x){x%=26;return x<0?x+26:x;}
static inline int deck(int m,int c,int p){return m==0?md(c-p):m==1?md(c+p):md(p-c);}   /* self-key value from c,p */
static inline int decp(int m,int c,int k){return m==0?md(c-k):m==1?md(k-c):md(c+k);}
int main(int argc,char**argv){
  const char*CT=argv[1]; int LC=atoi(argv[2]), LP=atoi(argv[3]); const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK";
  for(int i=0;i<97;i++)crib[i]=-1; for(int i=0;i<13;i++)crib[21+i]=cr1[i]-65; for(int i=0;i<11;i++)crib[63+i]=cr2[i]-65;
  int nc=0; for(int i=0;i<97;i++) if(crib[i]>=0) cp[nc++]=i;
  for(int t=0;t<2;t++)for(int k=0;k<26;k++)ix[t][AL[t][k]-65]=k;
  long tC=0,tP=0,hC=0,hP=0; int bestC=-99,bestP=99;
  for(int a=4;a<argc;a++){ FILE*f=fopen(argv[a],"rb"); fseek(f,0,2); long np=ftell(f)/194; fseek(f,0,0);
    short*S=malloc(np*194); fread(S,194,np,f); fclose(f);
    for(long n=0;n<np;n++) for(int inv=0;inv<2;inv++){ int s[97];
      if(!inv) for(int i=0;i<97;i++) s[i]=S[n*97+i]; else for(int i=0;i<97;i++) s[S[n*97+i]]=i;
      for(int t=0;t<2;t++){ int c[97]; for(int i=0;i<97;i++) c[i]=ix[t][CT[i]-65];
        for(int m=0;m<3;m++){
          /* Model C: required keyword value at crib i: c_i - k = enc-equivalent: P = decp(m, c_i - k, c_s(i)) -> solve k */
          int need[24]; for(int q=0;q<24;q++){ int i=cp[q]; int pv=ix[t][crib[i]];
            /* find x=c_i-k with decp(m,x,c_s(i))==pv */ int x= m==0?md(pv+c[s[i]]): m==1?md(c[s[i]]-pv): md(pv-c[s[i]]); need[q]=md(c[i]-x); }
          for(int L=1;L<=LC;L++){ tC++; int kv[48]; for(int r=0;r<L;r++)kv[r]=-1; int fail=0,chk=0;
            for(int q=0;q<24;q++){ int r=cp[q]%L; if(kv[r]<0)kv[r]=need[q]; else {chk++; if(kv[r]!=need[q])fail++;} }
            int sc=chk-fail*3; if(fail==0 && chk>bestC) bestC=chk;
            if(fail==0 && chk>=10){ hC++; printf("C %s n=%ld inv=%d t=%d m=%d L=%d chk=%d ",argv[a],n,inv,t,m,L,chk);
              for(int i=0;i<97;i++){ int k=kv[i%L]; putchar(k<0?'?':AL[t][decp(m,md(c[i]-k),c[s[i]])]); } putchar('\n'); } }
          /* Model P with keyword enumerated */
          for(int L=1;L<=LP;L++){ long nk=1; for(int r=0;r<L;r++) nk*=26;
            for(long code=0;code<nk;code++){ tP++; int kv[8]; long cc=code; for(int r=0;r<L;r++){kv[r]=cc%26;cc/=26;}
              int cx[97]; for(int i=0;i<97;i++) cx[i]=md(c[i]-kv[i%L]);
              int p[97]; for(int i=0;i<97;i++)p[i]=-1; int fail=0,checks=0;
              for(int q=0;q<24 && fail<=2;q++){ int i0=cp[q]; if(p[i0]>=0) continue; p[i0]=ix[t][crib[i0]]; int i=i0;
                while(1){ int j=s[i]; int v=deck(m,cx[i],p[i]);
                  if(p[j]>=0){ checks++; if(p[j]!=v) fail++; break; }
                  if(crib[j]>=0){ checks++; if(ix[t][crib[j]]!=v){fail++; if(fail>2)break;} }
                  p[j]=v; i=j; } }
              if(fail<bestP)bestP=fail;
              if(fail<=1 && checks>=8){ hP++; printf("P %s n=%ld inv=%d t=%d m=%d L=%d key=",argv[a],n,inv,t,m,L); for(int r=0;r<L;r++)putchar(AL[t][kv[r]]);
                printf(" fail=%d ",fail); for(int i=0;i<97;i++) putchar(p[i]<0?'?':AL[t][p[i]]); putchar('\n'); }
            } }
        }}
    } free(S); }
  fprintf(stderr,"model C configs %ld, best consistent checks %d, hits %ld; model P configs %ld, min fails %d, hits %ld\n",tC,bestC,hC,tP,bestP,hP);
}
