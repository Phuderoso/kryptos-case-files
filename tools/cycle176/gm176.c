/* Cycle 176 (IDEAS I-125): ordinary Gromark behind the 165,782 K3-law decimations / spiral-diagonal routes (all.bin).
   Model G: digits by chain addition d[i] = d[i-L] + d[i-L+1] mod 10 from a primer of length L (all 10^L primers, or a
   primer file of named primers); plaintext alphabet PA = A-Z or KRYPTOS; cipher alphabet ARBITRARY (any bijection v);
   ct = v^-1( w ),  w = PA(p) + d  (vig)  or  d - PA(p)  (beau; variant c = CA[PA(p) - d] is beau after reflecting CA).
   Feasible <=> for the 24 crib slots:  ct_a == ct_b  <=>  w_a == w_b  (mod 26).  Exact, strict (no error).
   Perm convention (repo): plaintext position i -> carved position S[i]; crib t at plaintext index CI[t] is carved at S[CI[t]].
   ix 0: Gromark on the plaintext index, then transpose  -> key index CI[t]   (hash join: perms keyed by ct partition)
   ix 1: transpose first, Gromark on the carved index     -> key index S[CI[t]] (brute force per perm x primer)
   usage: gm176 CT perms.bin label qlo qhi ix Lmin Lmax [primerfile]
     primerfile lines: "name digits"  (then Lmin/Lmax ignored; L = len(digits))
   output:  H label ix L pa form primers configs fits ;  M label ix L pa form q primer ;  END                         */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK",*AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int pav[2][24];               /* PA index of crib plaintext letters */
static void canon(const int*x,uint64_t*a,uint64_t*b){int lab[26];memset(lab,-1,sizeof lab);int n=0;uint64_t A=0,B=0;
  for(int t=0;t<24;t++){int v=x[t];if(lab[v]<0)lab[v]=n++;uint64_t l=lab[v];if(t<12)A|=l<<(5*t);else B|=l<<(5*(t-12));}*a=A;*b=B;}
/* hash table of perm codes (ix 0) */
#define HB 20
static uint64_t HA[1<<HB],HBk[1<<HB];static int Hhead[1<<HB],*nxt;static int used[1<<HB];
static int hslot(uint64_t a,uint64_t b){uint64_t h=((a*0x9E3779B97F4A7C15ULL)^(b*0xC2B2AE3D27D4EB4FULL))>>(64-HB);
  while(used[h]&&!(HA[h]==a&&HBk[h]==b))h=(h+1)&((1u<<HB)-1);return (int)h;}
