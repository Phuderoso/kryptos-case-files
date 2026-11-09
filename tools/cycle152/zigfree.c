/* Cycle 152: zig-zag autokey with a FREE form sequence (any word-keyed or arbitrary-length form cycle), plus progressive shift.
   Sub-layer equation at stream position j:  c_j = s + d*j + a_F*p_j + b_F*f_j (mod 26), F = F_j in {V,B,X} chosen freely per position:
     Vigenere (a=+1,b=+1), Beaufort (a=-1,b=+1), variant (a=+1,b=-1).  d = 0..25 progressive step (d=0: plain zig-zag).
   Feed f_j = c_{j-L} (CT autokey) or p_{j-L} (PT autokey), lag L = 1..96. Numbering A-Z or KRYPTOS.
   Any word-keyed form sequence (letter mod 3 or mod 2 under any residue->form map, any word, any phase) and every fixed
   cycle of any length is a special case, so the free model is a strict superset (an exact exclusion of the free model
   excludes all of them).
   For each crib k the admissible shifts are {c_j - d*j - a_F*p - b_F*f : F in V,B,X}; m = max over s of #cribs admitting s.
   A true configuration gives m = n (all eligible cribs). One wrong crib letter breaks one equation (m >= n-1); one wrong
   carved letter can break two with a CT feed (its own crib equation and the one that uses it as feed L later): m >= n-2.
   Layout as cycle 150: direct, or behind bank permutation S (both directions), ix=0 model Q, ix=1 carved order.
   usage: zigfree CT perms.bin|- label lo hi minm_ct minn (print CT m>=minm_ct or m>=n-2 with n>=minn; PT m==n with n>=9) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static const char *CRIB="EASTNORTHEASTBERLINCLOCK"; static int cpos[24];
int main(int ac,char**av){
  if(ac<8)return 1; const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]); int minct=atoi(av[6]),minpt=atoi(av[7]);
  {int k=0;for(int i=21;i<=33;i++)cpos[k++]=i;for(int i=63;i<=73;i++)cpos[k++]=i;}
  const int A[3]={1,25,1},B[3]={1,1,25};
  long np=1; short*bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np; long cfg=0,printed=0; int bestct=0,bestctn=0,hist[25]={0},fullct[25]={0},nearct[25]={0},near2ct[25]={0},histpt[25]={0},bestptn=0,bestptgap=99;
  for(long q=lo;q<hi;q++)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int nu=0;nu<2;nu++)for(int ix=0;ix<(bank?2:1);ix++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i;
      int c[97],kp[97],kj[24],kv[24]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)c[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kj[k]=cpos[k];}
      else{for(int i=0;i<97;i++)c[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kj[k]=S[cpos[k]];}
      for(int k=0;k<24;k++){kv[k]=idx[CRIB[k]-'A'];kp[kj[k]]=kv[k];}
      for(int feed=0;feed<2;feed++)for(int L=1;L<=96;L++){
        int base[24][3],jj[24],n=0;
        for(int k=0;k<24;k++){int j=kj[k]; if(j<L)continue; int f=feed?kp[j-L]:c[j-L]; if(f<0)continue;
          for(int F=0;F<3;F++)base[n][F]=((c[j]-A[F]*kv[k]-B[F]*f)%26+26*26)%26; jj[n]=j; n++;}
        if(n==0)continue;
        for(int d=0;d<26;d++){ cfg++;
          int cnt[26]={0},m=0,sb=0;
          for(int t=0;t<n;t++){int sh=(d*jj[t])%26; unsigned msk=0;
            for(int F=0;F<3;F++){int s=base[t][F]-sh; if(s<0)s+=26; if(!(msk>>s&1)){msk|=1u<<s; if(++cnt[s]>m){m=cnt[s];sb=s;}}}}
          if(!feed){hist[m]++; if(m>bestct){bestct=m;bestctn=n;} if(m==n)fullct[n]++; else if(m==n-1)nearct[n]++; else if(m==n-2)near2ct[n]++;}
          else{ if(m==n){histpt[n]++; if(n>bestptn)bestptn=n;} if(n>=6&&n-m<bestptgap)bestptgap=n-m; }
          if((!feed&&(m>=minct||(m>=n-2&&n>=minpt)))||(feed&&m==n&&n>=9)){
            /* report the admissible forms at each crib position for shift sb */
            char fr[25]; int t=0; for(int k=0;k<24;k++){int j=kj[k]; int f=(j<L)?-1:(feed?kp[j-L]:c[j-L]); if(f<0){fr[k]='-';continue;}
              int sh=(d*j)%26, a=0; for(int F=0;F<3;F++){int s=((c[j]-A[F]*kv[k]-B[F]*f-sh)%26+26*26)%26; if(s==sb)a|=1<<F;}
              fr[k]="0VBMXNYT"[a]; t++;} fr[24]=0; /* letters: V,B,X single; M=V|B, N=V|X, Y=B|X, T=all; 0 = none */
            printf("S %s feed=%s L=%d d=%d perm=%ld dir=%d ix=%d num=%d s=%d m=%d n=%d forms=%s\n",lab,feed?"PT":"CT",L,d,q,dir,ix,nu,sb,m,n,fr); printed++;}
        }
      }}}
  printf("C %s cfg=%ld printed=%ld bestCT=%d(n=%d) bestPTfull_n=%d bestPTgap(n>=6)=%d histCT",lab,cfg,printed,bestct,bestctn,bestptn,bestptgap);
  for(int i=0;i<=24;i++)if(hist[i])printf(" %d:%d",i,hist[i]); printf(" CTfull(n:cnt)"); for(int i=0;i<=24;i++)if(fullct[i])printf(" %d:%d",i,fullct[i]); printf(" CTnear(n:cnt)"); for(int i=0;i<=24;i++)if(nearct[i])printf(" %d:%d",i,nearct[i]); printf(" CTnear2(n:cnt)"); for(int i=0;i<=24;i++)if(near2ct[i])printf(" %d:%d",i,near2ct[i]); printf(" histPTfull"); for(int i=0;i<=24;i++)if(histpt[i])printf(" %d:%d",i,histpt[i]); printf("\n"); return 0;}
