/* Cycle 212 (I-284): word-restart key R1 on two-keyword Quagmire tableaux over a full alphabet LIST (e.g. the 144 themed alphabets),
   behind a transposition family (model Q: layer letter i = C[S[i]]), by a hash join on crib key-class difference vectors.
   Same model, segmentations, offsets, forms and survivor definition as cycle 210's wrq.c (case 197):
     Vigenere-form c = Y[x(p)+k] (variant = same consistency, counted once); Beaufort-form c = Y[k - x(p)].
   A configuration (L, segE, o1, segB, o2) partitions the 24 crib positions into key classes (equal key index).
   Survivor <=> inside every class:  y(c_j) - y(c_j0) = x(p_j) - x(p_j0)  (vig)   or   = -(x(p_j) - x(p_j0))  (beau).
   The left side depends only on (row, dir, Y), the right side only on (config, X, form): so per configuration the 2*nA plaintext-side
   target vectors are bucketed by their first two constraint values, and per (row, dir) every Y is looked up once per group of
   configurations that share those two constraints (alphabet-free pre-check first: equal plain letters in a class need equal cipher letters).
   Exact: every allowed (X, Y, form) is decided for every configuration; nothing is sampled except by stride/offset on rows.
   usage: wrj CT perms.bin|x LMIN LMAX alphabets.txt pairs.txt|all stride offset [maxprint]
     pairs.txt: "ix iy" lines (allowed ordered pairs); 'all' = every ordered pair except identical AZ/AZ (0,0) and KA/KA (1,1).
   output as wrq: 'S' lines, 'H L count', 'P ix iy form L count', 'T' totals. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define NA_MAX 160
static const char *C1="EASTNORTHEAST", *C2="BERLINCLOCK";
static const int P1=21, P2=63;
static const int SE[4][3]={{0},{1,4},{1,9},{2,4,9}};
static const char *SEN[4]={"EASTNORTHEAST","EAST|NORTHEAST","EASTNORTH|EAST","EAST|NORTH|EAST"};
static const int SB[2][2]={{0},{1,6}};
static const char *SBN[2]={"BERLINCLOCK","BERLIN|CLOCK"};
static int cidx(const int *b,int nb,int j,int o,int L){int pb=-1;for(int k=0;k<nb;k++)if(b[k]<=j)pb=b[k];return ((pb>=0)?(j-pb):(o+j))%L;}
static char AL[NA_MAX][27]; static int INV[NA_MAX][26]; static int na; static unsigned char ALLOW[NA_MAX][NA_MAX];
static int PT[24];
typedef struct { int L,s1,o1,s2,o2; int cls[24]; int nz; int za[24],zb[24]; int nd; int da[24],db[24]; int grp; unsigned char *tgt; /* [2*na][nd] */ } Cfg;
typedef struct { int nt; int a1,b1,a2,b2; int *bstart; int *bent; } Grp; /* buckets: 26^nt; entries = xf = X*2+f */
static Cfg *cf; static int ncf; static Grp *gr; static int ngr;
static int find_grp(int nt,int a1,int b1,int a2,int b2){
  for(int g=0;g<ngr;g++) if(gr[g].nt==nt&&gr[g].a1==a1&&gr[g].b1==b1&&gr[g].a2==a2&&gr[g].b2==b2) return g; return -1;}
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  int C[N]; for(int i=0;i<N;i++)C[i]=argv[1][i]-'A';
  int LMIN=atoi(argv[3]),LMAX=atoi(argv[4]); int stride=atoi(argv[7]),off=atoi(argv[8]); long maxprint=argc>9?atol(argv[9]):100;
  FILE*fa=fopen(argv[5],"r"); char line[256];
  while(fgets(line,sizeof line,fa)){ if(strlen(line)<26)continue; memcpy(AL[na],line,26); AL[na][26]=0;
    int seen=0; for(int i=0;i<26;i++){int v=AL[na][i]-'A'; if(v<0||v>25||(seen>>v&1)){fprintf(stderr,"bad alphabet %d\n",na);return 1;} seen|=1<<v; INV[na][v]=i;} na++; }
  fclose(fa);
  if(!strcmp(argv[6],"all")){ for(int x=0;x<na;x++)for(int y=0;y<na;y++)ALLOW[x][y]=!(x==y&&x<2); }
  else { FILE*fp=fopen(argv[6],"r"); int a,b; while(fscanf(fp,"%d %d",&a,&b)==2)ALLOW[a][b]=1; fclose(fp); }
  for(int j=0;j<13;j++)PT[j]=C1[j]-'A'; for(int j=0;j<11;j++)PT[13+j]=C2[j]-'A';
  /* configurations */
  int cap=0; for(int L=LMIN;L<=LMAX;L++)cap+=8*L*L; cf=calloc(cap,sizeof(Cfg)); gr=calloc(cap,sizeof(Grp));
  for(int L=LMIN;L<=LMAX;L++)for(int s1=0;s1<4;s1++)for(int o1=0;o1<L;o1++)for(int s2=0;s2<2;s2++)for(int o2=0;o2<L;o2++){
    Cfg*c=&cf[ncf++]; c->L=L;c->s1=s1;c->o1=o1;c->s2=s2;c->o2=o2;
    for(int j=0;j<13;j++)c->cls[j]=cidx(SE[s1]+1,SE[s1][0],j,o1,L);
    for(int j=0;j<11;j++)c->cls[13+j]=cidx(SB[s2]+1,SB[s2][0],j,o2,L);
    int first[32]; for(int k=0;k<32;k++)first[k]=-1;
    for(int j=0;j<24;j++){int k=c->cls[j]; if(first[k]<0){first[k]=j;continue;} int j0=first[k];
      if(PT[j]==PT[j0]){c->za[c->nz]=j;c->zb[c->nz++]=j0;} else {c->da[c->nd]=j;c->db[c->nd++]=j0;}}
    /* target vectors over constraints (all nd, the first min(nd,2) define the group) */
    c->tgt=malloc((size_t)2*na*(c->nd?c->nd:1));
    for(int x=0;x<na;x++)for(int f=0;f<2;f++)for(int t=0;t<c->nd;t++){
      int d=(INV[x][PT[c->da[t]]]-INV[x][PT[c->db[t]]]+26)%26; c->tgt[(size_t)(x*2+f)*c->nd+t]=f?(26-d)%26:d;}
    int nt=c->nd<2?c->nd:2; int a1=nt>0?c->da[0]:-1,b1=nt>0?c->db[0]:-1,a2=nt>1?c->da[1]:-1,b2=nt>1?c->db[1]:-1;
    int g=find_grp(nt,a1,b1,a2,b2);
    if(g<0){ g=ngr++; Grp*G=&gr[g]; G->nt=nt;G->a1=a1;G->b1=b1;G->a2=a2;G->b2=b2;
      int nb=nt==0?1:nt==1?26:676; G->bstart=calloc(nb+1,sizeof(int)); G->bent=malloc(sizeof(int)*2*na);
      int *key=malloc(sizeof(int)*2*na);
      for(int xf=0;xf<2*na;xf++){ int k=0; if(nt>0)k=c->tgt[(size_t)xf*c->nd]; if(nt>1)k=k*26+c->tgt[(size_t)xf*c->nd+1]; key[xf]=k; G->bstart[k+1]++; }
      for(int b=0;b<nb;b++)G->bstart[b+1]+=G->bstart[b];
      int *fill=calloc(nb,sizeof(int)); for(int xf=0;xf<2*na;xf++){int k=key[xf]; G->bent[G->bstart[k]+fill[k]++]=xf;}
      free(fill); free(key); }
    c->grp=g; }
  fprintf(stderr,"alphabets %d configs %d groups %d\n",na,ncf,ngr);
  int direct=!strcmp(argv[2],"x"); long np=1; short*Perm=NULL;
  if(!direct){FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);
    Perm=malloc(np*N*2); if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 1; fclose(pf);}
  size_t HS=(size_t)na*na*2*27; long long *ph=calloc(HS,sizeof(long long)); long long printed=0, rows=0;
  int nd=direct?1:2;
  #pragma omp parallel reduction(+:rows)
  {
   long long *lh=calloc(HS,sizeof(long long));
   int *gstamp=calloc(ngr,sizeof(int)), *gofs=calloc(ngr,sizeof(int)), *gcnt=calloc(ngr,sizeof(int)); int stamp=0;
   size_t ccap=1<<20; int *cand=malloc(sizeof(int)*ccap); /* packed Y<<16 | xf */
   #pragma omp for schedule(dynamic,16)
   for(long q=0;q<np;q++){
    if(!direct && q%stride!=off) continue; rows++;
    for(int dir=0;dir<nd;dir++){
     short S[N];
     if(direct){for(int i=0;i<N;i++)S[i]=i;}
     else{const short*s=Perm+q*N; if(dir){for(int i=0;i<N;i++)S[s[i]]=i;} else memcpy(S,s,2*N);}
     int c[24]; for(int j=0;j<13;j++)c[j]=C[S[P1+j]]; for(int j=0;j<11;j++)c[13+j]=C[S[P2+j]];
     static __thread unsigned char w[NA_MAX][24];
     for(int y=0;y<na;y++)for(int j=0;j<24;j++)w[y][j]=INV[y][c[j]];
     stamp++; size_t used=0;
     for(int ci=0;ci<ncf;ci++){
      const Cfg*K=&cf[ci]; int ok=1;
      for(int z=0;z<K->nz;z++) if(c[K->za[z]]!=c[K->zb[z]]){ok=0;break;}
      if(!ok)continue;
      int g=K->grp; const Grp*G=&gr[g];
      if(gstamp[g]!=stamp){ gstamp[g]=stamp; gofs[g]=used;
        for(int y=0;y<na;y++){ int k=0;
          if(G->nt>0)k=(w[y][G->a1]-w[y][G->b1]+26)%26; if(G->nt>1)k=k*26+(w[y][G->a2]-w[y][G->b2]+26)%26;
          for(int e=G->bstart[k];e<G->bstart[k+1];e++){ if(used>=ccap){ccap*=2;cand=realloc(cand,sizeof(int)*ccap);} cand[used++]=(y<<16)|G->bent[e]; } }
        gcnt[g]=used-gofs[g]; }
      const int *cl=cand+gofs[g]; int ncl=gcnt[g];
      for(int e=0;e<ncl;e++){ int y=cl[e]>>16, xf=cl[e]&0xffff, x=xf>>1, f=xf&1;
        if(!ALLOW[x][y])continue;
        const unsigned char*tg=K->tgt+(size_t)xf*K->nd; int good=1;
        for(int t=G->nt;t<K->nd;t++) if((w[y][K->da[t]]-w[y][K->db[t]]+26)%26!=tg[t]){good=0;break;}
        if(!good)continue;
        lh[(((size_t)x*na+y)*2+f)*27+K->L]++;
        long long doprint;
        #pragma omp atomic capture
        doprint=++printed;
        if(doprint<=maxprint){
          char key[27]; for(int k=0;k<K->L;k++)key[k]='?'; key[K->L]=0;
          for(int j=0;j<24;j++){int u=INV[x][PT[j]]; int v=f?(w[y][j]+u)%26:(w[y][j]-u+26)%26; key[K->cls[j]]=AL[y][v];}
          #pragma omp critical
          printf("S perm=%ld dir=%d X=%s Y=%s ix=%d iy=%d form=%s L=%d segE=%s segB=%s o1=%d o2=%d key=%s\n",q,dir,AL[x],AL[y],x,y,f?"beau":"vig",K->L,SEN[K->s1],SBN[K->s2],K->o1,K->o2,key);
        }}
     }}
   }
   #pragma omp critical
   for(size_t a=0;a<HS;a++)ph[a]+=lh[a];
   free(lh); free(cand); free(gstamp); free(gofs); free(gcnt);
  }
  for(int L=LMIN;L<=LMAX;L++){long long t=0; for(size_t a=0;a<HS/27;a++)t+=ph[a*27+L]; printf("H %d %lld\n",L,t);}
  for(size_t a=0;a<HS/27;a++)for(int L=LMIN;L<=LMAX;L++) if(ph[a*27+L]) printf("P %zu %zu %zu %d %lld\n",a/2/na,(a/2)%na,a%2,L,ph[a*27+L]);
  long long tot=0; for(size_t a=0;a<HS;a++)tot+=ph[a];
  printf("T rows=%lld dirs=%d alphabets=%d L=%d..%d configs=%d groups=%d survivors(cells, vig=variant counted once)=%lld printed=%lld\n",rows,nd,na,LMIN,LMAX,ncf,ngr,tot,printed);
  return 0;}
