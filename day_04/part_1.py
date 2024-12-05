import pandas as pd
import re

df = pd.read_csv("input.csv", names=["a"], engine="python")
count = 0
for i in range(0, len(df)):
    for x in re.findall('XMAS', df["a"][i]):
        count = count + 1
    
    for s in re.findall('SAMX', df["a"][i]):
        count = count + 1        


for j in range(0, len(df)-3):    
    for m in re.finditer('X', df["a"][j]):
        indexx = m.start(0)
        if df["a"][j+1][indexx] + df["a"][j+2][indexx] + df["a"][j+3][indexx] == "MAS":
            count = count + 1        
        
        if indexx > 2:
            if df["a"][j+1][indexx-1] + df["a"][j+2][indexx-2] + df["a"][j+3][indexx-3] == "MAS":
                count = count + 1    

        if indexx < len(df["a"][j])-3:
            if df["a"][j+1][indexx+1] + df["a"][j+2][indexx+2] + df["a"][j+3][indexx+3] == "MAS":
                count = count + 1        

for j in range(3, len(df)):    
    for m in re.finditer('X', df["a"][j]):
        indexx = m.start(0)
        if df["a"][j-1][indexx] + df["a"][j-2][indexx] + df["a"][j-3][indexx] == "MAS":
            count = count + 1        
        
        if indexx > 2:
            if df["a"][j-1][indexx-1] + df["a"][j-2][indexx-2] + df["a"][j-3][indexx-3] == "MAS":
                count = count + 1    

        if indexx < len(df["a"][j])-3:
            if df["a"][j-1][indexx+1] + df["a"][j-2][indexx+2] + df["a"][j-3][indexx+3] == "MAS":
                count = count + 1               
    
print(count)