/* Cycle 39 (crib-free classes at L<=13 get all 312 affine maps, chosen by quadgrams): periodic AFFINE substitution (c = a_r*x + b_r mod 26, a a unit, r = index mod L) on either side of a
   transposition, A-Z or KRYPTOS numbering. Exact crib check (24 known letters), periods L=1..26.
   Model A: affine at plaintext index i, then carved[P[i]] = s[i].  Model B: t[k]=pt[P[k]], carved[k]=aff_{k%L}(t[k]).
   (Same conventions as tools/vernam.c.) For fully determined configs (every class has a unique map) the whole
   97-letter decryption is scored with English quadgrams.
   usage: affine CARVED perms.bin qg.bin [maxperm] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const int U[12]={1,3,5,7,9,11,15,17,19,21,23,25};
float*QG; int inva[26];
static float score(const int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
int main(int argc,char**argv){
  const char*car=argv[1]; FILE*f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET);
  int np=sz/(2*N); short*perms=malloc(sz); if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1; fclose(f);
  if(argc>4){int m=atoi(argv[4]); if(m<np)np=m;}
  QG=malloc(sizeof(float)*456976); f=fopen(argv[3],"rb"); if(fread(QG,4,456976,f)!=456976)return 1; fclose(f);
  for(int a=1;a<26;a+=2)for(int b=1;b<26;b++)if(a*b%26==1)inva[a]=b;
  int num[2][26],den[2][26]; for(int l=0;l<26;l++){num[0][l]=l; num[1][l]=strchr(KA,'A'+l)-KA;} for(int e=0;e<2;e++)for(int l=0;l<26;l++)den[e][num[e][l]]=l;
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK"; int cp[24],cl[24],nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';} for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  long cons[27]={0},det[27]={0}; float best[27]; for(int L=0;L<27;L++)best[L]=-99;
  for(int p=0;p<np;p++){short*P=perms+(long)p*N; int inv[N]; for(int k=0;k<N;k++)inv[P[k]]=k;
   for(int e=0;e<2;e++)for(int m=0;m<2;m++){
    int ct[N]; for(int k=0;k<N;k++) ct[k]=num[e][(m==0? car[P[k]] : car[k])-'A'];
    int kidx[24],px[24],cx[24]; for(int j=0;j<24;j++){kidx[j]= m==0? cp[j] : inv[cp[j]]; px[j]=num[e][cl[j]]; cx[j]=ct[kidx[j]];}
    for(int L=1;L<=26;L++){
      int ok=1, alldet=1, nca[26], ca[26][312], cb[26][312];
      for(int r=0;r<L&&ok;r++){int seen=0; nca[r]=0;
        for(int u=0;u<12;u++){int a=U[u],b=-1,good=1;
          for(int j=0;j<24;j++){if(kidx[j]%L!=r)continue; seen=1; int bb=((cx[j]-a*px[j])%26+26)%26; if(b<0)b=bb; else if(b!=bb){good=0;break;}}
          if(!seen)break; if(good){ca[r][nca[r]]=a;cb[r][nca[r]]=b;nca[r]++;}}
        if(!seen){alldet=0; if(L<=13){nca[r]=0; for(int u=0;u<12;u++)for(int b=0;b<26;b++){ca[r][nca[r]]=U[u];cb[r][nca[r]]=b;nca[r]++;}} else nca[r]=-1; continue;} if(nca[r]==0)ok=0; else if(nca[r]>1)alldet=0;}
      if(!ok)continue; cons[L]++; if(alldet)det[L]++;
      int full=1; for(int r=0;r<L;r++)if(nca[r]<0)full=0;
      if(full){ /* every class has crib letters: pick each class's map by coordinate ascent on quadgrams, 4 restarts */
        float bs=-99; int bpo[N]; unsigned rs=p*131+L*7+e*3+m;
        for(int rst=0;rst<4;rst++){int ch[26]; for(int r=0;r<L;r++){rs=rs*1103515245+12345; ch[r]=(rs>>16)%nca[r];}
          float cur=-99; int improved=1, po[N];
          for(int round=0;round<6&&improved;round++){improved=0;
            for(int r=0;r<L;r++)for(int c=0;c<nca[r];c++){int old=ch[r]; ch[r]=c; int pt[N];
              for(int k=0;k<N;k++){int rr=k%L; int x=((ct[k]-cb[rr][ch[rr]])%26+26)%26*inva[ca[rr][ch[rr]]]%26; pt[k]=den[e][x];}
              if(m==1){for(int i=0;i<N;i++)po[i]=pt[inv[i]];} else memcpy(po,pt,sizeof pt);
              float sc=score(po); if(sc>cur+1e-6){cur=sc;improved=1; if(sc>bs){bs=sc;memcpy(bpo,po,sizeof po);}} else ch[r]=old;}}}
        if(bs>best[L])best[L]=bs;
        if(bs>-5.0){char o[N+1];for(int i=0;i<N;i++)o[i]='A'+bpo[i];o[N]=0; printf("HIT perm=%d num=%c model=%c L=%d score=%.3f pt=%s\n",p,e?'K':'A',m?'B':'A',L,bs,o);}}
    }}}
  printf("SUMMARY perms=%d\n",np); for(int L=1;L<=26;L++)printf("L=%d consistent=%ld determined=%ld best_qg=%.3f\n",L,cons[L],det[L],best[L]);
  return 0;}
