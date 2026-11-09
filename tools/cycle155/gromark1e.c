/* Cycle 155 (IDEAS I-008, I-003): Gromark / Periodic Gromark under ONE crib or carved-letter error, exact.
   Same model and primer sets as cycle 130 (tools/cycle130/pgfree.c): cipher alphabet arbitrary (injective v), plaintext
   alphabet A-Z or KRYPTOS, digits by chain addition d[i]=d[i-L]+d[i-L+1] mod 10 from a primer of length L.
     model P (periodic Gromark, relaxed ACA): L free group offsets o_g, g=(i/L) mod L  (as cycle 130)
     model G (ordinary Gromark): one offset (absorbed in v)  -- a stronger test, special case of P
   Each crib t gives  v(ct_t) - o_g(t) = w_t,  w = pa(p)+d (vig) or d-pa(p) (beau; variant is equivalent under arbitrary v).
   The key stream does not depend on the ciphertext, so one wrong carved letter under a crib or one wrong crib letter
   breaks exactly ONE equation, and a wrong carved letter elsewhere breaks none. One-error feasibility <=> some 23-subset
   is feasible. Exact pruning: if all 24 are infeasible, the dropped equation must lie in every infeasibility
   certificate; we take one certificate (the cycle closing the first contradiction in a spanning forest, or the tree path
   joining two letters forced to the same value) and re-test the full system without each of its edges.
   Output: per text/L/mode/model: primers tested, strict-feasible, one-error-feasible primers (and (primer,drop) pairs)
   per (pa,form); SHOW=1 prints every one-error survivor with the dropped crib index.
   usage: gromark1e CT L mode(all|perm) lo hi label model(P|G) [base=10]
   (base b: digits mod b, primers all b^L strings; cycle 10 checked bases 5-10, L 4-6 with A-Z plain)                                               */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define NN 40
static const char*AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int cp[24],cl[24],cc[24],L,G,grp[24];
/* forest with explicit tree edges for certificates (tiny graph: <=26 letters + <=12 offsets) */
static int par[NN],pot[NN];               /* union-find with potentials: pot[x]=v(x)-v(par[x]) chain */
static int adjn[NN],adjv[NN][24],adje[NN][24],adjw[NN][24];
static int find(int x,int*p){ int s=0; while(par[x]!=x){ s=(s+pot[x])%26; x=par[x]; } *p=s; return x; }
/* tree path edges between a and b (BFS over tree adjacency); returns count, fills ed */
static int treepath(int a,int b,int*ed){
  int prev[NN],pe[NN],q[NN],h=0,t=0; for(int i=0;i<NN;i++) prev[i]=-2; prev[a]=-1; q[t++]=a;
  while(h<t){ int x=q[h++]; if(x==b) break; for(int k=0;k<adjn[x];k++){ int y=adjv[x][k]; if(prev[y]==-2){prev[y]=x;pe[y]=adje[x][k];q[t++]=y;} } }
  int n=0; for(int x=b;x!=a;x=prev[x]) ed[n++]=pe[x]; return n; }
