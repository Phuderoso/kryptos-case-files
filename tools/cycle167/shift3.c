/* Cycle 167 (IDEAS I-082): segment-shifted period-7 key.  One period-7 key k (index mod 7, phase from position 0),
   three segments split by free boundaries; segment j uses k + d_j (d_1 = 0, d_2, d_3 free shifts).  One keyed alphabet
   on both sides (Quagmire III) out of 86,731 (0 = A-Z, 1 = KRYPTOS).  Form per segment f_j in {Vig (A^-1(c)-A^-1(p);
   variant Beaufort has the same consistency), Beau (A^-1(c)+A^-1(p))}; primary = same form in all segments (S),
   secondary = mixed forms (SM).  Exact: equations k[r] + d_s = v are solved by union-find with offsets mod 26 over
   7 key nodes + 3 shift nodes; exhaustive over boundary pairs 0 <= e1 <= e2 <= n in crib-index order (= every
   boundary in 0..97, also inside a crib).  A fit is "3" if all three segments hold at least one crib, else "deg"
   (= one key or k | k+d, already inside cases 123/150).
   usage: shift3 CT alpha.bin perms.bin|- label qlo qhi amax [drop [stride]]
   Out:  S lab q dir ix a f1 f2 f3 npairs n3 e1 e2      (e1 e2 = first 3-segment pair, -1 if none)
         H lab ix configs  cS_AZKA hS_AZKA cS_all hS_all  cM_AZKA hM_AZKA cM_all hM_all  deg_hits   (h = (a,combo) with a 3-seg fit) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PTS="EASTNORTHEASTBERLINCLOCK";
typedef struct{signed char c[10],o[10];}St;
static inline void init(St*s){for(int i=0;i<10;i++){s->c[i]=i;s->o[i]=0;}}
/* val(x)-val(y)=w, x = key node r, y = shift node 7+s  (k[r] + d_s = v  <=>  k[r] - D_s = v with D_s = -d_s) */
static inline int add(St*s,int x,int y,int w){int cx=s->c[x],cy=s->c[y];
  if(cx==cy)return ((s->o[x]-s->o[y]-w)%26+26)%26==0;
  int t=s->o[x]-w-s->o[y];
  for(int z=0;z<10;z++)if(s->c[z]==cy){s->c[z]=cx;s->o[z]=(signed char)(((s->o[z]+t)%26+26)%26);}
  return 1;}
static int n,R[24],V[2][24];
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
  long long H[2][10];memset(H,0,sizeof H);
  for(long q=qlo;q<qhi;q+=stride){const short*s=Perm+q*N;short u[N];for(int i=0;i<N;i++)u[s[i]]=i;
   for(int dir=0;dir<(idonly?1:2);dir++){const short*S=dir?u:s;
    for(int ix=0;ix<(idonly?1:2);ix++){
      int tx[24],tc[24],tp[24],CC[24],PP[24];n=0;
      for(int t=0;t<24;t++){if(t==drop)continue;int cpos=S[CI[t]];tx[n]=ix?cpos:CI[t];tc[n]=C[cpos];tp[n]=pt[t];n++;}
      int ord[24];for(int i=0;i<n;i++)ord[i]=i;
      for(int i=1;i<n;i++){int k=ord[i],j=i-1;while(j>=0&&tx[ord[j]]>tx[k]){ord[j+1]=ord[j];j--;}ord[j+1]=k;}
      for(int i=0;i<n;i++){CC[i]=tc[ord[i]];PP[i]=tp[ord[i]];R[i]=tx[ord[i]]%7;}
      H[ix][0]++;int cf[4]={0,0,0,0};
      for(int a=0;a<amax;a++){const uint8_t*iv=IV+a*26;
        for(int i=0;i<n;i++){int c=iv[CC[i]],p=iv[PP[i]];V[0][i]=(c-p+26)%26;V[1][i]=(c+p)%26;}
        for(int cb=0;cb<8;cb++){int f1=cb&1,f2=(cb>>1)&1,f3=(cb>>2)&1;int same=(cb==0||cb==7);
          long np2=0,n3=0;int fe1=-1,fe2=-1;St s1;init(&s1);
          for(int e1=0;e1<=n;e1++){
            if(e1>0&&!add(&s1,R[e1-1],7,V[f1][e1-1]))break;
            St s2=s1;
            for(int e2=e1;e2<=n;e2++){
              if(e2>e1&&!add(&s2,R[e2-1],8,V[f2][e2-1]))break;
              St s3=s2;int ok=1;
              for(int i=e2;i<n;i++)if(!add(&s3,R[i],9,V[f3][i])){ok=0;break;}
              if(ok){np2++;if(e1>0&&e2>e1&&e2<n){n3++;if(fe1<0){fe1=e1;fe2=e2;}}}
            }}
          if(np2){printf("S %s %ld %d %d %d %d %d %d %ld %ld %d %d\n",lab,q,dir,ix,a,f1,f2,f3,np2,n3,fe1,fe2);
            if(n3==0)H[ix][9]++;}
          if(n3){
            if(same){if(a<2){cf[0]=1;H[ix][2]++;}cf[1]=1;H[ix][4]++;}
            else{if(a<2){cf[2]=1;H[ix][6]++;}cf[3]=1;H[ix][8]++;}}
        }}
      H[ix][1]+=cf[0];H[ix][3]+=cf[1];H[ix][5]+=cf[2];H[ix][7]+=cf[3];
    }}}
  for(int ix=0;ix<2;ix++)if(H[ix][0]){printf("H %s %d",lab,ix);for(int k=0;k<10;k++)printf(" %lld",H[ix][k]);printf("\n");}
  return 0;}
