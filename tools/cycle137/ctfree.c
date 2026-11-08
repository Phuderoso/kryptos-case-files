/* Cycle 137: ciphertext-fed autokey with a keyed CIPHER alphabet and an
   ARBITRARY plaintext alphabet (the Quagmire II / IV family of CT-autokey),
   behind every bank transposition, both index orders.

   Model (Vigenere form):  y(c_j) = x(p_j) + z(c_{j-L})   (mod 26)
     y  = cipher-alphabet index (keyed alphabet: a vocabulary word, A-Z or KRYPTOS)
     z  = index used to read the key letter (the previous ciphertext letter):
          the same keyed alphabet (zmode 0), plain A-Z (1) or KRYPTOS (2)
     x  = plaintext-alphabet index: ANY of the 26! alphabets (free).
   Because x is free, Beaufort (x = z(c_{j-L}) - y(c_j)) is the same test as
   Vigenere (x -> -x); variant Beaufort (x = y(c_j) + z(c_{j-L})) is distinct.
   The primer never matters: for j >= L the feedback letter is carved/known.

   Test: d_j = y(c_j) -/+ z(c_{j-L}) at each crib key-index j >= L must be a
   function of the plaintext letter (equal letters -> equal d) and injective
   (different letters -> different d).  extra = active cribs - distinct letters.

   ix=1 carved index (transpose first, autokey on the carved text: layer = C)
   ix=0 plaintext index (model Q: autokey at plaintext position, then
        transpose: layer[i] = C[S[i]])

   usage: ctfree CT words.txt perms.bin label lo hi LMAX [pstride]
   ycomb: 0 (V,V) 1 (V,AZ) 2 (V,KA) 3 (AZ,V) 4 (KA,V); sign 0 '-' 1 '+'.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define MAXW 12000
#define MINCHK 6
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static char W[MAXW][32]; static unsigned char A[MAXW][26], INV[MAXW][26];
static unsigned char AZI[26], KAI[26], KAA[26];
static int Plet[24], C[N]; static const char *lab;
static void keyed(const char*w,unsigned char*al,unsigned char*inv){int u[26]={0},n=0;
 for(const char*p=w;*p;p++){int c=*p-'A';if(c<0||c>25||u[c])continue;u[c]=1;al[n++]=c;}
 for(int c=0;c<26;c++)if(!u[c])al[n++]=c; for(int i=0;i<26;i++)inv[al[i]]=i;}
static const char *YC[5]={"V,V","V,AZ","V,KA","AZ,V","KA,V"};
static const char *XN[2]={"pt","carved"};
static void report(int a,int yc,int sg,int ix,int L,long q,int dir,int extra,
  const unsigned char*y,const unsigned char*z,const short*S,const int*layer){
  /* x-index of every key position j>=L; label positions by crib letter where known */
  int d[N]; for(int j=0;j<N;j++) d[j]=-1;
  for(int j=L;j<N;j++){int v=sg?y[layer[j]]+z[layer[j-L]]:y[layer[j]]-z[layer[j-L]]; d[j]=((v%26)+26)%26;}
  int letter_of[26]; for(int i=0;i<26;i++)letter_of[i]=-1;
  int kp[24]; for(int t=0;t<24;t++){kp[t]=ix?S[CI[t]]:CI[t]; if(kp[t]>=L) letter_of[d[kp[t]]]=Plet[t];}
  char ps[N+1], cls[N+1]; ps[N]=cls[N]=0;
  for(int i=0;i<N;i++){int j=ix?S[i]:i; if(d[j]<0){ps[i]='?';cls[i]='?';}
    else {cls[i]='a'+d[j]; ps[i]= letter_of[d[j]]>=0?'A'+letter_of[d[j]]:'.';}}
  printf("S %s word=%s comb=%s sign=%c ix=%s L=%d perm=%ld dir=%d extra=%d partial=%s classes=%s\n",
    lab,W[a],YC[yc],sg?'+':'-',XN[ix],L,q,dir,extra,ps,cls);
}
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  for(int i=0;i<N;i++)C[i]=argv[1][i]-'A'; lab=argv[4];
  long lo=atol(argv[5]),hi=atol(argv[6]); int LMAX=atoi(argv[7]); long pstride=argc>8?atol(argv[8]):1;
  if(LMAX>96)LMAX=96;
  FILE*wf=fopen(argv[2],"r");int nw=0; while(nw<MAXW&&fscanf(wf,"%31s",W[nw])==1){keyed(W[nw],A[nw],INV[nw]);nw++;} fclose(wf);
  if(hi>nw)hi=nw;
  {unsigned char t[26]; keyed("A",t,AZI); keyed("KRYPTOS",KAA,KAI);}
  for(int t=0;t<24;t++)Plet[t]=PT[t]-'A';
  /* letter groups: for each crib t, gid = first crib index with same letter */
  int gid[24]; for(int t=0;t<24;t++){gid[t]=t;for(int s=0;s<t;s++)if(Plet[s]==Plet[t]){gid[t]=s;break;}}
  FILE*pf=fopen(argv[3],"rb"); fseek(pf,0,SEEK_END); long np=ftell(pf)/(2*N); rewind(pf);
  short*Perm=malloc((size_t)np*N*2); if(fread(Perm,2,(size_t)np*N,pf)!=(size_t)np*N)return 1; fclose(pf);
  long long tests=0,cons=0,surv=0, hist[2][97]; memset(hist,0,sizeof hist);
  long nperm_used=0;
  for(long q=0;q<np;q+=pstride){ nperm_used++;
    const short*s=Perm+q*N; short u[N]; for(int i=0;i<N;i++)u[s[i]]=i;
    for(int dir=0;dir<2;dir++){ const short*S=dir?u:s;
      for(int ix=0;ix<2;ix++){
        int layer[N], kp[24];
        for(int i=0;i<N;i++) layer[i]= ix?C[i]:C[S[i]];
        for(int t=0;t<24;t++) kp[t]= ix?S[CI[t]]:CI[t];
        for(int L=1;L<=LMAX;L++){
          /* active cribs */
          int c1[24],c2[24],act[24],na=0, rep[24]; int nd=0;
          int firstact[24]; for(int t=0;t<24;t++)firstact[t]=-1;
          /* equality checks (e1,e2) and reps for distinctness */
          int eq1[24],eq2[24],ne=0;
          for(int t=0;t<24;t++){int j=kp[t]; if(j<L)continue; c1[na]=layer[j];c2[na]=layer[j-L];act[na]=t;
            int g=gid[t]; if(firstact[g]<0){firstact[g]=na;rep[nd++]=na;} else {eq1[ne]=firstact[g];eq2[ne]=na;ne++;}
            na++;}
          if(ne<MINCHK) continue;
          for(long a=lo;a<hi;a++){
            for(int yc=0;yc<5;yc++){
              const unsigned char*y,*z;
              switch(yc){case 0:y=INV[a];z=INV[a];break;case 1:y=INV[a];z=AZI;break;case 2:y=INV[a];z=KAI;break;
                case 3:y=AZI;z=INV[a];break;default:y=KAI;z=INV[a];}
              for(int sg=0;sg<2;sg++){
                tests++;
                int ok=1;
                for(int e=0;e<ne;e++){int x1=eq1[e],x2=eq2[e];
                  int v1= sg? y[c1[x1]]+z[c2[x1]] : y[c1[x1]]-z[c2[x1]]+26;
                  int v2= sg? y[c1[x2]]+z[c2[x2]] : y[c1[x2]]-z[c2[x2]]+26;
                  if(v1%26!=v2%26){ok=0;break;}}
                if(!ok)continue;
                unsigned int seen=0;
                for(int r=0;r<nd;r++){int x1=rep[r]; int v=(sg? y[c1[x1]]+z[c2[x1]] : y[c1[x1]]-z[c2[x1]]+26)%26;
                  if(seen&(1u<<v)){ok=0;break;} seen|=1u<<v;}
                if(!ok)continue;
                cons++; hist[ix][L]++;
                report(a,yc,sg,ix,L,q,dir,ne,y,z,S,layer); surv++;
              }
            }
          }
        }
      }
    }
  }
  printf("C %s tests %lld consistent %lld survivors %lld alph=%ld..%ld nperm=%ld lmax=%d minchk=%d\n",lab,tests,cons,surv,lo,hi,nperm_used,LMAX,MINCHK);
  for(int ix=0;ix<2;ix++){printf("H %s ix=%s",lab,XN[ix]);for(int L=1;L<=LMAX;L++)printf(" %d:%lld",L,hist[ix][L]);printf("\n");}
  return 0;
}
