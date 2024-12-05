import pandas as pd
import re

df = pd.read_csv("input.csv", names=["a"], engine="python")
count = 0

# for j in range(1, 3):    
for j in range(1, len(df)-1):    
    for m in re.finditer('A', df["a"][j]):
        indexx = m.start(0)
        print(indexx)
        options = ["MMSS", "MSMS", "SSMM", "SMSM"]
        if indexx > 0 and indexx < len(df["a"][j]) -1:
            if df["a"][j-1][indexx-1] + df["a"][j-1][indexx+1] + df["a"][j+1][indexx-1] + df["a"][j+1][indexx+1] in options:
                count = count + 1             
    
print(count)