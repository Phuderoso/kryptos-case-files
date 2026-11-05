/* Cycle 107: Alberti disk that turns by a fixed step d at every carved W (exact, both rings free).
   Model A (sub then transposition): X[j]=carved[t[j]]; setting of X[j] = d * (#W in X[0..j-1]) (+1 if 'tw'=incl: W itself turns first).
   Model B (transposition then sub): setting of carved[i] = d * (#W in carved before i) (incl variant counts W at i).
   Model X: turn at plaintext X (unknown count) -> each crib block monoalphabetic, block 2 offset e free.
   Constraint tau(c) = pi(p) + s (mod 26), pi, tau injective. Weighted union-find; Beaufort = Vig with -d under free rings.
   usage: wturn CT perm.bin nperm  -> prints counts of consistent configs per model */
#include <stdio.h>
#include <stdlib.h>
static const char *CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
int par[52],w[52];
int find(int x){ if(par[x]==x) return x; int r=find(par[x]); w[x]=(w[x]+w[par[x]])%26; par[x]=r; return r;}
/* node p: 0..25 (pi), c: 26..51 (tau). edge tau(c)-pi(p)=s  */
int check(int*pl,int*cl,int*s,int n){ int red=0;
  for(int i=0;i<52;i++){par[i]=i;w[i]=0;}   /* w[x] = val(x)-val(parent) */
  for(int k=0;k<n;k++){ int a=pl[k],b=26+cl[k]; int ra=find(a),rb=find(b);
    if(ra==rb){ if(((w[b]-w[a]-s[k])%26+26)%26) return 0; red++; }
    else { par[rb]=ra; w[rb]=((w[a]+s[k]-w[b])%26+26)%26; } }
  static int stp[2][52][26]; static int st=0; st++;
  int mark[52]={0}; for(int k=0;k<n;k++){mark[pl[k]]=1;mark[26+cl[k]]=1;}
  for(int x=0;x<52;x++){ if(!mark[x]) continue; int r=find(x); int v=w[x]%26; int side=x<26?0:1;
    if(stp[side][r][v]==st) return 0; stp[side][r][v]=st; }
  return 1+red;
}
int nontriv(int*s){for(int k=1;k<24;k++) if(s[k]!=s[0]) return 1; return 0;}
int main(int argc,char**argv){
  const char*ct=argv[1]; int np=atoi(argv[3]);
  short*P=malloc((size_t)np*97*2); FILE*f=fopen(argv[2],"rb"); fread(P,2,(size_t)np*97,f); fclose(f);
  int cpos[24],pl[24]; for(int k=0;k<13;k++){cpos[k]=21+k;pl[k]=CR1[k]-65;} for(int k=0;k<11;k++){cpos[13+k]=63+k;pl[13+k]=CR2[k]-65;}
  int C[97]; for(int i=0;i<97;i++)C[i]=ct[i]-65;
  int wb[98]; wb[0]=0; for(int i=0;i<97;i++) wb[i+1]=wb[i]+(C[i]==22);
  long cntA[2]={0},cntB[2]={0},cntX=0; int shown=0; long mono=0; long hA[30]={0},hB[30]={0},hX[30]={0}; int r;
  for(int p=0;p<np;p++){ short*t=P+(size_t)p*97;
    int X[97]; for(int j=0;j<97;j++) X[j]=C[t[j]];
    int xb[98]; xb[0]=0; for(int j=0;j<97;j++) xb[j+1]=xb[j]+(X[j]==22);
    int cl[24]; for(int k=0;k<24;k++) cl[k]=C[t[cpos[k]]];
    for(int inc=0;inc<2;inc++){
      int nA[24],nB[24];
      for(int k=0;k<24;k++){ int j=cpos[k], i=t[j]; nA[k]=xb[j]+(inc&&X[j]==22); nB[k]=wb[i]+(inc&&C[i]==22); }
      for(int d=0;d<26;d++){ int s[24];
        for(int k=0;k<24;k++) s[k]=(nA[k]*d)%26; if(nontriv(s)&&(r=check(pl,cl,s,24))){hA[r-1]++; if(r-1>=3)printf("TOPA perm=%d inc=%d d=%d checks=%d\n",p,inc,d,r-1);cntA[inc]++; if(0)printf("A perm=%d inc=%d d=%d\n",p,inc,d);}
        for(int k=0;k<24;k++) s[k]=(nB[k]*d)%26; if(nontriv(s)&&(r=check(pl,cl,s,24))){hB[r-1]++; if(r-1>=3)printf("TOPB perm=%d inc=%d d=%d checks=%d\n",p,inc,d,r-1);cntB[inc]++; if(0)printf("B perm=%d inc=%d d=%d\n",p,inc,d);}
      }}
    { int s0[24]={0}; if(check(pl,cl,s0,24)) mono++; }
    for(int e=1;e<26;e++){ int s[24]; for(int k=0;k<24;k++) s[k]=k<13?0:e; if((r=check(pl,cl,s,24))){hX[r-1]++;cntX++; if(0)printf("X perm=%d e=%d\n",p,e);} }
  }
  printf("HIST checks A:");for(int i=0;i<30;i++)if(hA[i])printf(" %d:%ld",i,hA[i]);printf(" B:");for(int i=0;i<30;i++)if(hB[i])printf(" %d:%ld",i,hB[i]);printf(" X:");for(int i=0;i<30;i++)if(hX[i])printf(" %d:%ld",i,hX[i]);printf("\n"); printf("MONO(d=0 plain substitution) perms=%ld\n",mono); printf("RESULT A_excl=%ld A_incl=%ld B_excl=%ld B_incl=%ld X=%ld  (of %d perms x 26)\n",cntA[0],cntA[1],cntB[0],cntB[1],cntX,np);
}
