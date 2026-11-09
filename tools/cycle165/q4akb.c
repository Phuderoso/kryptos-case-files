/* Cycle 165 (IDEAS I-074): q4akb = cycle-164 q4ak with PERMUTATION BLOCKING (tables reused across a block of
   BLK permutations, so the 9,506 x 6 tables are streamed once per block instead of once per permutation).
   Tests, histograms and survivor rule are identical to q4ak (same C/H/S line formats; S-line order may differ).
   Original header follows.
   Cycle 164 (IDEAS I-015): Quagmire I/II/IV autokey with two DIFFERENT keyed alphabets.
   Plain alphabet X (list 1), cipher alphabet Y (list 2), X != Y; key letter read through Z in {X, Y}.
   Encryption at key index q (layer order):  Vig  c = Y[x(p) + z(k)];  Beau c = Y[z(k) - x(p)];  Var c = Y[x(p) - z(k)]
   PT-fed: k_q = layer plaintext at q-L (q >= L), else primer;  CT-fed: k_q = layer ciphertext at q-L.
   Any primer of length L is tested (cribs fix it or constrain the chain).  Exact.
   Orders: ix=0 key at the plaintext index, then transpose (model Q); ix=1 transpose first, key at the carved index.
   PT-fed check: two cribs on one residue class mod L, chain p -> D[c][p] through the carved letters between them.
   CT-fed check: crib at q >= L must satisfy D[c_q][c_{q-L}] == p.
   D[c][k] = decrypted plaintext letter for cipher letter c and key letter k (one 26x26 table per pair, Z, form).
   usage: q4ak CT plain.txt cipher.txt perms.bin|x label plo phi pstep LMAX [recount]
     perms processed: entries plo, plo+pstep, ... < phi (both directions).  'x' = direct (identity, one order).
   Output: S lines (survivors: consistent with >= MINCHK checks, decrypted), H histograms, C totals. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define MAXA 12000
#define MINCHK 6
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static int Plet[24], C[N];
static char W1[MAXA][40], W2[MAXA][40];
static unsigned char A1[MAXA][26],I1[MAXA][26],A2[MAXA][26],I2[MAXA][26];
static void keyed(const char*w,unsigned char*al,unsigned char*in){int u[26]={0},n=0;
 for(const char*p=w;*p;p++){int c=*p-'A';if(c<0||c>25||u[c])continue;u[c]=1;al[n++]=c;}
 for(int c=0;c<26;c++)if(!u[c])al[n++]=c; for(int i=0;i<26;i++)in[al[i]]=i;}
static int readlist(const char*fn,char W[][40],unsigned char A[][26],unsigned char I[][26]){
 FILE*f=fopen(fn,"r"); if(!f){perror(fn);exit(1);} int n=0; char b[64];
 while(n<MAXA&&fscanf(f,"%63s",b)==1){ if(!strcmp(b,"AZ"))b[0]=0; unsigned char al[26],in[26]; keyed(b,al,in);
   int dup=0; for(int i=0;i<n;i++) if(!memcmp(A[i],al,26)){dup=1;break;} if(dup)continue;
   strncpy(W[n],b[0]?b:"AZ",39); memcpy(A[n],al,26); memcpy(I[n],in,26); n++; }
 fclose(f); return n;}
/* structure for one (order, L) */
typedef struct { int npt, nct, chk_pt, chk_ct; unsigned short off; } St;
#define BLK 64
#define LM 27
static unsigned char pool[2][33][24*100]; static unsigned char bpool[BLK][2][LM][256]; static unsigned char bctp[BLK][2][LM][72]; static St bst[BLK][2][LM]; static short bS[BLK][N]; static long bq[BLK]; static int bdir[BLK]; /* PT chains: [n][p0][target][c1..cn] sorted by n; CT: [c][k][p] */
static unsigned char ctp[2][33][24*3];
static St st[2][33];
static int kpo[2][24]; static int lay[2][N];
static void build(int ix,int L){
 int *kp=kpo[ix]; int ord[24]; for(int t=0;t<24;t++)ord[t]=t;
 for(int a=1;a<24;a++){int t=ord[a],b=a;while(b>0&&kp[ord[b-1]]>kp[t]){ord[b]=ord[b-1];b--;}ord[b]=t;}
 int last[40]; for(int r=0;r<L;r++)last[r]=-1;
 int occ=0,nct=0; int cn[24],ca[24],cb[24],nc=0;
 unsigned char *ct=ctp[ix][L];
 for(int i=0;i<24;i++){int t=ord[i],j=kp[t],r=j%L;
   if(last[r]>=0){ca[nc]=last[r];cb[nc]=t;cn[nc]=(j-kp[last[r]])/L;nc++;} else occ++;
   last[r]=t;
   if(j>=L){ct[3*nct]=lay[ix][j];ct[3*nct+1]=lay[ix][j-L];ct[3*nct+2]=Plet[t];nct++;}}
 /* sort checks by chain length */
 for(int a=1;a<nc;a++){int x=cn[a],y=ca[a],z=cb[a],b=a;while(b>0&&cn[b-1]>x){cn[b]=cn[b-1];ca[b]=ca[b-1];cb[b]=cb[b-1];b--;}cn[b]=x;ca[b]=y;cb[b]=z;}
 unsigned char *p=pool[ix][L]; int o=0;
 for(int k=0;k<nc;k++){p[o++]=cn[k];p[o++]=Plet[ca[k]];p[o++]=Plet[cb[k]];int pos=kp[ca[k]];
   for(int s=0;s<cn[k];s++){pos+=L;p[o++]=lay[ix][pos];}}
 st[ix][L].npt=nc; st[ix][L].nct=nct; st[ix][L].chk_pt=24-occ; st[ix][L].chk_ct=nct;}
