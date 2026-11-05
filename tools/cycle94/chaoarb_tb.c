/* Cycle 94b: transpose, then Chaocipher (input wheel enumerated, output wheel arbitrary).
   PT[j] = R0[u[perm[j]]]; crib test = consistency/injectivity of u[perm[CI]] against the cribs. perm: n*97 int16. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static void opL(unsigned char*w,int i){unsigned char t[26];for(int k=0;k<26;k++)t[k]=w[(i+k)%26];unsigned char x=t[1];memmove(t+1,t+2,12);t[13]=x;memcpy(w,t,26);}
static void opR(unsigned char*w,int i){unsigned char t[26];for(int k=0;k<26;k++)t[k]=w[(i+1+k)%26];unsigned char x=t[2];memmove(t+2,t+3,11);t[13]=x;memcpy(w,t,26);}
int main(int argc,char**argv){ const char*CT=argv[1]; FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(na*26); fread(A,26,na,f); fclose(f); long M=atol(argv[4]); if(M>na)M=na;
  f=fopen(argv[3],"rb"); fseek(f,0,2); long np=ftell(f)/194; fseek(f,0,0); short*P=malloc(np*194); fread(P,194,np,f); fclose(f);
  int pa[24],pb[24],npair=0,dif[300][2],nd=0; for(int a=0;a<24;a++)for(int b=a+1;b<24;b++){ if(PT[a]==PT[b]){pa[npair]=a;pb[npair]=b;npair++;} else {dif[nd][0]=a;dif[nd][1]=b;nd++;} }
  long long hits=0,eqok=0;
  #pragma omp parallel for schedule(dynamic,16) reduction(+:hits,eqok)
  for(long a=0;a<M;a++) for(int d=0;d<2;d++){ unsigned char in[26],out[26],u[97]; memcpy(in,A+a*26,26); for(int k=0;k<26;k++)out[k]=k;
    for(int j=0;j<97;j++){ int x=CT[j]-65,i=0; while(in[i]!=x)i++; u[j]=out[i]; if(d==0){opL(in,i);opR(out,i);} else {opR(in,i);opL(out,i);} }
    for(long t=0;t<np;t++){ const short*p=P+t*97; int ok=1;
      for(int q=0;q<npair&&ok;q++) if(u[p[CI[pa[q]]]]!=u[p[CI[pb[q]]]]) ok=0;
      if(!ok) continue; eqok++;
      for(int q=0;q<nd&&ok;q++) if(u[p[CI[dif[q][0]]]]==u[p[CI[dif[q][1]]]]) ok=0;
      if(ok){ hits++;
        #pragma omp critical
        printf("HIT a=%ld dir=%d t=%ld\n",a,d,t); } } }
  printf("ALPHABETS %ld PERMS %ld RUNS %lld EQ_OK %lld HITS %lld\n",M,np,(long long)M*np*2,eqok,hits); return 0; }
