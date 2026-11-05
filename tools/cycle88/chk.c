// Cycle 88: exact periodic-key check behind permutations of a 92-letter text.
// usage: chk perms.bin CT92 PMAX hitsfile   (cribs: EASTNORTHEAST at 20, BERLINCLOCK at 60 in W-free coordinates)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 92
static const char*AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
int idx[2][26];
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,2); long sz=ftell(f); rewind(f);
  unsigned char*buf=malloc(sz); fread(buf,1,sz,f); fclose(f); long np=sz/N;
  const char*ct=argv[2]; int PMAX=atoi(argv[3]); FILE*H=fopen(argv[4],"w");
  for(int i=0;i<26;i++){idx[0][AZ[i]-'A']=i; idx[1][KA[i]-'A']=i;}
  int cp[24]; char cl[24]; const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK"; int nc=0;
  for(int i=0;i<13;i++){cp[nc]=20+i;cl[nc++]=c1[i];} for(int i=0;i<11;i++){cp[nc]=60+i;cl[nc++]=c2[i];}
  long cnt[40]={0};
  for(long q=0;q<np;q++){ unsigned char*P=buf+q*N; int inv[N]; for(int j=0;j<N;j++) inv[P[j]]=j;
    for(int model=0;model<2;model++) for(int pa=0;pa<2;pa++) for(int ca=0;ca<2;ca++) for(int beau=0;beau<2;beau++)
    for(int p=1;p<=PMAX;p++){
      int key[40]; for(int r=0;r<p;r++) key[r]=-1; int ok=1;
      for(int t=0;t<nc&&ok;t++){ int i=cp[t]; int j=inv[i]; char c; int ki;
        if(model==0){ c=ct[j]; ki=i%p; } else { c=ct[j]; ki=j%p; }
        // model0: substitution keyed on plaintext position, then transposition; model1: transposition, then key on ciphertext position
        int cv=idx[ca][c-'A'], pv=idx[pa][cl[t]-'A']; int k= beau? (cv+pv)%26 : (cv-pv+26)%26;
        if(key[ki]<0) key[ki]=k; else if(key[ki]!=k) ok=0; }
      if(ok){ cnt[p]++; if(p<=PMAX){ { char pt[N+1]; pt[N]=0; for(int j=0;j<N;j++){ int i=P[j]; int ki= model==0? i%p : j%p; int cv=idx[ca][ct[j]-'A'];
              if(key[ki]<0){pt[i]='.';continue;} int pv= beau? (key[ki]-cv+26)%26 : (cv-key[ki]+26)%26; pt[i]= (pa?KA:AZ)[pv]; }
            fprintf(H,"%ld %d %d %d %d %d %s\n",q,model,pa,ca,beau,p,pt);} } break; } // smallest consistent p only
    }}
  for(int p=1;p<=PMAX;p++) printf("p%d:%ld ",p,cnt[p]); printf("\n"); return 0; }
