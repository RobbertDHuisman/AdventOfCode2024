import pandas as pd
import re

def find_guard(df):
    location = []
    for i in range(0, len(df)):
            x = re.finditer('(<|>|\^|v)', df["a"][i])
            for match in x:
                location.append(i)
                location.append(match.start())
                direction = match.group()

    return location, direction

def find_next_location(location, direction):
    if direction == "^":
        next_location = [location[0] - 1, location[1]]

    elif direction == "v":
        next_location = [location[0] + 1, location[1]]

    elif direction == ">":
        next_location = [location[0], location[1] + 1]

    elif direction == "<":
        next_location = [location[0], location[1] - 1]

    return next_location

def determine_next_step(df, location, next_location, direction):
    if df["a"][next_location[0]][next_location[1]] == "#":
        new_location = location
        if direction == "^":
            new_direction = ">"

        elif direction == "v":
            new_direction = "<"

        elif direction == ">":
            new_direction = "v"

        elif direction == "<":
            new_direction = "^"
            
    else:
        new_location = next_location
        new_direction = direction

    return new_location, new_direction

def set_location_to_x(df, location):
    df.loc[location[0], "a"] = df["a"][location[0]][0:location[1]] + "X" + df["a"][location[0]][location[1] + 1:len(df["a"][location[0]])]
    return df

def determine_guard_left(df, next_location):
    if next_location[0] < 0 or next_location[0] == len(df) or next_location[1] < 0 or next_location[1] == len(df["a"]):
        guard_left = 1
    else:
        guard_left = 0

    return guard_left

def count_positions(df):
    positions = 0
    for i in df["a"]:
        positions = positions + i.count("X")

    return positions

def main():
    df = pd.read_csv("input.csv", names=["a"], engine="python")

    location, direction = find_guard(df)
    guard_left = 0
    while guard_left == 0:
        next_location = find_next_location(location, direction)
        guard_left = determine_guard_left(df, next_location)
        df = set_location_to_x(df, location)

        if guard_left == 0:
            location, direction = determine_next_step(df, location, next_location, direction)

    positions = count_positions(df)
    print(positions)

main()