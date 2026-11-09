/* Cycle 166 (IDEAS I-070): three key segments / a returning key, period-7 phase kept.
   Index positions 0..96 (direct, plaintext index behind a bank permutation = model Q, or carved index), key letter
   chosen by index mod 7 (phase from position 0).  One keyed alphabet A on both sides (Quagmire III) shared by all
   segments; Vigenere (key value A^-1(c)-A^-1(p); variant Beaufort shares consistency) or Beaufort (A^-1(c)+A^-1(p))
   chosen independently per segment.  Boundaries b1 <= b2 free in 0..97 (also inside a crib).
   Model T: three independent period-7 keys k1 | k2 | k3.   Model R: returning key k1 | k2 | k1 (same key and form
   before b1 and from b2 on).  Exact: a configuration is reported iff the 24 (or 23 with drop) crib equations are
   consistent for some boundaries.
   T: maximal consistent prefix (form m1) and suffix (form m3) are optimal; the middle must be consistent (m2).
   R: for every prefix length e (crib index order) the smallest suffix start s*(e) consistent together with the
      prefix (same table) is computed; the middle [e, s*) must be consistent under m2.  Exhaustive over e.
   Flags: T2 = already a two-segment fit (cycle 162), R0 = middle without cribs (= one key on all cribs).
   usage: split3 CT alpha.bin perms.bin|- label qlo qhi amax [drop [stride]]   (perms '-' = direct only)
   Out: T lab q dir ix a m1 m2 m3 e s two   /  R lab q dir ix a m1 m2 e s
        H lab ix configs Tcfg_AZKA Thits_AZKA Tcfg_all Thits_all T2hits Rcfg_AZKA Rhits_AZKA Rcfg_all Rhits_all R0hits */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PTS="EASTNORTHEASTBERLINCLOCK";
