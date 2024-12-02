import pandas as pd

df = pd.read_csv("input.csv", delimiter="   ", names=["a", "b"], engine="python")

product = []
for i in df["a"]:
    count = 0
    for j in range(0, len(df)):
        if df["b"][j] == i:
            count = count + 1
    if count > 0:
        product.append(i*count)

total = sum(product)
print(total)