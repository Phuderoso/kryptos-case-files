/* Cycle 77: coordinate key ("abscissa + ordinate") behind transpositions.
   Plaintext written row-major into a w-column grid starting at column offset o; each cell's key
   k = a[col] + b[row] (mod 26, tableau index space), a = column (abscissa) key, b = row (ordinate) key,
   both arbitrary. Equivalent: reading the key off a Vigenere/KRYPTOS tableau at (row word, column word).
   Model A: key indexed by plaintext position, then transposition. Model B: transposition first, then
   the coordinate key over the carved order. Exact union-find with offsets on the 24 crib equations.
   modes: 0 Vigenere c=p+k, 1 Beaufort c=k-p (variant c=p-k has the same consistency as Vigenere).
   usage: coord77 CARVED perms.bin alph.bin nalph minchecks [endperm [startperm]]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
static int m26(int x){x%=26;return x<0?x+26:x;}
static int par[160],pot[160]; /* pot[u]=val(u)-val(par[u]) */
static int findc(int u,int*pu){int s=0,x=u; while(par[x]!=x){s+=pot[x];x=par[x];} *pu=m26(s); 
  /* compress */ int y=u,acc=m26(s); while(par[y]!=y){int nx=par[y],py=pot[y]; par[y]=x; pot[y]=acc; acc=m26(acc-py); y=nx;} return x;}
long hist[2][25];
int main(int argc,char**argv){
  const char*carved=argv[1]; int nal=atoi(argv[4]),minck=atoi(argv[5]);
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); rewind(f);
  int np=sz/(2*N); short*perms=malloc(sz); if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1; fclose(f);
  int p0=0; if(argc>6){int m=atoi(argv[6]); if(m<np)np=m;} if(argc>7)p0=atoi(argv[7]);
  unsigned char*AL=malloc(26*nal); f=fopen(argv[3],"rb"); if(fread(AL,26,nal,f)!=(size_t)nal)return 2; fclose(f);
  int cpos[24],cpl[24]; for(int j=0;j<13;j++){cpos[j]=21+j;cpl[j]=CR1[j]-'A';} for(int j=0;j<11;j++){cpos[13+j]=63+j;cpl[13+j]=CR2[j]-'A';}
  long tests=0,cons=0,hits=0;
  for(int pi=p0;pi<np;pi++){short*P=perms+(long)pi*N;
   for(int t=0;t<nal;t++){unsigned char*A=AL+26*t; int inv[26]; for(int i=0;i<26;i++)inv[A[i]]=i;
    int X[24],Pl[24]; for(int j=0;j<24;j++){X[j]=inv[carved[P[cpos[j]]]-'A'];Pl[j]=inv[cpl[j]];}
    for(int mode=0;mode<2;mode++){int K[24]; for(int j=0;j<24;j++)K[j]=mode==0?m26(X[j]-Pl[j]):m26(X[j]+Pl[j]);
     for(int model=0;model<2;model++){ if(model==1&&pi==0)continue; /* identity: B == A */
      int idx[24]; for(int j=0;j<24;j++)idx[j]=model==0?cpos[j]:P[cpos[j]];
      for(int w=2;w<=48;w++) for(int o=0;o<w;o++){ tests++;
        int R=(96+o)/w+1; for(int u=0;u<w+R;u++){par[u]=u;pot[u]=0;}
        int ok=1,ck=0;
        for(int j=0;j<24&&ok;j++){int q=idx[j]+o,c=q%w,r=w+q/w; int pc,pr; int rc=findc(c,&pc),rr=findc(r,&pr);
          /* want val(c)-val(r)=K */
          if(rc==rr){ if(m26(pc-pr)!=K[j])ok=0; else ck++; }
          else { /* attach rc under rr: val(rc)-val(rr) = K - pc + pr */ par[rc]=rr; pot[rc]=m26(K[j]-pc+pr);} }
        if(ok){cons++; hist[model][ck]++; if(ck>=minck){hits++; printf("HIT perm=%d alph=%d mode=%d model=%c w=%d o=%d checks=%d\n",pi,t,mode,model?'B':'A',w,o,ck);}}
      }}}}}
  fprintf(stderr,"perms=%d tests=%ld consistent=%ld hits=%ld\n",np,tests,cons,hits);
  for(int m=0;m<2;m++){printf("HIST model=%c",m?'B':'A'); for(int c=0;c<25;c++)printf(" %ld",hist[m][c]); printf("\n");}
  return 0;}
