/* Cycle 66: four-square (Delastelle/Wheatstone family) with arbitrary cipher squares and themed plain squares,
   squares of 26 cells (2x13, 13x2) or 36 cells (6x6, digits appended or A1B2..J0 interleaved).
   Pair (a,b) at rows/cols (ra,ca) in P, (rb,cb) in P:  x = C1[ra][cb], y = C2[rb][ca].
   Exact test: every crib pair fixes one cell of C1 and one of C2; consistent iff cell->symbol is a partial injection.
   Layers: direct; order A (four-square then transposition: I[j]=CT[p[j]]); order B (transposition then four-square:
   known plaintext letters move to I[j]=PT[p[j]]). Perms: cycle-12 set (uint16x97, enc+dec forms; entries 65535 = omitted slot, treated as a null that breaks its pair).
   usage: c66 CT a264.bin c12_perm.bin shape(0..3) [nperm_limit]   CT may contain digits (codes 26..35) for controls */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static int pt[N];
static int R,Cc,S; static int rr[264][36],cc[264][36],inv[264][36]; static int NA;
static double BG[26][26]; static int G_m; static double G_sc; static int G_dec[N];
static int check(const int*I,const int*pm,int a,int off,int*np){
  int cv[2][36],lc[2][36]; memset(cv,-1,sizeof cv); memset(lc,-1,sizeof lc); int n=0;
  for(int k=off;k+1<N;k+=2){int p=pm[k],q=pm[k+1]; if(p<0||q<0)continue;
    if(I[k]>=36||I[k+1]>=36)continue;
    int c1=rr[a][p]*Cc+cc[a][q], c2=rr[a][q]*Cc+cc[a][p]; int x=I[k],y=I[k+1];
    if(cv[0][c1]<0){ if(lc[0][x]>=0) return 0; cv[0][c1]=x; lc[0][x]=c1;} else if(cv[0][c1]!=x) return 0;
    if(cv[1][c2]<0){ if(lc[1][y]>=0) return 0; cv[1][c2]=y; lc[1][y]=c2;} else if(cv[1][c2]!=y) return 0;
    n++;}
  *np=n; G_m=0; G_sc=0;
  for(int k=off;k+1<N;k+=2){ if(pm[k]>=0||pm[k+1]>=0) continue; int x=I[k],y=I[k+1]; if(x>=36||y>=36) continue;
    int cx=lc[0][x], cy=lc[1][y]; if(cx<0||cy<0) continue;
    int ra=cx/Cc, cb=cx%Cc, rb=cy/Cc, ca=cy%Cc; int A_=inv[a][ra*Cc+ca], B_=inv[a][rb*Cc+cb];
    if(A_>=26||B_>=26){G_m++; G_sc+=-6; continue;} G_m++; G_sc+=BG[A_][B_]; }
  return 1;}
int main(int argc,char**argv){
  const char*ct=argv[1]; int shape=atoi(argv[4]); long lim=argc>5?atol(argv[5]):-1;
  int CT[N]; for(int i=0;i<N;i++){char ch=ct[i]; CT[i]=(ch>='A'&&ch<='Z')?ch-'A':26+(ch-'0');}
  for(int i=0;i<N;i++)pt[i]=-1; const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  for(int i=0;i<13;i++)pt[21+i]=c1[i]-'A'; for(int i=0;i<11;i++)pt[63+i]=c2[i]-'A';
  {FILE*g=fopen("bg.txt","r"); for(int i=0;i<26;i++)for(int j=0;j<26;j++) if(fscanf(g,"%lf",&BG[i][j])!=1) return 1; fclose(g);}
  FILE*f=fopen(argv[2],"rb"); unsigned char ab[264*26]; NA=fread(ab,26,264,f); fclose(f);
  if(shape==0){R=2;Cc=13;}else if(shape==1){R=13;Cc=2;}else{R=6;Cc=6;} S=R*Cc;
  for(int a=0;a<NA;a++){int seq[36],m=0;
    for(int i=0;i<26;i++){int L=ab[a*26+i]; seq[m++]=L; if(shape==3&&L<10) seq[m++]=26+(L+1)%10;}
    if(shape==2) for(int d=0;d<10;d++) seq[m++]=26+d;
    for(int i=0;i<m;i++){rr[a][seq[i]]=i/Cc; cc[a][seq[i]]=i%Cc; inv[a][i]=seq[i];}}
  long hist[3][2][40]; memset(hist,0,sizeof hist); int I[N],pm[N];
  /* direct */
  for(int a=0;a<NA;a++)for(int o=0;o<2;o++){int n; if(check(CT,pt,a,o,&n)){hist[0][o][n]++; printf("HIT direct a=%d off=%d n=%d m=%d sc=%.2f\n",a,o,n,G_m,G_m?G_sc/G_m:0);}}
  f=fopen(argv[3],"rb"); unsigned short pp[N]; long np=0;
  while(fread(pp,2,N,f)==N){ if(lim>=0&&np>=lim)break;
    for(int j=0;j<N;j++){ if(pp[j]>=N){I[j]=99;pm[j]=-1;} else {I[j]=CT[pp[j]]; pm[j]=pt[pp[j]];}}
    for(int a=0;a<NA;a++)for(int o=0;o<2;o++){int n;
      if(check(I,pt,a,o,&n)){hist[1][o][n]++; if(n>=10)printf("HIT A perm=%ld a=%d off=%d n=%d m=%d sc=%.2f\n",np,a,o,n,G_m,G_m?G_sc/G_m:0);}
      if(check(CT,pm,a,o,&n)){hist[2][o][n]++; if(n>=10)printf("HIT B perm=%ld a=%d off=%d n=%d\n",np,a,o,n);}}
    np++;}
  fclose(f);
  const char*nm[3]={"direct","A","B"};
  for(int l=0;l<3;l++)for(int o=0;o<2;o++){printf("HIST %s off=%d:",nm[l],o); for(int n=0;n<40;n++) if(hist[l][o][n]) printf(" n%d=%ld",n,hist[l][o][n]); printf("\n");}
  printf("perms=%ld alphabets=%d shape=%d\n",np,NA,shape); return 0;}
