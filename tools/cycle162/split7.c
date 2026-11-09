/* Cycle 162 (IDEAS I-013): split periodic key that keeps the width-7 phase.
   Two periodic keys of period P (default 7), phase counted from position 0 of the chosen index, key 1 on
   positions < b and key 2 on positions >= b, boundary b free in 0..97 (also inside a crib).  Quagmire III
   tableau (one keyed alphabet A on both sides) for every alphabet in alpha.bin; Vigenere (variant Beaufort is the
   dual and shares consistency) or Beaufort chosen independently per segment.  Layers: direct (identity), or behind
   every bank permutation in both directions with the key at the plaintext index (ix 0, model Q: substitute then
   transpose) or at the carved index (ix 1, transpose then substitute).  Exact.
   Consistency: in each segment, cribs in one residue class (x mod P) must imply one key value
     Vig: A^-1(c) - A^-1(p),  Beau: A^-1(c) + A^-1(p)   (mod 26).
   Prefix scan in increasing x: first conflicting crib at x = B1 -> b <= B1 (97 if none).
   Suffix scan in decreasing x: first conflicting crib at x = B2 -> b >= B2+1 (0 if none).  Consistent iff B2+1 <= B1.
   The first check of every scan is evaluated for all alphabets at once (vectorisable), survivors scalar.
   usage: split7 CT alpha.bin perms.bin label qlo qhi [P [idonly [drop]]]
   Output: S lab q dir ix alpha m1 m2 blo bhi   (model S: same alphabet both segments; m 0 Vig, 1 Beau)
           Z lab q dir ix a1 m1 a2 m2 blo bhi   (model Z: AZ (0) / KRYPTOS (1) cross, a1 != a2)
           X lab q dir ix maxB1 minB2+1         (model X: alphabet free per segment over all alphabets)
           H lab ix configs prefilter_pass S_cfg S_hits Z_cfg X_cfg */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PTS="EASTNORTHEASTBERLINCLOCK";
