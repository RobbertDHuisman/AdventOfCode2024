import pandas as pd

def get_bad_rows_and_good_middles(rules, rows):
    bad_rows = []
    good_middles = []

    for i in rows:
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

        if good == 0:
            bad_rows.append(i)

        else:
            good_middles.append(int(i[int(len(i)/2)]))

    nr_bad_rows = len(bad_rows)

    return bad_rows, good_middles, nr_bad_rows

def reorder(rules, bad_rows):
    new_rows = []

    for i in bad_rows:
        for j in range(0, len(i) - 1):
            befores = rules[rules["after"] == int(i[j])]["before"]
            for k in range(j+1, len(i)):
                for m in befores:
                    if int(i[k]) == m:
                        new_row = i.copy()
                        new_row[j] = i[k]
                        new_row[k] = i[j]

        for n in range(1, len(i)):
            afters = rules[rules["before"] == int(i[n])]["after"]
            for o in range(0, n-1):
                for p in afters:
                    if int(i[o]) == p:
                        new_row = i.copy()
                        new_row[n] = i[o]
                        new_row[o] = i[n]
        new_rows.append(new_row)

    return new_rows

def main():
    rules = pd.read_csv("input_rules.csv", delimiter="|", names=["before", "after"], engine="python")
    orders = pd.read_csv("input_orders.csv", delimiter="|", names=["orders"], engine="python")
    orders["orders"] = orders["orders"].str.split(",")
    rows = []
    for i in orders["orders"]:
        rows.append(i)

    bad_rows, good_middles_not_needed, nr_bad_rows = get_bad_rows_and_good_middles(rules, rows)
    good_middles = []

    while nr_bad_rows > 0:
        new_rows = reorder(rules, bad_rows)
        bad_rows, good_middles_to_add, nr_bad_rows = get_bad_rows_and_good_middles(rules, new_rows)
        good_middles.append(sum(good_middles_to_add))
        print(f"bad rows left {nr_bad_rows}, added good middles {good_middles_to_add}")

    print(sum(good_middles))

main()