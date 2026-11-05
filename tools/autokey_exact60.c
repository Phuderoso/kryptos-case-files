// Cycle 60: exact autokey test behind a permutation family (decimations).
// perm file: int16 x N per perm; perm[j] = carved index of the symbol paired with PT position j.
// Model A: PT -> autokey -> I (PT order) -> transposition -> carved:  I[j] = CT[perm[j]].
// Model B: PT -> transposition -> T (carved order) -> autokey -> carved: T[perm[j]] = PT[j].
// Feeds: CT-fed (key_j = previous ciphertext letter of that layer, lag L), PT-fed (key_j = PT letter lag L).
// Modes in alphabet-index space: vig c=p+k, beau c=k-p, var c=p-k.  '?' symbols give no constraint.
// A test = (perm, alphabet, model, feed, mode, lag). It "hits" when all n crib constraints hold (n>=1).
// Prints hit histogram by n per (model,feed); lines for hits with n >= NREP (CT-fed hits also print the
// fully determined decryption of positions >= L, '.' where unknown).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage: perm.bin N alpha.bin nalpha ct.txt cribofs lmax [nrep]\n");return 1;}
  int N=atoi(argv[2]);
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); rewind(f);
  long np=sz/(2*N); short*P=malloc(sz); if(fread(P,1,sz,f)!=(size_t)sz) return 2; fclose(f);
  int na=atoi(argv[4]); f=fopen(argv[3],"rb"); unsigned char*A=malloc(26*na); if(fread(A,1,26*na,f)!=(size_t)(26*na)) return 3; fclose(f);
  char ct[256]; f=fopen(argv[5],"r"); if(fscanf(f,"%255s",ct)!=1) return 4; fclose(f);
  int ofs=atoi(argv[6]), lmax=atoi(argv[7]), nrep=argc>8?atoi(argv[8]):8;
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int crib[256]; for(int i=0;i<N;i++) crib[i]=-1;
  for(int i=0;i<13;i++) crib[ofs+21+i]=cr1[i]-'A'; for(int i=0;i<11;i++) crib[ofs+63+i]=cr2[i]-'A';
  long hist[4][32]; long tests[4][32]; memset(hist,0,sizeof hist); memset(tests,0,sizeof tests);
  #pragma omp parallel
  { long lh[4][32], lt[4][32]; memset(lh,0,sizeof lh); memset(lt,0,sizeof lt);
  #pragma omp for schedule(dynamic,32)
  for(long t=0;t<np;t++){ short*pp=P+t*N; int inv[256]; for(int i=0;i<N;i++) inv[i]=-1; for(int j=0;j<N;j++) if(pp[j]>=0) inv[pp[j]]=j;
    for(int a=0;a<na;a++){ unsigned char*al=A+26*a; int idx[26]; for(int i=0;i<26;i++) idx[al[i]]=i;
      int cx[256]; for(int i=0;i<N;i++) cx[i]=ct[i]=='?'?-1:idx[ct[i]-'A'];
      int px[256]; for(int i=0;i<N;i++) px[i]=crib[i]<0?-1:idx[crib[i]];
      for(int L=1;L<=lmax;L++) for(int mf=0;mf<4;mf++){ // mf: 0 A-CT,1 A-PT,2 B-CT,3 B-PT
        int C[32],Pp[32],K[32],n=0;
        for(int j=0;j<N;j++){ if(px[j]<0||pp[j]<0) continue; int c,k;
          if(mf==0){ if(j<L||pp[j-L]<0) continue; c=cx[pp[j]]; k=cx[pp[j-L]]; }
          else if(mf==1){ if(j<L||px[j-L]<0) continue; c=cx[pp[j]]; k=px[j-L]; }
          else if(mf==2){ int cp=pp[j]; if(cp<L) continue; c=cx[cp]; k=cx[cp-L]; }
          else { int cp=pp[j]; if(cp<L||inv[cp-L]<0||px[inv[cp-L]]<0) continue; c=cx[cp]; k=px[inv[cp-L]]; }
          if(c<0||k<0) continue; C[n]=c;Pp[n]=px[j];K[n]=k;n++; }
        if(n==0) continue;
        for(int m=0;m<3;m++){ lt[mf][n]++; int ok=1;
          for(int i=0;i<n&&ok;i++){ int e= m==0?(Pp[i]+K[i])%26: m==1?(K[i]-Pp[i]+26)%26:(Pp[i]-K[i]+26)%26; if(e!=C[i]) ok=0; }
          if(!ok) continue; lh[mf][n]++;
          if(n>=nrep){ char out[257]; for(int j=0;j<N;j++) out[j]='.'; out[N]=0;
            if(mf==0||mf==2) for(int j=0;j<N;j++){ int c,k; if(pp[j]<0) continue;
              if(mf==0){ if(j<L||pp[j-L]<0) continue; c=cx[pp[j]]; k=cx[pp[j-L]]; }
              else { int cp=pp[j]; if(cp<L) continue; c=cx[cp]; k=cx[cp-L]; }
              if(c<0||k<0) continue; int p= m==0?(c-k+26)%26: m==1?(k-c+26)%26:(c+k)%26; out[j]=al[p]+'A'; }
            #pragma omp critical
            printf("HIT perm %ld alpha %d model %c feed %s mode %s L %d n %d %s\n",t,a,mf<2?'A':'B',mf%2?"PT":"CT",m==0?"vig":m==1?"beau":"var",L,n,out); } } } } }
  #pragma omp critical
  for(int x=0;x<4;x++) for(int y=0;y<32;y++){hist[x][y]+=lh[x][y];tests[x][y]+=lt[x][y];} }
  const char*nm[4]={"A/CT","A/PT","B/CT","B/PT"};
  fprintf(stderr,"perms %ld alphabets %d lmax %d\n",np,na,lmax);
  for(int x=0;x<4;x++){ fprintf(stderr,"%s hits(n)/tests:",nm[x]); for(int y=1;y<32;y++) if(tests[x][y]) fprintf(stderr," n%d:%ld/%ld",y,hist[x][y],tests[x][y]); fprintf(stderr,"\n"); }
  return 0; }