static int NA; static uint8_t *IVT; /* IVT[letter*NA + a] = position of letter in alphabet a */
static uint8_t *B1v[2],*B2v[2]; static int *alive;
/* check list entry: letters x1,x2 vs y1,y2, crib position */
typedef struct{int x1,x2,y1,y2,pos;}chk;
static void scan(const chk*L,int nl,uint8_t*B,uint8_t none){
  if(nl==0){memset(B,none,NA);return;}
  const uint8_t *a1=IVT+L[0].x1*NA,*a2=IVT+L[0].x2*NA,*b1=IVT+L[0].y1*NA,*b2=IVT+L[0].y2*NA; uint8_t p0=L[0].pos;
  for(int a=0;a<NA;a++){int d=(int)a1[a]+a2[a]-b1[a]-b2[a];B[a]=(d==0||d==26||d==-26)?none:p0;}
  if(nl==1)return;
  int na=0;for(int a=0;a<NA;a++)if(B[a]==none)alive[na++]=a;
  for(int k=0;k<na;k++){int a=alive[k];
    for(int l=1;l<nl;l++){int d=(int)IVT[L[l].x1*NA+a]+IVT[L[l].x2*NA+a]-IVT[L[l].y1*NA+a]-IVT[L[l].y2*NA+a];
      if(!(d==0||d==26||d==-26)){B[a]=L[l].pos;break;}}}
}
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage\n");return 1;}
  int C[N];for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  FILE*f=fopen(argv[2],"rb");fseek(f,0,2);NA=ftell(f)/26;rewind(f);uint8_t*AL=malloc(NA*26);if(fread(AL,26,NA,f)!=(size_t)NA)return 1;fclose(f);
  IVT=malloc(26*NA);for(int a=0;a<NA;a++)for(int i=0;i<26;i++)IVT[AL[a*26+i]*NA+a]=i;
  for(int m=0;m<2;m++){B1v[m]=malloc(NA);B2v[m]=malloc(NA);} alive=malloc(NA*sizeof(int));
  const char*lab=argv[4];long qlo=atol(argv[5]),qhi=atol(argv[6]);int P=argc>7?atoi(argv[7]):7;int idonly=argc>8&&atoi(argv[8]);int drop=argc>9?atoi(argv[9]):-1;
  short*Perm;long np;
  if(idonly){np=1;Perm=malloc(N*2);for(int i=0;i<N;i++)Perm[i]=i;qlo=0;qhi=1;}
  else{f=fopen(argv[3],"rb");fseek(f,0,2);np=ftell(f)/(2*N);rewind(f);Perm=malloc(np*N*2);if(fread(Perm,2,np*N,f)!=(size_t)(np*N))return 2;fclose(f);}
  if(qhi>np)qhi=np;
  int pt[24];for(int i=0;i<24;i++)pt[i]=PTS[i]-'A';
  long long H[2][6];memset(H,0,sizeof H);
  for(long q=qlo;q<qhi;q++){const short*s=Perm+q*N;short u[N];for(int i=0;i<N;i++)u[s[i]]=i;
   for(int dir=0;dir<(idonly?1:2);dir++){const short*S=dir?u:s;
    for(int ix=0;ix<(idonly?1:2);ix++){
      int n=0,X[24],CC[24],PP[24],R[24],tx[24],tc[24],tp[24];
      for(int t=0;t<24;t++){if(t==drop)continue;int cpos=S[CI[t]];tx[n]=ix?cpos:CI[t];tc[n]=C[cpos];tp[n]=pt[t];n++;}
      int ord[24];for(int i=0;i<n;i++)ord[i]=i;
      for(int i=1;i<n;i++){int k=ord[i],j=i-1;while(j>=0&&tx[ord[j]]>tx[k]){ord[j+1]=ord[j];j--;}ord[j+1]=k;}
      for(int i=0;i<n;i++){X[i]=tx[ord[i]];CC[i]=tc[ord[i]];PP[i]=tp[ord[i]];R[i]=X[i]%P;}
      H[ix][0]++;
      int Bf1=97,Bf2=-1;
      for(int i=0;i<n&&Bf1==97;i++)for(int j=0;j<i;j++)if(R[j]==R[i]&&((CC[j]==CC[i])!=(PP[j]==PP[i]))){Bf1=X[i];break;}
      for(int i=n-1;i>=0&&Bf2==-1;i--)for(int j=n-1;j>i;j--)if(R[j]==R[i]&&((CC[j]==CC[i])!=(PP[j]==PP[i]))){Bf2=X[i];break;}
      if(Bf2>=Bf1)continue;
      H[ix][1]++;
      /* check lists: prefix (compare with first member of residue), suffix (with last member) */
      chk Lp[2][24],Ls[2][24];int np_=0,ns_=0;int first[32],last[32];
      for(int r=0;r<P;r++)first[r]=last[r]=-1;
      for(int i=0;i<n;i++){int f0=first[R[i]];if(f0<0){first[R[i]]=i;continue;}
        Lp[0][np_]=(chk){CC[i],PP[f0],CC[f0],PP[i],X[i]}; Lp[1][np_]=(chk){CC[i],PP[i],CC[f0],PP[f0],X[i]}; np_++;}
      for(int i=n-1;i>=0;i--){int f0=last[R[i]];if(f0<0){last[R[i]]=i;continue;}
        Ls[0][ns_]=(chk){CC[i],PP[f0],CC[f0],PP[i],X[i]+1}; Ls[1][ns_]=(chk){CC[i],PP[i],CC[f0],PP[f0],X[i]+1}; ns_++;}
      for(int m=0;m<2;m++){scan(Lp[m],np_,B1v[m],97);scan(Ls[m],ns_,B2v[m],0);}
      int maxB1=0,minB2=255,sc=0,zc=0;
      for(int a=0;a<NA;a++){int lo=B2v[0][a]<B2v[1][a]?B2v[0][a]:B2v[1][a],hi=B1v[0][a]>B1v[1][a]?B1v[0][a]:B1v[1][a];
        if(hi>maxB1)maxB1=hi; if(lo<minB2)minB2=lo;
        if(lo<=hi){for(int m1=0;m1<2;m1++)for(int m2=0;m2<2;m2++)if(B2v[m2][a]<=B1v[m1][a]){sc++;H[ix][3]++;
          printf("S %s %ld %d %d %d %d %d %d %d\n",lab,q,dir,ix,a,m1,m2,B2v[m2][a],B1v[m1][a]);}}}
      for(int a1=0;a1<2;a1++)for(int a2=0;a2<2;a2++)if(a1!=a2)for(int m1=0;m1<2;m1++)for(int m2=0;m2<2;m2++)
        if(B2v[m2][a2]<=B1v[m1][a1]){zc++;printf("Z %s %ld %d %d %d %d %d %d %d %d\n",lab,q,dir,ix,a1,m1,a2,m2,B2v[m2][a2],B1v[m1][a1]);}
      if(sc)H[ix][2]++; if(zc)H[ix][4]++; if(minB2<=maxB1){H[ix][5]++;printf("X %s %ld %d %d %d %d\n",lab,q,dir,ix,maxB1,minB2);}
    }}}
  for(int ix=0;ix<2;ix++)if(H[ix][0])printf("H %s %d %lld %lld %lld %lld %lld %lld\n",lab,ix,H[ix][0],H[ix][1],H[ix][2],H[ix][3],H[ix][4],H[ix][5]);
  return 0;}
