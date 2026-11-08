/* Cycle 131: two stacked keyword tableau layers (K1/K2-style "do it twice"), each layer one of
   {A-Z, KRYPTOS tableau} x {Vigenere a+s, Beaufort s-a, variant a-s}, keys = two keywords repeated.
   Mode D (direct): every pair from list1 x list2, all 36 layer settings.
   Mode T (with bank transposition, both directions): model M = layer1 at plaintext position, transposition,
   layer2 at carved position; model P = transposition first, both layers at carved position;
   model Q = both layers at plaintext position, then transposition. Settings restricted by NSET (16 = vig/beau only).
   Exact: all 24 crib letters must match.  usage: dbl CT list1 list2 D|T perms.bin label [lo hi] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*ALPH[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static int inv[2][26]; static char W1[20000][32],W2[20000][32]; static int L1[20000],L2[20000];
static int op(int f,int a,int s){ int r= f==0? a+s : f==1? s-a : a-s; return ((r%26)+26)%26; }
static int lay(int T,int f,int letter,int keyletter){ return ALPH[T][op(f,inv[T][letter],inv[T][keyletter])]-'A'; }
static int rd(const char*fn,char W[][32],int*L){ FILE*f=fopen(fn,"r"); int n=0; while(fscanf(f,"%31s",W[n])==1){ L[n]=strlen(W[n]); n++; } fclose(f); return n; }
int main(int argc,char**argv){
  const char*Cs=argv[1]; int C[N]; for(int i=0;i<N;i++) C[i]=Cs[i]-'A';
  int n1=rd(argv[2],W1,L1), n2=rd(argv[3],W2,L2); int T=argv[4][0]=='T'; const char*lab=argv[6];
  long lo=argc>7?atol(argv[7]):0, hi=argc>8?atol(argv[8]):n1;
  for(int t=0;t<2;t++) for(int i=0;i<26;i++) inv[t][ALPH[t][i]-'A']=i;
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK"; int cp[24],cl[24];
  for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=c1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=c2[i]-'A';}
  short*P=0; long np=0;
  if(T){ FILE*pf=fopen(argv[5],"rb"); fseek(pf,0,SEEK_END); np=ftell(pf)/(2*N); rewind(pf); P=malloc(np*N*4); fread(P,2,np*N,pf);
    for(long q=0;q<np;q++){ short*s=P+q*N,*u=P+(np+q)*N; for(int i=0;i<N;i++) u[s[i]]=i; } }
  int nf=T?2:3; long cfg=0,surv=0;
  for(long a=lo;a<hi&&a<n1;a++) for(int b=0;b<n2;b++)
  for(int T1=0;T1<2;T1++) for(int f1=0;f1<nf;f1++) for(int T2=0;T2<2;T2++) for(int f2=0;f2<nf;f2++){
    const char*w1=W1[a],*w2=W2[b]; int l1=L1[a],l2=L2[b]; cfg++;
    if(!T){ int t=0; for(;t<24;t++){ int i=cp[t]; int y=lay(T1,f1,cl[t],w1[i%l1]-'A'); if(lay(T2,f2,y,w2[i%l2]-'A')!=C[i]) break; }
      if(t==24){ surv++; printf("S %s D %s %s T1=%d f1=%d T2=%d f2=%d\n",lab,w1,w2,T1,f1,T2,f2); } continue; }
    static unsigned char ok[3][24][N];
    for(int t=0;t<24;t++){ int i=cp[t]; int y=lay(T1,f1,cl[t],w1[i%l1]-'A'); int q=lay(T2,f2,y,w2[i%l2]-'A');
      for(int j=0;j<N;j++){ ok[0][t][j]= C[j]==lay(T2,f2,y,w2[j%l2]-'A');
        ok[1][t][j]= C[j]==lay(T2,f2,lay(T1,f1,cl[t],w1[j%l1]-'A'),w2[j%l2]-'A');
        ok[2][t][j]= C[j]==q; } }
    for(int m=0;m<3;m++) for(long q=0;q<2*np;q++){ short*s=P+q*N; int t=0; for(;t<24;t++) if(!ok[m][t][s[cp[t]]]) break;
      if(t==24){ surv++; printf("S %s %c %s %s T1=%d f1=%d T2=%d f2=%d perm=%ld dir=%ld\n",lab,"MPQ"[m],w1,w2,T1,f1,T2,f2,q%np,q/np); } }
  }
  printf("C %s %s configs %ld survivors %ld\n",lab,T?"T":"D",cfg,surv);
}