static const char*FN[3]={"vig","beau","var"}, *ZN[2]={"zX","zY"}, *XN[2]={"pt","carved"};
static const char*lab;
static void report(int feed,int a,int b,int z,int f,int ix,int L,long q,int dir,int chk,const unsigned char*D,const short*S){
 /* full decrypt in layer order */
 int T[N]; for(int i=0;i<N;i++)T[i]=-1; int *kp=kpo[ix],*ly=lay[ix];
 if(feed){ for(int j=L;j<N;j++)T[j]=D[ly[j]*26+ly[j-L]]; for(int t=0;t<24;t++) if(kp[t]<L) T[kp[t]]=Plet[t]; }
 else { /* inverse: given p at q and c at q, key letter k with D[c][k]==p */
  for(int t=0;t<24;t++){int j=kp[t]; if(T[j]>=0)continue; T[j]=Plet[t]; int v=Plet[t],pos=j;
   while(pos+L<N){v=D[ly[pos+L]*26+v];pos+=L;T[pos]=v;}
   pos=j;v=Plet[t]; while(pos>=L){int k=-1;for(int x=0;x<26;x++)if(D[ly[pos]*26+x]==v){k=x;break;} pos-=L; v=k; T[pos]=v;}}}
 char ps[N+1];ps[N]=0;int full=1;
 for(int i=0;i<N;i++){int src=ix?S[i]:i; if(T[src]<0){ps[i]='?';full=0;} else ps[i]='A'+T[src];}
 int ok=1; for(int t=0;t<24;t++) if(ps[CI[t]]!=PT[t]) ok=0;
 printf("S %s feed=%s X=%s Y=%s %s %s ix=%s L=%d perm=%ld dir=%d checks=%d crib24=%s %s=%s\n",lab,feed?"CT":"PT",W1[a],W2[b],ZN[z],FN[f],XN[ix],L,q,dir,chk,ok?"ok":"FAIL",full?"plain":"partial",ps);}
