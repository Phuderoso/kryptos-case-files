/* Cycle 78: transposition (165,065 perms) then periodic keyword + per-carved-row shift on the copper rows.
   pt[i] sits at carved position j=P[i]; key at j = A[a(j)] + B[row(j)], a = col%p (R) or j%p (C), col/row from j+start over 31.
   usage: rowkeyT78 CT perms.bin lo hi minchecks */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *CR="EASTNORTHEASTBERLINCLOCK"; static int CP[24];
static int par[64], val[64];
static int find(int x,int *d){int s=0; while(par[x]!=x){s+=val[x]; x=par[x];} *d=((s%26)+26)%26; return x;}
int main(int argc,char**argv){
  const char*ct=argv[1]; FILE*f=fopen(argv[2],"rb"); long lo=atol(argv[3]),hi=atol(argv[4]); int minc=atoi(argv[5]);
  for(int i=0;i<13;i++)CP[i]=21+i; for(int i=0;i<11;i++)CP[13+i]=63+i;
  short P[97]; long tests=0,cons=0,hits=0; int maxc=-1; fseek(f,lo*97*2,SEEK_SET);
  int ixK[2][26]; for(int t=0;t<2;t++){const char*T=t?AZ:KA; for(int c=0;c<26;c++) ixK[t][T[c]-'A']=c;}
  for(long pi=lo;pi<hi;pi++){ if(fread(P,2,97,f)!=97)break;
   for(int t=0;t<2;t++)for(int mode=0;mode<3;mode++)for(int model=0;model<2;model++)for(int start=26;start<=27;start++)for(int p=1;p<=31;p++){
    tests++; for(int x=0;x<64;x++){par[x]=x;val[x]=0;} int checks=0,ok=1;
    for(int n=0;n<24&&ok;n++){int i=CP[n], j=P[i]; int c=ixK[t][ct[j]-'A'], q=ixK[t][CR[n]-'A'];
      int k= mode==0? c-q : mode==1? c+q : q-c; k=((k%26)+26)%26;
      int g=j+start, col=g%31, row=g/31; int a= model==0? col%p : j%p; int na=a, nb=32+row;
      int da,db; int ra=find(na,&da), rb=find(nb,&db);
      if(ra==rb){ if(((da-db-k)%26+26)%26) ok=0; else checks++; }
      else { par[ra]=rb; val[ra]=((db+k-da)%26+26)%26; } }
    if(!ok)continue; cons++; if(checks>maxc)maxc=checks;
    if(checks>=minc){hits++; printf("HIT perm=%ld tab=%s mode=%d model=%c start=%d p=%d checks=%d\n",pi,t?"AZ":"KA",mode,model?'C':'R',start,p,checks);}
   }}
  printf("tests=%ld consistent=%ld maxchecks=%d hits=%ld\n",tests,cons,maxc,hits); return 0;}
