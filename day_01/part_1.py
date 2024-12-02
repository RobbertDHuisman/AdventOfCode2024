import pandas as pd

df = pd.read_csv("input.csv", delimiter="   ", names=["a", "b"], engine="python")

def part_1():
    left = df["a"].sort_values().reset_index()
    right = df["b"].sort_values().reset_index()
    distance = abs(left["a"] - right["b"])
    total = sum(distance)
    print(total)

