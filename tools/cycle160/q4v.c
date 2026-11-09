/* Cycle 160 (IDEAS I-010): periodic Quagmire IV with two DIFFERENT vocabulary-keyed
   alphabets (PA = keyed(W1), CA = keyed(W2)), any periodic key of length p,
   Vigenere (variant shares consistency) and Beaufort, behind every permutation of
   the 165,065-entry bank in both directions, key at the plaintext index (model Q,
   ix=0) or at the carved index (transposition first, ix=1).  Exact.

   For a configuration (perm, dir, ix, p) the 24 cribs fall into residue classes.
   Two cribs a,b in one class must satisfy
       CA^-1(c_a) - CA^-1(c_b) == s * (PA^-1(p_a) - PA^-1(p_b))   (mod 26)
   with s = +1 (Vigenere) or -1 (Beaufort).  Alphabet independent prefilter:
   c_a == c_b  <=>  p_a == p_b, else the config is dead for every alphabet pair.
   Pairs with c_a==c_b and p_a==p_b are trivially true and dropped.  The remaining
   m pairs are a vector equation D_C(CA) == s * D_P(PA): hash join over the unique
   keyed alphabets (key = first 3 coordinates, 26^3 buckets), full check after.
   Identical constraint lists (same perm signature) are cached.

   usage: q4v CT vocab.txt perms.bin label qlo qhi PMIN PMAX [identity_only [drop_crib]]
   drop_crib (0-23) removes one crib (one wrong crib letter or one wrong carved letter under it).
   Output lines:
     H lab ix p configs prefilter_pass computed survivors_cfg matches_new matches_same
     M lab q dir ix p mode W1 W2 m              (each QIV match, when a config has <= MAXLIST)
     S lab q dir ix p m nmatch                  (config with > MAXLIST matches, summary only)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
#define MAXW 12000
#define MAXLIST 40
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static char Wd[MAXW][40]; static int nw;
static unsigned char UA[MAXW][26], UI[MAXW][26]; static int nu; static int urep[MAXW]; /* rep word idx */
static void keyed(const char*w,unsigned char*al,unsigned char*inv){int u[26]={0},n=0;for(const char*p=w;*p;p++){int c=*p-'A';if(c<0||c>25||u[c])continue;u[c]=1;al[n++]=c;}for(int c=0;c<26;c++)if(!u[c])al[n++]=c;for(int i=0;i<26;i++)inv[al[i]]=i;}
/* cache */
#define HB 22
static uint64_t *hk; static int *hv;
static int cache_get(uint64_t k,int*v){uint64_t h=(k*0x9E3779B97F4A7C15ULL)>>(64-HB);while(hk[h]){if(hk[h]==k){*v=hv[h];return 1;}h=(h+1)&((1u<<HB)-1);}return 0;}
static long cache_n=0;
static void cache_put(uint64_t k,int v){if(cache_n>(1L<<HB)*7/10)return;uint64_t h=(k*0x9E3779B97F4A7C15ULL)>>(64-HB);while(hk[h])h=(h+1)&((1u<<HB)-1);hk[h]=k;hv[h]=v;cache_n++;}
static int bcount[17577], bstart[17577], border[MAXW];
static int ckey[MAXW];
/* join: returns #matches with distinct alphabets (new), *same gets identical-alphabet matches; if lst, print */
static int join(int m,const int*ca,const int*cb,const int*pa,const int*pb,int*same,int print,const char*lab,long q,int dir,int ix,int p){
  int kk=m<3?m:3; int nb=1; for(int i=0;i<kk;i++)nb*=26;
  memset(bcount,0,sizeof(int)*(nb+1));
  for(int a=0;a<nu;a++){const unsigned char*I=UI[a];int k=0;for(int i=kk-1;i>=0;i--){int d=I[ca[i]]-I[cb[i]];if(d<0)d+=26;k=k*26+d;}ckey[a]=k;bcount[k]++;}
  int s=0;for(int b=0;b<nb;b++){bstart[b]=s;s+=bcount[b];bcount[b]=bstart[b];}
  for(int a=0;a<nu;a++)border[bcount[ckey[a]]++]=a;
  int nn=0,ns=0;
  for(int mode=0;mode<2;mode++) for(int b=0;b<nu;b++){const unsigned char*J=UI[b];int e[24];
    int k=0;for(int i=kk-1;i>=0;i--){int d=J[pa[i]]-J[pb[i]];if(mode)d=-d;d%=26;if(d<0)d+=26;e[i]=d;k=k*26+d;}
    int st=bstart[k],en=st+ (k+1<nb? bstart[k+1]-st : nu-st);
    for(int t=st;t<en;t++){int a=border[t];const unsigned char*I=UI[a];int ok=1;
      for(int i=kk;i<m;i++){int d=I[ca[i]]-I[cb[i]];if(d<0)d+=26;int f=J[pa[i]]-J[pb[i]];if(mode)f=-f;f%=26;if(f<0)f+=26;if(d!=f){ok=0;break;}}
      if(!ok)continue;
      if(a==b)ns++;else{nn++; if(print) printf("M %s %ld %d %d %d %s %s %s %d\n",lab,q,dir,ix,p,mode?"beau":"vig",Wd[urep[b]],Wd[urep[a]],m);}
    }}
  *same=ns;return nn;
}
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage\n");return 1;}
  const char*Cs=argv[1];int C[N];for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  const char*lab=argv[4];long qlo=atol(argv[5]),qhi=atol(argv[6]);int PMIN=atoi(argv[7]),PMAX=atoi(argv[8]);int idonly=argc>9&&atoi(argv[9]);int drop=argc>10?atoi(argv[10]):-1;
  FILE*wf=fopen(argv[2],"r");while(nw<MAXW&&fscanf(wf,"%39s",Wd[nw])==1)nw++;fclose(wf);
  for(int w=0;w<nw;w++){unsigned char al[26],inv[26];keyed(Wd[w],al,inv);int f=-1;
    for(int u=0;u<nu;u++)if(!memcmp(UA[u],al,26)){f=u;break;}
    if(f<0){memcpy(UA[nu],al,26);memcpy(UI[nu],inv,26);urep[nu]=w;nu++;}}
  fprintf(stderr,"%s: %d words, %d unique alphabets\n",lab,nw,nu);
  int ptl[24];for(int i=0;i<24;i++)ptl[i]=PT[i]-'A';
  short*Perm;long np;
  if(idonly){np=1;Perm=malloc(N*sizeof(short));for(int i=0;i<N;i++)Perm[i]=i;qlo=0;qhi=1;}
  else{FILE*pf=fopen(argv[3],"rb");fseek(pf,0,SEEK_END);np=ftell(pf)/(2*N);rewind(pf);Perm=malloc(np*N*sizeof(short));if(fread(Perm,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);}
  if(qhi>np)qhi=np;
  hk=calloc(1u<<HB,8);hv=calloc(1u<<HB,4);
  static long long H[2][33][6];memset(H,0,sizeof H);
  for(long q=qlo;q<qhi;q++){const short*s=Perm+q*N;short u[N];for(int i=0;i<N;i++)u[s[i]]=i;
    for(int dir=0;dir<(idonly?1:2);dir++){const short*S=dir?u:s;int tc[24],ct[24];
      for(int t=0;t<24;t++){tc[t]=S[CI[t]];ct[t]=C[tc[t]];}
      for(int ix=0;ix<2;ix++){ if(idonly&&ix)continue;
       for(int p=PMIN;p<=PMAX;p++){H[ix][p][0]++;
        int last[33];for(int r=0;r<p;r++)last[r]=-1;
        int ca[24],cb[24],pa[24],pb[24],m=0,dead=0;
        for(int i=0;i<24;i++){if(i==drop)continue;int r=(ix?tc[i]:CI[i])%p;int j=last[r];last[r]=i;if(j<0)continue;
          int ce=ct[j]==ct[i],pe=ptl[j]==ptl[i];if(ce!=pe){dead=1;break;}if(ce)continue;
          ca[m]=ct[j];cb[m]=ct[i];pa[m]=ptl[j];pb[m]=ptl[i];m++;}
        if(dead)continue;H[ix][p][1]++;
        uint64_t key=1469598103934665603ULL^(uint64_t)(p*131+ix*7+1);
        for(int i=0;i<m;i++){key=(key^(uint64_t)(ca[i]|cb[i]<<5|pa[i]<<10|pb[i]<<15))*1099511628211ULL;}
        key^=(uint64_t)m<<58; if(!key)key=1;
        int v,sm=0;
        if(!cache_get(key,&v)){v=join(m,ca,cb,pa,pb,&sm,0,lab,q,dir,ix,p);H[ix][p][2]++;H[ix][p][5]+=sm;cache_put(key,v);}
        if(v>0){H[ix][p][3]++;H[ix][p][4]+=v;
          if(v<=MAXLIST)join(m,ca,cb,pa,pb,&sm,1,lab,q,dir,ix,p);
          else printf("S %s %ld %d %d %d %d %d\n",lab,q,dir,ix,p,m,v);}
      }}}
  }
  for(int ix=0;ix<2;ix++)for(int p=PMIN;p<=PMAX;p++)if(H[ix][p][0])printf("H %s %d %d %lld %lld %lld %lld %lld %lld\n",lab,ix,p,H[ix][p][0],H[ix][p][1],H[ix][p][2],H[ix][p][3],H[ix][p][4],H[ix][p][5]);
  return 0;}
