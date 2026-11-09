/* Cycle 155 stage 2: exact ACA Periodic Gromark check with ANY keyword for a stage-1 survivor rank primer.
   Stage 1 (gromark1e, model P, perm primers) is an exact superset: any one-error ACA encryption with an L-letter keyword
   (letters distinct after dedupe) survives there with primer = ranks(keyword) mod 10. Given a rank permutation of 1..L,
   each set of L distinct letters gives exactly one keyword (the letter of rank k is the k-th smallest), so all keywords
   with that primer are the C(26,L) letter sets. For each: cipher alphabet ACA (keyword-columnar), keyword-mixed or KRYPTOS
   (cycle 129 variants), group offset = CA.index(kw[g mod L]), d by chain addition, forms vig/beau/var, plain A-Z or KRYPTOS;
   count crib mismatches; report configurations with <= MAXMIS (default 1) mismatches.
   usage: acakw1e CT L digits label [maxmis]                                                                          */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
int L,cp[24],cl[24],cc[24],maxmis=1; long hits=0,tested=0; const char*lab;
static void check(const int*rank,const char*kw){
  int d[N]; for(int i=0;i<L;i++) d[i]=rank[i]%10; for(int i=L;i<74;i++) d[i]=(d[i-L]+d[i-L+1])%10;
  char mixed[27]; int n=0,used[26]={0}; for(int i=0;i<L;i++){mixed[n++]=kw[i];used[kw[i]-'A']=1;} for(int c=0;c<26;c++) if(!used[c]) mixed[n++]='A'+c;
  char aca[27]; n=0; for(int r=1;r<=L;r++){ int col=-1; for(int c=0;c<L;c++) if(rank[c]==r) col=c; for(int j=col;j<26;j+=L) aca[n++]=mixed[j]; }
  const char*CAs[3]={aca,mixed,KA};
  for(int v=0;v<3;v++){ int inv[26]; for(int i=0;i<26;i++) inv[CAs[v][i]-'A']=i;
    int off[16]; for(int g=0;g<L;g++) off[g]=inv[kw[g]-'A'];
    for(int p=0;p<2;p++){ const char*PA=p?KA:AZ; int pinv[26]; for(int i=0;i<26;i++) pinv[PA[i]-'A']=i;
      for(int f=0;f<3;f++){ int mis=0; tested++;
        for(int t=0;t<24&&mis<=maxmis;t++){ int i=cp[t]; int k=(off[(i/L)%L]+d[i])%26; int a=pinv[cl[t]];
          int x= f==0? a+k : f==1? k-a : a-k; x=((x%26)+26)%26; if(x!=inv[cc[t]]) mis++; }
        if(mis<=maxmis){ hits++; printf("H %s L=%d kw=%.*s ca=%s pa=%s form=%d mis=%d\n",lab,L,L,kw,v==0?"aca":v==1?"mix":"ka",p?"ka":"az",f,mis); } } } }
}
static int nextperm(int*a,int n){ int i=n-2; while(i>=0&&a[i]>=a[i+1]) i--; if(i<0) return 0; int j=n-1; while(a[j]<=a[i]) j--;
  int t=a[i];a[i]=a[j];a[j]=t; for(int l=i+1,r=n-1;l<r;l++,r--){t=a[l];a[l]=a[r];a[r]=t;} return 1; }
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  const char*C=argv[1]; L=atoi(argv[2]); const char*dg=argv[3]; lab=argv[4]; if(argc>5) maxmis=atoi(argv[5]);
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=c1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=c2[i]-'A';}
  for(int t=0;t<24;t++) cc[t]=C[cp[t]]-'A';
  int a[16],nperm=0; for(int i=0;i<L;i++) a[i]=i+1;
  do{ int ok=1; for(int i=0;i<L;i++) if(a[i]%10!=dg[i]-'0'){ok=0;break;} if(!ok) continue; nperm++;
      for(unsigned m=(1u<<L)-1; m<(1u<<26); ){ char s[16]; int n=0; for(int c=0;c<26;c++) if(m>>c&1) s[n++]='A'+c;
        char kw[16]; for(int i=0;i<L;i++) kw[i]=s[a[i]-1]; check(a,kw);
        unsigned c=m&-m, r=m+c; m=(((r^m)>>2)/c)|r; }
  } while(nextperm(a,L));
  printf("D %s L=%d digits=%s rankperms=%d configs=%ld hits=%ld\n",lab,L,dg,nperm,tested,hits);
}
