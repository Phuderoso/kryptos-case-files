// Cycle 58: Portax (ACA period-pair digraphic, Porta-style slide), exact crib test.
// usage: portax texts.txt alpha.bin nalpha perm.bin nperm pmax
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *CRIB[2]={"EASTNORTHEAST","BERLINCLOCK"}; static const int CS[2]={21,63};
int CI[24],CV[24];
// Portax involution on alphabet indices with shift k
static inline void ptx(int a,int b,int k,int*o1,int*o2){
  int r1,c1; if(a<13){r1=0;c1=a;} else {r1=1;c1=((a-13-k)%13+13)%13;}
  int c2=b>>1,r2=b&1;
  #define UP(r,c) ((r)==0?(c):13+((c)+k)%13)
  if(c1!=c2){*o1=UP(r1,c2);*o2=2*c1+r2;} else {*o1=UP(1-r1,c1);*o2=2*c1+(1-r2);}
}
// test: ct = alphabet indices (97), want[i]=-1 or required plaintext index at position i. returns 1 if consistent; fills key
int test(const int*ct,const int*want,int p,int*key,int*npairs){
  int np=0;
  for(int j=0;j<p;j++){ int ok=-1;
    for(int k=0;k<13&&ok<0;k++){ int good=1;
      for(int t=j;t+p<97&&good;t+=2*p){ int s=t+p; if(want[t]<0&&want[s]<0) continue;
        int o1,o2; ptx(ct[t],ct[s],k,&o1,&o2);
        if(want[t]>=0&&o1!=want[t]) good=0; if(want[s]>=0&&o2!=want[s]) good=0; }
      if(good) ok=k; }
    if(ok<0) return 0; key[j]=ok; }
  for(int j=0;j<p;j++) for(int t=j;t+p<97;t+=2*p) if(want[t]>=0||want[t+p]>=0) np++;
  *npairs=np; return 1;
}
int main(int argc,char**argv){
  int n=0; for(int s=0;s<2;s++) for(int i=0;CRIB[s][i];i++){CI[n]=CS[s]+i;CV[n]=CRIB[s][i]-65;n++;}
  FILE*f=fopen(argv[2],"rb"); int na=atoi(argv[3]); unsigned char*A=malloc(na*26); fread(A,26,na,f); fclose(f);
  int nt=atoi(argv[5]); short*P=malloc((long)nt*194); f=fopen(argv[4],"rb"); nt=fread(P,194,nt,f); fclose(f);
  int pmax=atoi(argv[6]);
  char name[64],txt[128]; f=fopen(argv[1],"r");
  while(fscanf(f,"%63s %127s",name,txt)==2){
    long hits=0,tested=0,inf=0;
    for(int a=0;a<na;a++){ int ix[26]; const unsigned char*al=A+a*26; for(int i=0;i<26;i++) ix[al[i]]=i;
      int ct[97]; for(int i=0;i<97;i++) ct[i]=ix[txt[i]-65]; int cv[24]; for(int i=0;i<24;i++) cv[i]=ix[CV[i]];
      for(long t=0;t<nt;t++){ const short*pp=P+t*97; int bad=0; for(int i=0;i<97;i++) if(pp[i]<0) bad=1; if(bad) continue;
        for(int ord=0;ord<2;ord++){ int c2[97],want[97]; for(int i=0;i<97;i++) want[i]=-1;
          if(ord==0){ memcpy(c2,ct,sizeof c2); for(int i=0;i<24;i++) want[pp[CI[i]]]=cv[i]; }   // Portax first, then untranspose
          else { for(int i=0;i<97;i++) c2[i]=ct[pp[i]]; for(int i=0;i<24;i++) want[CI[i]]=cv[i]; } // untranspose, then Portax
          if(t==0&&ord==1) continue; // identity counted once
          for(int p=1;p<=pmax;p++){ int key[64],npairs; tested++;
            if(test(c2,want,p,key,&npairs)){ hits++; if(npairs>=8) inf++;
              if(hits<=20||npairs>=8){ int out[97]; memcpy(out,c2,sizeof out);
                for(int j=0;j<p;j++) for(int s=j;s+p<97;s+=2*p) ptx(c2[s],c2[s+p],key[j],&out[s],&out[s+p]);
                char pt[98]; for(int i=0;i<97;i++){int v=(ord==0)?out[pp[i]]:out[i]; pt[i]=al[v]+65;} pt[97]=0;
                char ks[65]; for(int j=0;j<p;j++) ks[j]='A'+2*key[j]; ks[p]=0;
                printf("%s HIT alpha=%d perm=%ld ord=%d p=%d pairs=%d key=%s pt=%s\n",name,a,t,ord,p,npairs,ks,pt);} } } } } }
    printf("%s SUMMARY tested=%ld hits=%ld informative=%ld\n",name,tested,hits,inf); fflush(stdout);
  }
}