static void stream(const int*pr,int L,int*d){for(int i=0;i<L;i++)d[i]=pr[i];for(int i=L;i<N;i++)d[i]=(d[i-L]+d[i-L+1])%10;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];int C[N];if(strlen(Cs)!=N)return 1;for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  const char*lab=argv[3];long qlo=atol(argv[4]),qhi=atol(argv[5]);int ix=atoi(argv[6]),Lmin=atoi(argv[7]),Lmax=atoi(argv[8]);
  for(int t=0;t<24;t++){pav[0][t]=PT[t]-'A';pav[1][t]=strchr(KA,PT[t])-KA;}
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;
  /* primer list */
  int npr=0,cap=0;int*prs=NULL;int*prL=NULL;char(*prn)[32]=NULL;
  if(argc>9){FILE*f=fopen(argv[9],"r");char nm[64],dg[64];while(fscanf(f,"%63s %63s",nm,dg)==2){if(npr==cap){cap=cap?cap*2:1024;prs=realloc(prs,cap*16*sizeof(int));prL=realloc(prL,cap*sizeof(int));prn=realloc(prn,cap*32);}
      int L=strlen(dg);if(L>16)continue;for(int i=0;i<L;i++)prs[npr*16+i]=dg[i]-'0';prL[npr]=L;snprintf(prn[npr],32,"%s",nm);npr++;}fclose(f);}
  int usefile=argc>9;
  if(ix==0){
    nxt=malloc(sizeof(int)*(qhi-qlo+1));
    for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int x[24];for(int t=0;t<24;t++)x[t]=C[S[CI[t]]];uint64_t a,b;canon(x,&a,&b);
      int h=hslot(a,b);if(!used[h]){used[h]=1;HA[h]=a;HBk[h]=b;Hhead[h]=-1;}nxt[q-qlo]=Hhead[h];Hhead[h]=(int)(q-qlo);}
    int Ls=usefile?0:Lmin,Le=usefile?0:Lmax;
    for(int L=Ls;L<=Le;L++){
      long nprim=1;if(!usefile)for(int i=0;i<L;i++)nprim*=10;else nprim=npr;
      long long fits[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,4096) reduction(+:fits[:2][:2])
      for(long k=0;k<nprim;k++){int pr[16],LL,d[N];
        if(usefile){LL=prL[k];memcpy(pr,prs+k*16,LL*sizeof(int));}else{LL=L;long z=k;for(int i=LL-1;i>=0;i--){pr[i]=z%10;z/=10;}}
        stream(pr,LL,d);
        for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++){int w[24];
          for(int t=0;t<24;t++){int v=fm?d[CI[t]]-pav[pa][t]:pav[pa][t]+d[CI[t]];w[t]=((v%26)+26)%26;}
          uint64_t a,b;canon(w,&a,&b);int h=hslot(a,b);if(!used[h])continue;
          for(int e=Hhead[h];e>=0;e=nxt[e]){
            fits[pa][fm]++;
            char ps[20];for(int i=0;i<LL;i++)ps[i]='0'+pr[i];ps[LL]=0;
            #pragma omp critical
            printf("M %s 0 %d %s %s %ld %s%s%s\n",lab,LL,pa?"ka":"az",fm?"beau":"vig",qlo+e,ps,usefile?" ":"",usefile?prn[k]:"");}}
      }
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 0 %d %s %s %ld %lld %lld\n",lab,usefile?-1:L,pa?"ka":"az",fm?"beau":"vig",nprim,(long long)nprim*(qhi-qlo),fits[pa][fm]);
    }
  } else {
    int Ls=usefile?0:Lmin,Le=usefile?0:Lmax;
    for(int L=Ls;L<=Le;L++){
      long nprim=1;if(!usefile)for(int i=0;i<L;i++)nprim*=10;else nprim=npr;
      unsigned char*D=malloc(nprim*N);int*Lk=malloc(nprim*sizeof(int));
      #pragma omp parallel for
      for(long k=0;k<nprim;k++){int pr[16],LL,d[N];if(usefile){LL=prL[k];memcpy(pr,prs+k*16,LL*sizeof(int));}else{LL=L;long z=k;for(int i=LL-1;i>=0;i--){pr[i]=z%10;z/=10;}}
        stream(pr,LL,d);for(int i=0;i<N;i++)D[k*N+i]=d[i];Lk[k]=LL;}
      long long fits[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,64) reduction(+:fits[:2][:2])
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int tc[24],ct[24];for(int t=0;t<24;t++){tc[t]=S[CI[t]];ct[t]=C[tc[t]];}
        /* equal-ct pairs (a,b) first: fast reject; then full bijection check */
        int ea[300],eb[300],ne=0;for(int a=0;a<24;a++)for(int b=a+1;b<24;b++)if(ct[a]==ct[b]){ea[ne]=a;eb[ne]=b;ne++;}
        for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++){int need[300];
          for(int e=0;e<ne;e++){int r=fm?(pav[pa][ea[e]]-pav[pa][eb[e]]):(pav[pa][eb[e]]-pav[pa][ea[e]]);need[e]=((r%26)+26)%26;} /* d_a - d_b == need mod 26 */
          for(long k=0;k<nprim;k++){const unsigned char*d=D+k*N;int ok=1;
            for(int e=0;e<ne;e++){int x=(int)d[tc[ea[e]]]-(int)d[tc[eb[e]]]+26;if(x>=26)x-=26;if(x!=need[e]){ok=0;break;}}
            if(!ok)continue;
            int w[24],m2[26];memset(m2,-1,sizeof m2);
            for(int t=0;t<24&&ok;t++){int v=fm?d[tc[t]]-pav[pa][t]:pav[pa][t]+d[tc[t]];v=((v%26)+26)%26;w[t]=v;if(m2[v]<0)m2[v]=ct[t];else if(m2[v]!=ct[t])ok=0;}
            if(!ok)continue;
            fits[pa][fm]++;char ps[20];for(int i=0;i<Lk[k];i++)ps[i]='0'+d[i];ps[Lk[k]]=0;
            #pragma omp critical
            printf("M %s 1 %d %s %s %ld %s%s%s\n",lab,Lk[k],pa?"ka":"az",fm?"beau":"vig",q,ps,usefile?" ":"",usefile?prn[k]:"");
          }}
      }
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 1 %d %s %s %ld %lld %lld\n",lab,usefile?-1:L,pa?"ka":"az",fm?"beau":"vig",nprim,(long long)nprim*(qhi-qlo),fits[pa][fm]);
      free(D);free(Lk);
    }
  }
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