static void setperm(const short*S){for(int t=0;t<24;t++){kpo[0][t]=CI[t]; kpo[1][t]=S[CI[t]];} for(int i=0;i<N;i++){lay[0][i]=C[S[i]]; lay[1][i]=C[i];}}
int main(int argc,char**argv){
 if(argc<10){fprintf(stderr,"usage\n");return 1;}
 for(int i=0;i<N;i++)C[i]=argv[1][i]-'A'; for(int t=0;t<24;t++)Plet[t]=PT[t]-'A';
 int n1=readlist(argv[2],W1,A1,I1), n2=readlist(argv[3],W2,A2,I2);
 lab=argv[5]; long plo=atol(argv[6]),phi=atol(argv[7]),pst=atol(argv[8]); int LMAX=atoi(argv[9]); int recount=argc>10;
 int direct=!strcmp(argv[4],"x"); long np=1; short*Perm=NULL;
 if(!direct){FILE*pf=fopen(argv[4],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
  Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 1; fclose(pf);}
 if(phi>np)phi=np;
 /* pair list and tables */
 int npair=0; int *pa=malloc(sizeof(int)*n1*n2),*pb=malloc(sizeof(int)*n1*n2);
 for(int a=0;a<n1;a++)for(int b=0;b<n2;b++) if(memcmp(A1[a],A2[b],26)){pa[npair]=a;pb[npair]=b;npair++;}
 unsigned char *TB=malloc((size_t)npair*6*676);
 for(int k=0;k<npair;k++){const unsigned char*X=A1[pa[k]],*xi=I1[pa[k]],*yi=I2[pb[k]];
  for(int z=0;z<2;z++){const unsigned char*zi=z?I2[pb[k]]:xi;
   for(int f=0;f<3;f++){unsigned char*D=TB+((size_t)k*6+z*3+f)*676;
    for(int c=0;c<26;c++)for(int kk=0;kk<26;kk++){int r=f==0?yi[c]-zi[kk]:f==1?zi[kk]-yi[c]:yi[c]+zi[kk]; D[c*26+kk]=X[((r%26)+26)%26];}}}}
 static long long hist[2][2][3][2][41]; static long long tests=0,cons=0,surv=0;
 int nord=direct?1:2;

 if(LMAX>=LM){fprintf(stderr,"LMAX<=26\n");return 1;}
 long items=0; for(long q=plo;q<phi;q+=pst) items++; items*= (direct?1:2);
 for(long it0=0;it0<items;it0+=BLK){ int nb=(int)((items-it0)<BLK?(items-it0):BLK);
  for(int b=0;b<nb;b++){ long it=it0+b; int dir=direct?0:(int)(it%2); long q=plo+(direct?it:it/2)*pst; bq[b]=q; bdir[b]=dir;
   short*S=bS[b]; if(direct) for(int i=0;i<N;i++)S[i]=i; else { const short*s=Perm+q*N; if(dir) for(int i=0;i<N;i++)S[s[i]]=i; else memcpy(S,s,2*N);}
   for(int t=0;t<24;t++){kpo[0][t]=CI[t]; kpo[1][t]=S[CI[t]];}
   for(int i=0;i<N;i++){lay[0][i]=C[S[i]]; lay[1][i]=C[i];}
   for(int ix=0;ix<nord;ix++) for(int L=1;L<=LMAX;L++){ build(ix,L); bst[b][ix][L]=st[ix][L];
     memcpy(bctp[b][ix][L],ctp[ix][L],72);
     /* pool length */ const unsigned char*p=pool[ix][L]; int o=0; for(int i=0;i<st[ix][L].npt;i++) o+=3+p[o];
     if(o>256){fprintf(stderr,"pool overflow %d\n",o);return 1;} memcpy(bpool[b][ix][L],p,o);} }
  for(int k=0;k<npair;k++) for(int zf=0;zf<6;zf++){ const unsigned char*D=TB+((size_t)k*6+zf)*676;
   for(int b=0;b<nb;b++) for(int ix=0;ix<nord;ix++) for(int L=1;L<=LMAX;L++){ St*s=&bst[b][ix][L]; tests+=2;
    const unsigned char*ct=bctp[b][ix][L]; int ok=1;
    for(int i=0;i<s->nct;i++) if(D[ct[3*i]*26+ct[3*i+1]]!=ct[3*i+2]){ok=0;break;}
    if(ok){cons++;hist[1][zf/3][zf%3][ix][L]++; if(s->chk_ct>=MINCHK||recount){surv++; if(!recount){setperm(bS[b]);report(1,pa[k],pb[k],zf/3,zf%3,ix,L,bq[b],bdir[b],s->chk_ct,D,bS[b]);}}}
    const unsigned char*p=bpool[b][ix][L]; ok=1;
    for(int i=0;i<s->npt;i++){int n=p[0],v=p[1]; for(int j=0;j<n;j++) v=D[p[3+j]*26+v]; if(v!=p[2]){ok=0;break;} p+=3+n;}
    if(ok){cons++;hist[0][zf/3][zf%3][ix][L]++; if(s->chk_pt>=MINCHK||recount){surv++; if(!recount){setperm(bS[b]);report(0,pa[k],pb[k],zf/3,zf%3,ix,L,bq[b],bdir[b],s->chk_pt,D,bS[b]);}}}
   }}
 }
 printf("C %s tests %lld consistent %lld reported %lld pairs %d (n1 %d n2 %d) perms %ld..%ld step %ld lmax %d direct %d\n",lab,tests,cons,surv,npair,n1,n2,plo,phi,pst,LMAX,direct);
 for(int fe=0;fe<2;fe++)for(int z=0;z<2;z++)for(int f=0;f<3;f++)for(int ix=0;ix<nord;ix++){
  printf("H %s feed=%s %s %s ix=%s",lab,fe?"CT":"PT",ZN[z],FN[f],XN[ix]); for(int L=1;L<=LMAX;L++)printf(" %lld",hist[fe][z][f][ix][L]); printf("\n");}
 return 0;}
