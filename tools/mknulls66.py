import random
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
with open('nulls_extra.txt','w') as f:
    for i in range(5,25):
        l=list(K4); random.Random(6600+i).shuffle(l); f.write(f"NULL{i} "+''.join(l)+"\n")
