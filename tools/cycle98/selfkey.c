/* Cycle 98: self-keying by transposition.
   Model C: key = ciphertext read through a permutation s:  P_i = dec(C_i, C_s(i))
   Model P: key = plaintext read through s:                C_i = enc(P_i, P_s(i))  (solved by walking cycles of s)
   Tableaux AZ / KA (index arithmetic on the alphabet); modes Vig (c=p+k), Beau (c=k-p), Var (c=p-k).
   Each perm is tested as s and as s^-1.  Usage: ./selfkey CT perms.bin [perms.bin ...]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char*AL[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
int ix[2][26]; int crib[97];
static int md(int x){x%=26;return x<0?x+26:x;}
int encf(int m,int p,int k){return m==0?md(p+k):m==1?md(k-p):md(p-k);}
int deck(int m,int c,int p){/* key from c,p */ return m==0?md(c-p):m==1?md(c+p):md(p-c);}
int decp(int m,int c,int k){return m==0?md(c-k):m==1?md(k-c):md(c+k);}
int main(int argc,char**argv){
  const char*CT=argv[1]; const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK";
  for(int i=0;i<97;i++)crib[i]=-1; for(int i=0;i<13;i++)crib[21+i]=cr1[i]-65; for(int i=0;i<11;i++)crib[63+i]=cr2[i]-65;
  for(int t=0;t<2;t++)for(int k=0;k<26;k++)ix[t][AL[t][k]-65]=k;
  long tested=0,hitsC=0,hitsP=0; int bestC=0,bestPfail=99;
  for(int a=2;a<argc;a++){ FILE*f=fopen(argv[a],"rb"); fseek(f,0,2); long np=ftell(f)/194; fseek(f,0,0);
    short*S=malloc(np*194); fread(S,194,np,f); fclose(f);
    for(long n=0;n<np;n++) for(int inv=0;inv<2;inv++){ int s[97];
      if(!inv) for(int i=0;i<97;i++) s[i]=S[n*97+i]; else for(int i=0;i<97;i++) s[S[n*97+i]]=i;
      for(int t=0;t<2;t++){ int c[97]; for(int i=0;i<97;i++) c[i]=ix[t][CT[i]-65];
        for(int m=0;m<3;m++){ tested++;
          /* Model C */ int ok=0; for(int i=0;i<97;i++) if(crib[i]>=0){ if(decp(m,c[i],c[s[i]])==ix[t][crib[i]]) ok++; }
          if(ok>bestC)bestC=ok; if(ok>=20){hitsC++; printf("C %s n=%ld inv=%d t=%d m=%d ok=%d ",argv[a],n,inv,t,m,ok);
            for(int i=0;i<97;i++) putchar(AL[t][decp(m,c[i],c[s[i]])]); putchar('\n');}
          /* Model P: c_i = enc(p_i, p_s(i)) -> p_s(i) = key-from(c_i,p_i) */
          int p[97]; for(int i=0;i<97;i++) p[i]=-1; int fail=0,checks=0;
          for(int i0=0;i0<97;i0++) if(crib[i0]>=0 && p[i0]<0){ p[i0]=ix[t][crib[i0]]; int i=i0;
            while(1){ int j=s[i]; int v=deck(m,c[i],p[i]);
              if(p[j]>=0){ checks++; if(p[j]!=v) fail++; if(j==i0||1) { if(j==i0) break; } }
              else { if(crib[j]>=0){ checks++; if(ix[t][crib[j]]!=v) fail++; } p[j]=v; }
              i=j; if(i==i0) break; }
          }
          if(fail<bestPfail)bestPfail=fail;
          if(fail<=1 && checks>=8){ hitsP++; printf("P %s n=%ld inv=%d t=%d m=%d checks=%d fail=%d ",argv[a],n,inv,t,m,checks,fail);
            for(int i=0;i<97;i++) putchar(p[i]<0?'?':AL[t][p[i]]); putchar('\n'); }
        }}
    } free(S); }
  fprintf(stderr,"tested %ld configs; model C best %d/24, hits(>=20) %ld; model P min fails %d, hits(<=1 fail) %ld\n",tested,bestC,hitsC,bestPfail,hitsP);
}
