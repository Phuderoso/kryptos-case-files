/* Cycle 243 (PREREG243, I-402): running keys through the 27-cell groups of case 228.
   Groups (as tri242.c): g 0 Z3^3 carry-free base 3, g 1 Z27; forms f 0 V c=p+k, 1 R c=p-k, 2 B c=k-p.
   Plain alphabet X, cipher alphabet Y (cell = index in the alphabet, 0..25; 26 = extra symbol, never carved).
   The 24 crib seats (0-based 21-33, 63-73) give 24 required key cells k_j. A running key is a letter stream;
   a key letter becomes a cell through map M: 0 = its index in X, 1 = its index in Y, 2 = its index in A-Z
   (maps identical as permutations to an earlier map are skipped). Required key letter at seat j = Malpha[k_j]
   (impossible if k_j = 26).
   EXACT part: key letter at plaintext position i = T[(o+i) mod len] for every offset o of every text in the
   texts file (cyclic). Offsets are reached through two 4-letter anchors (seats 0-3 = positions 21-24 and
   seats 13-16 = positions 63-66); a one-error survivor always keeps one anchor intact, so the search is complete
   for viol <= 1. Survivor: viol (mismatched seats) 0 (strict) or 1 (one error).
   HEURISTIC part (unknown English running key): when no k_j is 26, the implied key fragments (13 + 11 letters)
   are scored as the mean log10 quadgram over the 10 + 8 quadgrams (qg.bin). Top lines and a histogram kept.
   usage: rk243 CT Xalpha.bin Yalpha.bin mode texts.txt qg.bin [maxprint] [topH]   mode eq | all
   output: 'S g f x y M text offset viol errseat' survivors; 'D depth count' anchor-depth histogram (descriptive);
           'H score g f x y M frag1 frag2' top lines; 'B bin count' score histogram (bin = floor(score*10)); 'T ...' totals. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *C1="EASTNORTHEAST",*C2="BERLINCLOCK";
static int POS[24],PT[24];
static int ADD[2][27][27],SUB[2][27][27];
static unsigned char* rd(const char*fn,long*n){FILE*f=fopen(fn,"rb");if(!f){perror(fn);exit(1);}fseek(f,0,SEEK_END);long s=ftell(f);rewind(f);
  unsigned char*b=malloc(s);if(fread(b,1,s,f)!=(size_t)s)exit(1);fclose(f);*n=s;return b;}
static int keyof(int g,int f,int p,int c){ return f==0?SUB[g][c][p]: f==1?SUB[g][p][c]: ADD[g][c][p]; }
/* texts */
static int NT; static char NAME[64][64]; static long TLEN[64],TOFF[64]; static unsigned char*TX; static long TTOT;
static long *BHEAD,*BNEXT; /* bucket chains over all 4-gram start positions (global index) */
static float *QG;
#define TOPH 4096
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage\n");return 1;}
  int C[N]; if(strlen(argv[1])!=N){fprintf(stderr,"CT len\n");return 1;} for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  for(int j=0;j<13;j++){POS[j]=21+j;PT[j]=C1[j]-'A';} for(int j=0;j<11;j++){POS[13+j]=63+j;PT[13+j]=C2[j]-'A';}
  for(int a=0;a<27;a++)for(int b=0;b<27;b++){
    int s=0,d=0,m=1; for(int t=0;t<3;t++){int da=(a/m)%3,db=(b/m)%3; s+=((da+db)%3)*m; d+=((da-db+3)%3)*m; m*=3;}
    ADD[0][a][b]=s; SUB[0][a][b]=d; ADD[1][a][b]=(a+b)%27; SUB[1][a][b]=(a-b+27)%27;}
  long nxb,nyb; unsigned char*XA=rd(argv[2],&nxb),*YA=rd(argv[3],&nyb); long nx=nxb/26,ny=nyb/26;
  int eq=!strcmp(argv[4],"eq"); if(eq&&nx!=ny){fprintf(stderr,"eq\n");return 1;}
  long maxprint=argc>7?atol(argv[7]):100000; int topH=argc>8?atoi(argv[8]):50; if(topH>TOPH)topH=TOPH;
  /* texts */
  { FILE*f=fopen(argv[5],"r"); if(!f){perror("texts");return 1;} static char line[1<<20]; char*big=NULL; size_t cap=0; TTOT=0; NT=0;
    char nm[256]; 
    while(fscanf(f,"%255s ",nm)==1){ int ch; long l=0; long start=TTOT;
      while((ch=fgetc(f))!=EOF && ch!='\n'){ if(ch>='A'&&ch<='Z'){ if(TTOT+1>(long)cap){cap=cap?cap*2:1<<20; big=realloc(big,cap);} big[TTOT++]=ch-'A'; l++; } }
      strncpy(NAME[NT],nm,63); TLEN[NT]=l; TOFF[NT]=start; NT++; if(NT>=64)break; }
    fclose(f); TX=(unsigned char*)big; (void)line; }
  BHEAD=malloc(sizeof(long)*456976); for(long i=0;i<456976;i++)BHEAD[i]=-1; BNEXT=malloc(sizeof(long)*TTOT);
  for(int t=0;t<NT;t++){ long L=TLEN[t]; for(long s=L-1;s>=0;s--){ long gi=TOFF[t]+s;
      int code=((TX[TOFF[t]+s]*26+TX[TOFF[t]+(s+1)%L])*26+TX[TOFF[t]+(s+2)%L])*26+TX[TOFF[t]+(s+3)%L];
      BNEXT[gi]=BHEAD[code]; BHEAD[code]=gi; } }
  long qn; unsigned char*qb=rd(argv[6],&qn); if(qn!=456976*4){fprintf(stderr,"qg size\n");return 1;} QG=(float*)qb;
  unsigned char*XI=malloc(nx*26),*YI=malloc(ny*26);
  for(long a=0;a<nx;a++)for(int i=0;i<26;i++)XI[a*26+XA[a*26+i]]=i;
  for(long a=0;a<ny;a++)for(int i=0;i<26;i++)YI[a*26+YA[a*26+i]]=i;
  unsigned char AZ[26]; for(int i=0;i<26;i++)AZ[i]=i;
  long long nconf=0,nimp=0,nsurv[2]={0,0},ncand=0,depth[25]; memset(depth,0,sizeof depth);
  long long hist[100]; memset(hist,0,sizeof hist); long printed=0;
  /* top-H heap (min at [0]) - kept globally under critical */
  static float hs[TOPH]; static char hl[TOPH][128]; int hn=0;
  long npairs=eq?nx:nx*ny;
  #pragma omp parallel for schedule(dynamic,64)
  for(long pi=0;pi<npairs;pi++){
    long x=eq?pi:pi/ny, y=eq?pi:pi%ny;
    const unsigned char*X=XA+x*26,*Y=YA+y*26,*xi=XI+x*26,*yi=YI+y*26;
    const unsigned char*maps[3]={X,Y,AZ}; int use[3]={1,!eq,1};
    if(use[1]&&!memcmp(Y,X,26))use[1]=0;
    if(!memcmp(AZ,X,26)||(use[1]&&!memcmp(AZ,Y,26)))use[2]=0;
    long long lconf=0,limp=0,lsurv[2]={0,0},lcand=0,ldep[25]; memset(ldep,0,sizeof ldep); long long lh[100]; memset(lh,0,sizeof lh);
    char out[64][96]; int no=0; float lhs[8]; char lhl[8][128]; int lhn=0;
    for(int g=0;g<2;g++)for(int f=0;f<3;f++){
      int k[24]; int has26=0;
      for(int j=0;j<24;j++){ k[j]=keyof(g,f,xi[PT[j]],yi[C[POS[j]]]); if(k[j]==26)has26++; }
      for(int M=0;M<3;M++){ if(!use[M])continue; const unsigned char*Ma=maps[M]; lconf++;
        int Lq[24]; for(int j=0;j<24;j++)Lq[j]=k[j]==26?255:Ma[k[j]];
        if(has26>1){limp++;continue;}
        if(has26)limp++;
        /* exact via anchors */
        for(int an=0;an<2;an++){
          int j0=an?13:0; int ok=1; for(int d=0;d<4;d++)if(Lq[j0+d]==255)ok=0; if(!ok)continue;
          int code=((Lq[j0]*26+Lq[j0+1])*26+Lq[j0+2])*26+Lq[j0+3];
          for(long gi=BHEAD[code];gi>=0;gi=BNEXT[gi]){
            int t=0; while(t+1<NT&&TOFF[t+1]<=gi)t++; long L=TLEN[t]; long s=gi-TOFF[t];
            long o=((s-POS[j0])%L+L)%L; const unsigned char*T=TX+TOFF[t];
            if(an==1){ int aok=1; for(int d=0;d<4;d++){ if(Lq[d]==255||T[(o+POS[d])%L]!=Lq[d]){aok=0;break;} } if(aok)continue; }
            int mis=0,es=-1,dep=0; for(int j=0;j<24;j++){ if(T[(o+POS[j])%L]==Lq[j])dep++; else {mis++; es=j;} }
            lcand++; ldep[dep]++;
            if(mis<=1){ lsurv[mis]++; if(no<64) snprintf(out[no++],96,"S %d %d %ld %ld %d %s %ld %d %d\n",g,f,x,y,M,NAME[t],o,mis,mis?es:-1); }
          } }
        /* heuristic */
        if(!has26){ float s=0; for(int j=0;j+3<13;j++){int c=((Lq[j]*26+Lq[j+1])*26+Lq[j+2])*26+Lq[j+3]; s+=QG[c];}
          for(int j=13;j+3<24;j++){int c=((Lq[j]*26+Lq[j+1])*26+Lq[j+2])*26+Lq[j+3]; s+=QG[c];}
          s/=18.0f; int b=(int)((s+10.0f)*10.0f); if(b<0)b=0; if(b>99)b=99; lh[b]++;
          if(s>-5.6f){ /* candidate for global top: keep locally best 8 */
            int slot=-1; if(lhn<8)slot=lhn++; else { int mi=0; for(int q=1;q<8;q++)if(lhs[q]<lhs[mi])mi=q; if(lhs[mi]<s)slot=mi; }
            if(slot>=0){ char f1[14],f2[12]; for(int j=0;j<13;j++)f1[j]='A'+Lq[j]; f1[13]=0; for(int j=0;j<11;j++)f2[j]='A'+Lq[13+j]; f2[11]=0;
              lhs[slot]=s; snprintf(lhl[slot],128,"H %.5f %d %d %ld %ld %d %s %s\n",s,g,f,x,y,M,f1,f2);} } }
      } }
    #pragma omp critical
    { nconf+=lconf; nimp+=limp; nsurv[0]+=lsurv[0]; nsurv[1]+=lsurv[1]; ncand+=lcand; for(int d=0;d<25;d++)depth[d]+=ldep[d]; for(int b=0;b<100;b++)hist[b]+=lh[b];
      for(int b=0;b<no&&printed<maxprint;b++){fputs(out[b],stdout);printed++;}
      for(int q=0;q<lhn;q++){ if(hn<topH){hs[hn]=lhs[q];strcpy(hl[hn],lhl[q]);hn++;} else { int mi=0; for(int r=1;r<hn;r++)if(hs[r]<hs[mi])mi=r; if(hs[mi]<lhs[q]){hs[mi]=lhs[q];strcpy(hl[mi],lhl[q]);} } } }
  }
  /* sort top lines descending */
  for(int a=0;a<hn;a++)for(int b=a+1;b<hn;b++)if(hs[b]>hs[a]){float t=hs[a];hs[a]=hs[b];hs[b]=t;char tmp[128];strcpy(tmp,hl[a]);strcpy(hl[a],hl[b]);strcpy(hl[b],tmp);}
  for(int a=0;a<hn;a++)fputs(hl[a],stdout);
  for(int d=0;d<25;d++)if(depth[d])printf("D %d %lld\n",d,depth[d]);
  for(int b=0;b<100;b++)if(hist[b])printf("B %d %lld\n",b-100,hist[b]);
  printf("T confs %lld one26_or_more %lld cand %lld strict %lld one %lld texts %d letters %ld\n",nconf,nimp,ncand,nsurv[0],nsurv[1],NT,TTOT);
  return 0;}
