"""Cycle 160: how much of vocabulary x vocabulary Quagmire IV was already covered?
(a) behind the bank p<=16: cycle 28 covered ordered pairs of 268 themed alphabets (analysis/q4_alpha_names.txt);
    cycle 135 covered PA == CA (Quagmire III).  (b) direct: cycle 11b SAT excluded every alphabet pair for
    p in 1-7, 9-12, 14, 15 (and 17, 18, 21, 22, 25); its phrase hash join covered pairs with one side a keyed
    K1-K3 substring (length 4-30) alphabet.  Approximation for (b): a vocabulary word is 'phrase-covered' if it
    is a substring of the K1-K3 plaintext (its AZ-keyed alphabet is then in the 31,418 phrase set)."""
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def keyed(w):
    s=""
    for c in w+AZ:
        if c not in s: s+=c
    return s
K123=("BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION"
"ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLETHEYUSEDTHEEARTHSMAGNETICFIELDXTHEINFORMATIONWASGATHEREDANDTRANSMITTEDUNDERGRUUNDTOANUNKNOWNLOCATIONXDOESLANGLEYKNOWABOUTTHISTHEYSHOULDITSBURIEDOUTTHERESOMEWHEREXWHOKNOWSTHEEXACTLOCATIONONLYWWTHISWASHISLASTMESSAGEXTHIRTYEIGHTDEGREESFIFTYSEVENMINUTESSIXPOINTFIVESECONDSNORTHSEVENTYSEVENDEGREESEIGHTMINUTESFORTYFOURSECONDSWESTIDBYROWS"
"SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWEREREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTEDTHECANDLEANDPEEREDINTHEHOTAIRESCAPINGFROMTHECHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHINEMERGEDFROMTHEMISTXCANYOUSEEANYTHINGQ")
words=open('vocab.txt').read().split()
U={}
for w in words: U.setdefault(keyed(w),w)
n=len(U); pairs=n*(n-1)
names=[l.strip() for l in open('analysis/q4_alpha_names.txt') if l.strip() and not l.strip().endswith('_rev')]
themed={keyed(x) for x in names if x!='AZ'}
th=sum(1 for a in U if a in themed)
phr=set()
for i in range(len(K123)):
    for L in range(4,31):
        if i+L<=len(K123): phr.add(keyed(K123[i:i+L]))
ph=sum(1 for a in U if a in phr)
print(f"vocabulary words {len(words)}, unique keyed alphabets {n}, ordered pairs with PA != CA {pairs:,}")
print(f"themed (cycle 28) alphabets among them: {th}; pairs covered behind the bank: {th*(th-1):,} ({th*(th-1)/pairs:.5%})")
cov=pairs-(n-ph)*(n-ph-1)
print(f"phrase-set (cycle 11b) alphabets among them: {ph}; direct pairs with >=1 phrase side: {cov:,} ({cov/pairs:.3%})")
print("direct p 1-7, 9-12, 14, 15: covered for ALL pairs by cycle 11b SAT; p 8, 13, 16: new for "
      f"{(n-ph)*(n-ph-1)/pairs:.3%} of pairs (cycle 11b SAT left these periods open)")
print(f"=> bank p 1-16: {1-th*(th-1)/pairs:.4%} of ordered pairs x every permutation is new; direct: only p 8, 13, 16 (and 17-26) are new")