/* returns 1 feasible; if infeasible and cert!=NULL fills certificate edges (count in *nc) */
static int feasible(const int*w,int skip,int*cert,int*nc){
  int nn=26+G; for(int i=0;i<nn;i++){par[i]=i;pot[i]=0;adjn[i]=0;}
  for(int t=0;t<24;t++){ if(t==skip) continue;
    int x=cc[t], y=26+grp[t], px,py; int rx=find(x,&px), ry=find(y,&py);   /* v(x)-v(y)=w */
    if(rx==ry){ if(((px-py-w[t])%26+26)%26){ if(cert){ *nc=treepath(x,y,cert); cert[(*nc)++]=t; } return 0; } }
    else { par[rx]=ry; pot[rx]=((py+w[t]-px)%26+52)%26;
      adjv[x][adjn[x]]=y; adje[x][adjn[x]]=t; adjn[x]++; adjv[y][adjn[y]]=x; adje[y][adjn[y]]=t; adjn[y]++; } }
  int seenr[26],seenv[26],ns=0;
  for(int t=0;t<24;t++){ if(t==skip) continue; int c=cc[t],dup=0; for(int u=0;u<t;u++) if(u!=skip&&cc[u]==c){dup=1;break;} if(dup) continue;
    int p,r=find(c,&p);
    for(int k=0;k<ns;k++) if(seenr[k]==r&&seenv[k]==p){ if(cert){ int other=-1;
          for(int u=0;u<t;u++){ if(u==skip) continue; int pp,rr=find(cc[u],&pp); if(rr==r&&pp==p&&cc[u]!=c){other=cc[u];break;} }
          *nc=treepath(c,other,cert); } return 0; }
    seenr[ns]=r; seenv[ns]=p; ns++; }
  return 1;
}
static int nextperm(int*a,int n){ int i=n-2; while(i>=0&&a[i]>=a[i+1]) i--; if(i<0) return 0; int j=n-1; while(a[j]<=a[i]) j--;
  int t=a[i];a[i]=a[j];a[j]=t; for(int l=i+1,r=n-1;l<r;l++,r--){t=a[l];a[l]=a[r];a[r]=t;} return 1; }
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  const char*C=argv[1]; L=atoi(argv[2]); int perm=!strcmp(argv[3],"perm"); long lo=atol(argv[4]),hi=atol(argv[5]); const char*lab=argv[6];
  int periodic=argv[7][0]=='P'; int B=argc>8?atoi(argv[8]):10; G=periodic?L:1; int show=getenv("SHOW")!=NULL;
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  for(int i=0;i<13;i++){cp[i]=21+i;cl[i]=c1[i]-'A';} for(int i=0;i<11;i++){cp[13+i]=63+i;cl[13+i]=c2[i]-'A';}
  for(int t=0;t<24;t++){ cc[t]=C[cp[t]]-'A'; grp[t]=periodic?((cp[t]/L)%L):0; }
  int paz[26],pka[26]; for(int i=0;i<26;i++){paz[AZ[i]-'A']=i;pka[KA[i]-'A']=i;}
  long strict[2][2]={{0}},one[2][2]={{0}},pairs[2][2]={{0}},dropc[24]={0};
  int d[N],a[16],w[24],cert[64],nc; for(int i=0;i<L;i++) a[i]=i+1;
  long idx=0,tested=0;
  for(;;){
    if(idx>=hi) break;
    if(idx>=lo){
      if(perm) for(int i=0;i<L;i++) d[i]=a[i]%10;
      else { long x=idx; for(int i=L-1;i>=0;i--){d[i]=x%B;x/=B;} }
      for(int i=L;i<74;i++) d[i]=(d[i-L]+d[i-L+1])%B;
      tested++;
      for(int p=0;p<2;p++){ const int*pa=p?pka:paz;
        for(int f=0;f<2;f++){
          for(int t=0;t<24;t++){ int v=f==0? pa[cl[t]]+d[cp[t]] : d[cp[t]]-pa[cl[t]]; w[t]=((v%26)+26)%26; }
          if(feasible(w,-1,cert,&nc)){ strict[p][f]++; continue; }
          int cand[64],ncand=nc; memcpy(cand,cert,sizeof(int)*nc);
          int got=0;
          for(int k=0;k<ncand;k++){ int dup=0; for(int u=0;u<k;u++) if(cand[u]==cand[k]) dup=1; if(dup) continue;
            if(feasible(w,cand[k],NULL,NULL)){ got++; pairs[p][f]++; dropc[cand[k]]++;
              if(show){ printf("S %s %c L=%d %s pa=%s form=%s drop=%d(pos%d %c) primer=",lab,periodic?'P':'G',L,perm?"perm":"all",p?"ka":"az",f?"beau":"vig",cand[k],cp[cand[k]],'A'+cl[cand[k]]);
                for(int i=0;i<L;i++) printf("%d",d[i]); printf("\n"); } } }
          if(got) one[p][f]++;
        } }
    }
    idx++;
    if(perm){ if(!nextperm(a,L)) break; } else { long m=1; for(int i=0;i<L;i++) m*=B; if(idx>=m) break; }
  }
  printf("C %s %c%s L=%d %s lo=%ld tested=%ld strict az:vig=%ld beau=%ld ka:vig=%ld beau=%ld | one az:vig=%ld beau=%ld ka:vig=%ld beau=%ld | pairs=%ld | dropidx",
    lab,periodic?'P':'G',B==10?"":argv[8],L,perm?"perm":"all",lo,tested,strict[0][0],strict[0][1],strict[1][0],strict[1][1],one[0][0],one[0][1],one[1][0],one[1][1],
    pairs[0][0]+pairs[0][1]+pairs[1][0]+pairs[1][1]);
  for(int t=0;t<24;t++) if(dropc[t]) printf(" %d:%ld",t,dropc[t]); printf("\n");
}