static int n,R[24],V[2][24];
static int cons(int m,int lo,int hi){int K[7];for(int r=0;r<7;r++)K[r]=-1;
  for(int i=lo;i<hi;i++){int r=R[i];if(K[r]<0)K[r]=V[m][i];else if(K[r]!=V[m][i])return 0;}return 1;}
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  int C[N];for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  FILE*f=fopen(argv[2],"rb");fseek(f,0,2);int NA=ftell(f)/26;rewind(f);uint8_t*AL=malloc(NA*26);if(fread(AL,26,NA,f)!=(size_t)NA)return 1;fclose(f);
  uint8_t*IV=malloc(26*NA);for(int a=0;a<NA;a++)for(int i=0;i<26;i++)IV[a*26+AL[a*26+i]]=i;
  const char*lab=argv[4];long qlo=atol(argv[5]),qhi=atol(argv[6]);int amax=atoi(argv[7]);if(amax>NA)amax=NA;
  int drop=argc>8?atoi(argv[8]):-1;long stride=argc>9?atol(argv[9]):1;int idonly=!strcmp(argv[3],"-");
  short*Perm;long np;
  if(idonly){np=1;Perm=malloc(N*2);for(int i=0;i<N;i++)Perm[i]=i;qlo=0;qhi=1;}
  else{f=fopen(argv[3],"rb");fseek(f,0,2);np=ftell(f)/(2*N);rewind(f);Perm=malloc(np*N*2);if(fread(Perm,2,np*N,f)!=(size_t)(np*N))return 2;fclose(f);}
  if(qhi>np)qhi=np;
  int pt[24];for(int i=0;i<24;i++)pt[i]=PTS[i]-'A';
  long long H[2][11];memset(H,0,sizeof H);
  for(long q=qlo;q<qhi;q+=stride){const short*s=Perm+q*N;short u[N];for(int i=0;i<N;i++)u[s[i]]=i;
   for(int dir=0;dir<(idonly?1:2);dir++){const short*S=dir?u:s;
    for(int ix=0;ix<(idonly?1:2);ix++){
      int tx[24],tc[24],tp[24],X[24],CC[24],PP[24];n=0;
      for(int t=0;t<24;t++){if(t==drop)continue;int cpos=S[CI[t]];tx[n]=ix?cpos:CI[t];tc[n]=C[cpos];tp[n]=pt[t];n++;}
      int ord[24];for(int i=0;i<n;i++)ord[i]=i;
      for(int i=1;i<n;i++){int k=ord[i],j=i-1;while(j>=0&&tx[ord[j]]>tx[k]){ord[j+1]=ord[j];j--;}ord[j+1]=k;}
      for(int i=0;i<n;i++){X[i]=tx[ord[i]];CC[i]=tc[ord[i]];PP[i]=tp[ord[i]];R[i]=X[i]%7;}
      H[ix][0]++;int tcA=0,tcAll=0,rcA=0,rcAll=0;
      for(int a=0;a<amax;a++){const uint8_t*iv=IV+a*26;
        for(int i=0;i<n;i++){int c=iv[CC[i]],p=iv[PP[i]];V[0][i]=(c-p+26)%26;V[1][i]=(c+p)%26;}
        int E[2],Sm[2];
        for(int m=0;m<2;m++){int e=n;int K[7];for(int r=0;r<7;r++)K[r]=-1;
          for(int i=0;i<n;i++){int r=R[i];if(K[r]<0)K[r]=V[m][i];else if(K[r]!=V[m][i]){e=i;break;}}E[m]=e;
          int sm=0;for(int r=0;r<7;r++)K[r]=-1;
          for(int i=n-1;i>=0;i--){int r=R[i];if(K[r]<0)K[r]=V[m][i];else if(K[r]!=V[m][i]){sm=i+1;break;}}Sm[m]=sm;}
        int th=0;
        for(int m1=0;m1<2;m1++)for(int m3=0;m3<2;m3++){int e=E[m1],sx=Sm[m3];
          if(sx<=e){th++;H[ix][5]++;printf("T %s %ld %d %d %d %d - %d %d %d 2\n",lab,q,dir,ix,a,m1,m3,e,sx);continue;}
          for(int m2=0;m2<2;m2++)if(cons(m2,e,sx)){th++;printf("T %s %ld %d %d %d %d %d %d %d %d 3\n",lab,q,dir,ix,a,m1,m2,m3,e,sx);}}
        if(th){if(a<2)H[ix][2]+=th;H[ix][4]+=th;if(a<2)tcA=1;tcAll=1;}
        int rh=0;
        for(int m1=0;m1<2;m1++){int K[7];for(int r=0;r<7;r++)K[r]=-1;int ok=1;
          int hit2[2]={0,0};
          for(int e=0;e<=n&&ok;e++){
            if(e>0){int r=R[e-1];if(K[r]<0)K[r]=V[m1][e-1];else if(K[r]!=V[m1][e-1]){ok=0;break;}}
            int K2[7];memcpy(K2,K,sizeof K);int ss=e;
            for(int i=n-1;i>=e;i--){int r=R[i];if(K2[r]<0)K2[r]=V[m1][i];else if(K2[r]!=V[m1][i]){ss=i+1;break;}}
            for(int m2=0;m2<2;m2++)if(!hit2[m2]&&cons(m2,e,ss)){hit2[m2]=1;rh++;if(ss==e)H[ix][10]++;
              printf("R %s %ld %d %d %d %d %d %d %d\n",lab,q,dir,ix,a,m1,m2,e,ss);}
          }}
        if(rh){if(a<2)H[ix][7]+=rh;H[ix][9]+=rh;if(a<2)rcA=1;rcAll=1;}
      }
      H[ix][1]+=tcA;H[ix][3]+=tcAll;H[ix][6]+=rcA;H[ix][8]+=rcAll;
    }}}
  for(int ix=0;ix<2;ix++)if(H[ix][0]){printf("H %s %d",lab,ix);for(int k=0;k<11;k++)printf(" %lld",H[ix][k]);printf("\n");}
  return 0;}
