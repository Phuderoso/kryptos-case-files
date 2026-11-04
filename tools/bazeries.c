/* Cycle 49: Bazeries-style digit-group reversal transposition (groups sized by the digits of a number,
   cycled; each group reversed; optional whole-text reversal) x {arbitrary monoalphabetic substitution,
   periodic Vigenere/Beaufort with A-Z or KRYPTOS tableau, L 1..14, key before or after}. Exact crib test.
   Usage: bazeries CT [maxdigits] ; prints hits, then summary counts. */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int cpos[24], cpt[24]; static int ct[N]; static int kai[26];
static long long nmono=0, nper[2][2][2][15]; /* tab, mode(vig/beau), order(before/after), L */
static long long tested=0;
static void test(const int *dig,int nd,int rev){
  int r[N]; /* r[i] = ct position of plaintext position i */
  int i=0,g=0; while(i<N){int s=dig[g%nd]; if(i+s>N)s=N-i; for(int t=0;t<s;t++) r[i+t]=i+s-1-t; i+=s; g++;}
  if(rev) for(i=0;i<N;i++) r[i]=N-1-r[i];
  tested++;
  /* mono */
  int f[26],b[26]; memset(f,-1,sizeof f); memset(b,-1,sizeof b); int ok=1;
  for(int c=0;c<24&&ok;c++){int p=cpt[c],q=ct[r[cpos[c]]];
    if(f[p]<0&&b[q]<0){f[p]=q;b[q]=p;} else if(f[p]!=q||b[q]!=p) ok=0;}
  if(ok){nmono++; printf("MONO rev=%d key=",rev); for(int k=0;k<nd;k++)printf("%d",dig[k]); printf("\n");}
  for(int tab=0;tab<2;tab++)for(int mode=0;mode<2;mode++)for(int ord=0;ord<2;ord++)for(int L=1;L<=14;L++){
    int kk[14]; for(int k=0;k<L;k++)kk[k]=-1; int good=1;
    for(int c=0;c<24&&good;c++){int p=cpt[c],q=ct[r[cpos[c]]];
      if(tab){p=kai[p];q=kai[q];}
      int off= mode==0 ? (q-p+26)%26 : (q+p)%26;
      int ix = ord==0 ? cpos[c]%L : r[cpos[c]]%L;
      if(kk[ix]<0)kk[ix]=off; else if(kk[ix]!=off) good=0;}
    if(good){nper[tab][mode][ord][L]++;
      printf("PER tab=%s mode=%s ord=%s L=%d rev=%d key=",tab?"KA":"AZ",mode?"beau":"vig",ord?"after":"before",L,rev);
      for(int k=0;k<nd;k++)printf("%d",dig[k]); printf(" kfrag=");
      for(int k=0;k<L;k++)putchar(kk[k]<0?'?':(tab?KA[kk[k]]:'A'+kk[k])); printf("\n");}
  }
}
int main(int argc,char**argv){
  const char*s=argv[1]; int maxd=argc>2?atoi(argv[2]):7; int mind=argc>3?atoi(argv[3]):1; int sl=argc>4?atoi(argv[4]):0, ns=argc>5?atoi(argv[5]):1;
  for(int i=0;i<26;i++)kai[KA[i]-'A']=i;
  for(int i=0;i<N;i++)ct[i]=s[i]-'A';
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  for(int i=0;i<13;i++){cpos[i]=21+i;cpt[i]=c1[i]-'A';}
  for(int i=0;i<11;i++){cpos[13+i]=63+i;cpt[13+i]=c2[i]-'A';}
  int dig[16];
  for(int nd=mind;nd<=maxd;nd++){
    long long tot=1; for(int k=0;k<nd;k++)tot*=9;
    for(long long x=sl;x<tot;x+=ns){long long y=x; for(int k=0;k<nd;k++){dig[k]=1+y%9;y/=9;}
      test(dig,nd,0); test(dig,nd,1);}
    fflush(stdout);
  }
  printf("SUMMARY tested=%lld mono=%lld\n",tested,nmono);
  for(int tab=0;tab<2;tab++)for(int mode=0;mode<2;mode++)for(int ord=0;ord<2;ord++){
    printf("SUMMARY %s %s %s:",tab?"KA":"AZ",mode?"beau":"vig",ord?"after":"before");
    for(int L=1;L<=14;L++)printf(" %lld",nper[tab][mode][ord][L]); printf("\n");}
  return 0;}
