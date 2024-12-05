import pandas as pd

good_middles = []
rules = pd.read_csv("input_rules.csv", delimiter="|", names=["before", "after"], engine="python")
orders = pd.read_csv("input_orders.csv", delimiter="|", names=["orders"], engine="python")
orders["orders"] = orders["orders"].str.split(",")

for i in orders["orders"]:
    good = 1
    for j in range(0, len(i) - 1):
        befores = rules[rules["after"] == int(i[j])]["before"]
        for k in range(j+1, len(i)):
            for m in befores:
                if int(i[k]) == m:
                    good = 0

    for n in range(1, len(i)):
        afters = rules[rules["before"] == int(i[n])]["after"]
        for o in range(0, n-1):
            for p in afters:
                if int(i[o]) == p:
                    good = 0

    if good == 1:
        good_middles.append(int(i[int(len(i)/2)]))

print(sum(good_middles))