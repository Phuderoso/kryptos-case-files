/* Cycle 242 (PREREG242, I-399): 27-cell additive substitutions on keyed alphabets.
   A letter's index i (0..25) in its keyed alphabet is a cell of a 27-cell group:
     g 0  Z3^3 carry-free ("ternary Vigenere"): i -> 3 base-3 digits, digit-wise addition mod 3 (no carries);
     g 1  Z27 (ordinary addition mod 27, one extra symbol = cell 26).
   Plain alphabet X, cipher alphabet Y (index = position of the letter in the alphabet). Forms:
     f 0 V  c = p + k      f 1 R  c = p - k      f 2 B  c = k - p     (group operations; key k is a cell 0..26)
   The 24 crib seats (EASTNORTHEAST 0-based 21-33, BERLINCLOCK 63-73) give 24 required key cells k_j (key-agnostic).
   Models (direct, key on plaintext index):
     PER P  : periodic key, P 1..48; viol = sum over residue classes of (size - max multiplicity); strict viol 0, one-error viol <= 1.
     CA L,M : ciphertext autokey, key cell at i = index_M(c[i-L]) (M 0 = X map, 1 = Y map), L 1..48; seats with i-L < 0 unconstrained;
              one-error = all violated seats explained by one wrong carved letter (seat q and seat q+L).
     PA L,M : plaintext autokey, key cell at i = index_M(p[i-L]); constraints only where i-L is also a crib seat, L 1..60;
              one-error = all violated constraints share one seat.
   usage: tri242 CT Xalpha.bin Yalpha.bin mode [maxprint]   mode: eq (x = y), all (all pairs)
   output (printed only for PER with >= 6 constraints, all CA, PA ncons>=6): 'S model g f x y par M viol ncons' survivor lines (viol <= 1); 'T ...' totals line. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *C1="EASTNORTHEAST",*C2="BERLINCLOCK";
static int POS[24],PT[24],ISCRIB[N],SEAT[N];
static int ADD[2][27][27],SUB[2][27][27];
static unsigned char* rd(const char*fn,long*n){FILE*f=fopen(fn,"rb");if(!f){perror(fn);exit(1);}fseek(f,0,SEEK_END);long s=ftell(f);rewind(f);
  unsigned char*b=malloc(s);if(fread(b,1,s,f)!=(size_t)s)exit(1);fclose(f);*n=s/26;return b;}
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 1;}
  int C[N]; if(strlen(argv[1])!=N){fprintf(stderr,"CT len\n");return 1;} for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  for(int i=0;i<N;i++){ISCRIB[i]=0;SEAT[i]=-1;}
  for(int j=0;j<13;j++){POS[j]=21+j;PT[j]=C1[j]-'A';} for(int j=0;j<11;j++){POS[13+j]=63+j;PT[13+j]=C2[j]-'A';}
  for(int j=0;j<24;j++){ISCRIB[POS[j]]=1;SEAT[POS[j]]=j;}
  for(int a=0;a<27;a++)for(int b=0;b<27;b++){
    int s=0,d=0,m=1; for(int t=0;t<3;t++){int da=(a/m)%3,db=(b/m)%3; s+=((da+db)%3)*m; d+=((da-db+3)%3)*m; m*=3;}
    ADD[0][a][b]=s; SUB[0][a][b]=d; ADD[1][a][b]=(a+b)%27; SUB[1][a][b]=(a-b+27)%27;}
  long nx,ny; unsigned char*XA=rd(argv[2],&nx),*YA=rd(argv[3],&ny); int eq=!strcmp(argv[4],"eq"); long maxprint=argc>5?atol(argv[5]):100000;
  if(eq&&nx!=ny){fprintf(stderr,"eq needs same list\n");return 1;}
  unsigned char*XI=malloc(nx*26),*YI=malloc(ny*26);
  for(long a=0;a<nx;a++)for(int i=0;i<26;i++)XI[a*26+XA[a*26+i]]=i;
  for(long a=0;a<ny;a++)for(int i=0;i<26;i++)YI[a*26+YA[a*26+i]]=i;
  /* PA constraint lists per L: pairs (seat j, seat jj) with POS[j]-L == POS[jj] */
  static int pac[61][24][2],pan[61],nP[49];
  for(int P=1;P<=48;P++){int seen[48]={0},d=0; for(int j=0;j<24;j++){if(!seen[POS[j]%P]){seen[POS[j]%P]=1;d++;}} nP[P]=24-d;}
  for(int L=1;L<=60;L++){pan[L]=0; for(int j=0;j<24;j++){int q=POS[j]-L; if(q>=0&&ISCRIB[q]){pac[L][pan[L]][0]=j;pac[L][pan[L]][1]=SEAT[q];pan[L]++;}}}
  long long npf=0,sPER[49][2],sCA[49][2][2],sPA[61][2][2]; memset(sPER,0,sizeof sPER);memset(sCA,0,sizeof sCA);memset(sPA,0,sizeof sPA);
  long long printed=0;
  long ntot=eq?nx:nx*ny;
  #pragma omp parallel for schedule(dynamic,64)
  for(long t=0;t<ntot;t++){
    long x=eq?t:t/ny, y=eq?t:t%ny;
    int px[24],cy[24]; for(int j=0;j<24;j++){px[j]=XI[x*26+PT[j]]; cy[j]=YI[y*26+C[POS[j]]];}
    long long lPER[49][2],lCA[49][2][2],lPA[61][2][2]; memset(lPER,0,sizeof lPER);memset(lCA,0,sizeof lCA);memset(lPA,0,sizeof lPA);
    char buf[64][96]; int nb=0;
    for(int g=0;g<2;g++)for(int f=0;f<3;f++){
      int k[24]; for(int j=0;j<24;j++){ k[j]= f==0?SUB[g][cy[j]][px[j]] : f==1?SUB[g][px[j]][cy[j]] : ADD[g][cy[j]][px[j]]; }
      for(int P=1;P<=48;P++){ int viol=0; int done[24]={0};
        for(int j=0;j<24&&viol<=1;j++){ if(done[j])continue; int cnt[27]={0},sz=0,mx=0;
          for(int jj=j;jj<24;jj++) if(POS[jj]%P==POS[j]%P){done[jj]=1;sz++; if(++cnt[k[jj]]>mx)mx=cnt[k[jj]];}
          viol+=sz-mx; }
        if(viol<=1){ lPER[P][viol]++; if(nb<64&&nP[P]>=6) snprintf(buf[nb++],96,"S PER %d %d %ld %ld %d - %d -\n",g,f,x,y,P,viol); } }
      for(int M=0;M<2;M++){ const unsigned char*MI=M?YI+y*26:XI+x*26;
        for(int L=1;L<=48;L++){ int viol=0,nc=0,bad[24],nbad=0;
          for(int j=0;j<24&&nbad<=2;j++){int q=POS[j]-L; if(q<0)continue; nc++; if(MI[C[q]]!=k[j])bad[nbad++]=j;}
          /* one carved error at position q spoils seat q (as cipher) and seat q+L (as key): v 1 iff all bad seats explained by one q */
          if(nbad==0)viol=0; else if(nbad>2)viol=2; else if(nbad==1)viol=1; else viol=(POS[bad[1]]-L==POS[bad[0]])?1:2;
          if(viol<=1){ lCA[L][M][viol]++; if(nb<64) snprintf(buf[nb++],96,"S CA %d %d %ld %ld %d %d %d %d\n",g,f,x,y,L,M,viol,nc);} }
        for(int L=1;L<=60;L++){ if(!pan[L])continue; int bad[24],nbad=0;
          for(int c=0;c<pan[L];c++){int j=pac[L][c][0],jj=pac[L][c][1]; if(MI[PT[jj]]!=k[j]) bad[nbad++]=c;}
          int v; if(nbad==0)v=0; else { v=2; for(int s=0;s<24&&v==2;s++){int ok=1; for(int b=0;b<nbad;b++){int j=pac[L][bad[b]][0],jj=pac[L][bad[b]][1]; if(j!=s&&jj!=s){ok=0;break;}} if(ok)v=1;} }
          if(v<=1){ lPA[L][M][v]++; if(nb<64&&pan[L]>=6) snprintf(buf[nb++],96,"S PA %d %d %ld %ld %d %d %d %d\n",g,f,x,y,L,M,v,pan[L]);} } }
    }
    #pragma omp critical
    { npf+=6; for(int P=1;P<=48;P++)for(int v=0;v<2;v++)sPER[P][v]+=lPER[P][v];
      for(int L=1;L<=48;L++)for(int M=0;M<2;M++)for(int v=0;v<2;v++)sCA[L][M][v]+=lCA[L][M][v];
      for(int L=1;L<=60;L++)for(int M=0;M<2;M++)for(int v=0;v<2;v++)sPA[L][M][v]+=lPA[L][M][v];
      for(int b=0;b<nb&&printed<maxprint;b++){fputs(buf[b],stdout);printed++;} }
  }
  printf("T pairforms %lld\n",npf);
  for(int P=1;P<=48;P++)printf("T PER %d ncons %d strict %lld one %lld\n",P,nP[P],sPER[P][0],sPER[P][1]);
  for(int L=1;L<=48;L++)for(int M=0;M<2;M++)printf("T CA %d %d strict %lld one %lld\n",L,M,sCA[L][M][0],sCA[L][M][1]);
  for(int L=1;L<=60;L++)for(int M=0;M<2;M++) if(pan[L]) printf("T PA %d %d ncons %d strict %lld one %lld\n",L,M,pan[L],sPA[L][M][0],sPA[L][M][1]);
  return 0;}
