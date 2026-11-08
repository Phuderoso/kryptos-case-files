/* Cycle 130: Periodic Gromark with the keyword UNKNOWN (relaxed, exact).
   Model: v(c) = CA^-1(c) arbitrary injective; group offsets o_g (g = (i/L) mod L) free in Z26; digits d_i from a
   primer of length L by chain addition d[i] = d[i-L] + d[i-L+1] mod 10.  Each crib gives one difference equation
     vig (ACA):  v(ct_i) - o_g = pa(p_i) + d_i      beau: v(ct_i) - o_g = d_i - pa(p_i)      variant: v(ct_i) - o_g = pa(p_i) - d_i
   (beau/variant: o_g renamed to -o_g, which is still free).  Feasible <=> weighted union-find over the 26 letter
   nodes + L offset nodes has no contradiction and letters in one component get distinct values (components can be
   shifted apart independently; with <=26 letters that is always possible).  This relaxes the ACA rule (alphabet and
   offsets need not come from one keyword), so a negative is strong and survivors are only candidates.
   Primers: all 10^L digit strings for L <= LALL, keyword-rank primers (permutations of 1..L, 10 -> 0) for L up to LMAX.
   usage: pgfree CT L mode(all|perm) lo hi label       (lo/hi = index range of primers, for splitting)            */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int cp[24],cl[24],cc[24],L,par[64],pot[64];
static int find(int x){ if(par[x]==x) return x; int r=find(par[x]); pot[x]=(pot[x]+pot[par[x]])%26; par[x]=r; return r; }
/* pot[x] = value(x) - value(root) */
static int feasible(const int*d,const int*pa,int form){
  for(int i=0;i<26+L;i++){par[i]=i;pot[i]=0;}
  for(int t=0;t<24;t++){ int i=cp[t]; int a=pa[cl[t]], w;
    if(form==0) w=a+d[i]; else if(form==1) w=d[i]-a; else w=a-d[i]; w=((w%26)+26)%26;
    int x=cc[t], y=26+((i/L)%L);           /* v(x) - v(y) = w */
    int rx=find(x), ry=find(y);
    if(rx==ry){ if(((pot[x]-pot[y]-w)%26+26)%26) return 0; }
    else { par[rx]=ry; pot[rx]=((pot[y]+w-pot[x])%26+26)%26; } }
  /* injectivity among letter nodes */
  int seen[64][26]; memset(seen,0,sizeof seen);
  for(int c=0;c<26;c++){ int r=find(c); if(r==c && par[c]==c){ int used=0; for(int t=0;t<24;t++) if(cc[t]==c) used=1; if(!used) continue; }
    int used=0; for(int t=0;t<24;t++) if(cc[t]==c) used=1; if(!used) continue;
    if(seen[r][pot[c]]) return 0; seen[r][pot[c]]=1; }
  return 1;
}
static int nextperm(int*a,int n){ int i=n-2; while(i>=0&&a[i]>=a[i+1]) i--; if(i<0) return 0; int j=n-1; while(a[j]<=a[i]) j--;
  int t=a[i];a[i]=a[j];a[j]=t; for(int l=i+1,r=n-1;l<r;l++,r--){t=a[l];a[l]=a[r];a[r]=t;} return 1; }
int main(int argc,char**argv){
  const char*C=argv[1]; L=atoi(argv[2]); int perm=!strcmp(argv[3],"perm"); long lo=atol(argv[4]),hi=atol(argv[5]); const char*lab=argv[6];
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=c1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=c2[i]-'A';}
  for(int t=0;t<24;t++) cc[t]=C[cp[t]]-'A';
  int paz[26],pka[26]; for(int i=0;i<26;i++){paz[AZ[i]-'A']=i;pka[KA[i]-'A']=i;}
  long cnt[2][3]={{0}}; int d[N]; int a[16]; for(int i=0;i<L;i++) a[i]=i+1;
  long idx=0, tested=0;
  for(;;){
    if(idx>=hi) break;
    if(idx>=lo){
      if(perm) for(int i=0;i<L;i++) d[i]=a[i]%10;
      else { long x=idx; for(int i=L-1;i>=0;i--){d[i]=x%10;x/=10;} }
      for(int i=L;i<N;i++) d[i]=(d[i-L]+d[i-L+1])%10;
      tested++;
      for(int p=0;p<2;p++) for(int f=0;f<3;f++) if(feasible(d,p?pka:paz,f)){ cnt[p][f]++;
        if(getenv("SHOW")){ printf("S %s L=%d pa=%s form=%d primer=",lab,L,p?"ka":"az",f); for(int i=0;i<L;i++)printf("%d",d[i]); printf("\n"); } }
    }
    idx++;
    if(perm){ if(!nextperm(a,L)) break; } else { long m=1; for(int i=0;i<L;i++) m*=10; if(idx>=m) break; }
  }
  printf("C %s L=%d %s tested=%ld az:vig=%ld beau=%ld var=%ld ka:vig=%ld beau=%ld var=%ld\n",lab,L,perm?"perm":"all",tested,
    cnt[0][0],cnt[0][1],cnt[0][2],cnt[1][0],cnt[1][1],cnt[1][2]);
}
