/* Cycle 148: running keys from digit streams of mathematical constants (pi, e, sqrt2, sqrt3, sqrt5, phi, ln2, gamma),
   key[i] = stream[o + i] + c (mod 26), any start o, any constant shift c (covers A=0 / A=1 conventions).
   Forms: Vigenere p = L - k, Beaufort p = k - L, variant p = L + k; tableau A-Z or KRYPTOS. Direct or behind a bank
   permutation S (both directions): ix=0 model Q (stream L[i]=CT[S[i]], crib at plaintext position i), ix=1 carved
   (stream = CT, crib p at stream position S[p]). Exact: for the two smallest crib stream positions s1<s2 the needed
   key difference picks candidate starts from a (gap,diff) index; each candidate is verified on all 24 crib letters.
   Prints configs with >= MINM matches (default 22) and their full decryption.
   usage: constkey CT streams.txt perms.bin|- label lo hi [minm] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static const char *CRIB="EASTNORTHEASTBERLINCLOCK"; static int cpos[24];
#define MS 48
static char sname[MS][32]; static int slen[MS], *sv[MS], ns=0;
static int *idx_[MS][97][26], cnt[MS][97][26];
int main(int ac,char**av){
  if(ac<7)return 1; const char*CT=av[1]; const char*lab=av[4]; long lo=atol(av[5]),hi=atol(av[6]); int minm=ac>7?atoi(av[7]):22;
  {int k=0;for(int i=21;i<=33;i++)cpos[k++]=i;for(int i=63;i<=73;i++)cpos[k++]=i;}
  FILE*f=fopen(av[2],"r"); while(ns<MS&&fscanf(f,"%31s %d",sname[ns],&slen[ns])==2){sv[ns]=malloc(slen[ns]*sizeof(int));for(int i=0;i<slen[ns];i++)if(fscanf(f,"%d",&sv[ns][i])!=1)return 4;ns++;} fclose(f);
  for(int s=0;s<ns;s++){int n=slen[s]-97; if(n<1)n=1;
    for(int g=1;g<97;g++){for(int d=0;d<26;d++)cnt[s][g][d]=0; for(int o=0;o<n;o++)cnt[s][g][(sv[s][o+g]-sv[s][o]+26)%26]++;
      for(int d=0;d<26;d++){idx_[s][g][d]=malloc((cnt[s][g][d]+1)*sizeof(int));cnt[s][g][d]=0;}
      for(int o=0;o<n;o++){int d=(sv[s][o+g]-sv[s][o]+26)%26; idx_[s][g][d][cnt[s][g][d]++]=o;}}}
  long np=1; short*bank=NULL; if(strcmp(av[3],"-")){f=fopen(av[3],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np; long cfg=0,cand=0,hits=0; int bestm=0;
  for(long q=lo;q<hi;q++)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int nu=0;nu<2;nu++)for(int ix=0;ix<(bank?2:1);ix++){
      const char*N=NUMS[nu]; int id[26]; for(int i=0;i<26;i++)id[N[i]-'A']=i;
      int L[97],sp[24],pv[24]; for(int i=0;i<97;i++)L[i]=id[CT[ix==0?S[i]:i]-'A'];
      for(int k=0;k<24;k++){sp[k]=ix==0?cpos[k]:S[cpos[k]]; pv[k]=id[CRIB[k]-'A'];}
      int a=0,b=1; for(int k=0;k<24;k++)if(sp[k]<sp[a])a=k; if(a==b)b=0; for(int k=0;k<24;k++)if(k!=a&&sp[k]<sp[b])b=k;
      for(int form=0;form<3;form++){
        int need[24]; for(int k=0;k<24;k++){int l=L[sp[k]],p=pv[k]; need[k]=form==0?(l-p+26)%26:form==1?(l+p)%26:(p-l+26)%26;}
        int g=sp[b]-sp[a], d=(need[b]-need[a]+26)%26;
        for(int s=0;s<ns;s++){ cfg++; int n=slen[s]-97; int *lst=idx_[s][g][d]; int nc=cnt[s][g][d];
          for(int t=0;t<nc;t++){int o=lst[t]-sp[a]; if(o<0||o+97>slen[s])continue; cand++;
            int c=(need[a]-sv[s][o+sp[a]]+26)%26, m=0, miss=0;
            for(int k=0;k<24;k++){if((sv[s][o+sp[k]]+c)%26==need[k])m++; else if(++miss>24-minm)break;}
            if(m>bestm)bestm=m;
            if(m>=minm){hits++; char out[98],pt[98]; for(int i=0;i<97;i++){int kk=(sv[s][o+i]+c)%26,l=L[i];
                int p=form==0?(l-kk+26)%26:form==1?(kk-l+26)%26:(kk+l)%26; out[i]=N[p];}
              if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]]; pt[97]=0;
              printf("S %s %s o=%d c=%d form=%d num=%d ix=%d perm=%ld dir=%d m=%d %s\n",lab,sname[s],o,c,form,nu,ix,q,dir,m,pt);}}
          (void)n;}}}}
  printf("C %s cfg=%ld cand=%ld hits=%ld bestm=%d\n",lab,cfg,cand,hits,bestm); return 0;}
