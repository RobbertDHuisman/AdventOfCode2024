import pandas as pd
import re
from part_1 import find_guard, find_next_location, determine_guard_left, set_location_to_x, determine_next_step

def get_route_guard(df): 
    location, direction = find_guard(df)
    location_guard = location
    guard_left = 0
    while guard_left == 0:
        next_location = find_next_location(location, direction)
        guard_left = determine_guard_left(df, next_location)
        df = set_location_to_x(df, location)

        if guard_left == 0:
            location, direction = determine_next_step(df, location, next_location, direction)

    return df, location_guard

def find_locations_x(df):
    xs = []
    for i in range(0, len(df)):
            location = re.finditer('X', df["a"][i])
            for match in location:
                x = []
                x.append(i)
                x.append(match.start())
                xs.append(x)

    return xs

def make_new_dataframe_with_obstruction(df, location):
    df.loc[location[0], "a"] = df["a"][location[0]][0:location[1]] + "#" + df["a"][location[0]][location[1] + 1:len(df["a"][location[0]])]
    return df

def determine_option_obstruction(df): 
    location, direction = find_guard(df)
    guard_left = 0
    guard_in_loop = 0
    locations_directions = []
    while guard_left == 0:
        next_location = find_next_location(location, direction)
        guard_left = determine_guard_left(df, next_location)
        df = set_location_to_x(df, location)

        if guard_left == 0:
            location_direction = []
            location, direction = determine_next_step(df, location, next_location, direction)
            location_direction.append(location)
            location_direction.append(direction)
            if location_direction in locations_directions:
                guard_in_loop = 1
                guard_left = 1
            else:
                locations_directions.append(location_direction)

    return guard_in_loop

def step_2():
    df = pd.read_csv("input.csv", names=["a"], engine="python")
    df_original = df.copy()

    obstructions = 0
    df_with_route, location_guard = get_route_guard(df)
    xs = find_locations_x(df_with_route)
    for x in xs:
        df_try = df_original.copy()
        if x != location_guard:
            df_obstruct = make_new_dataframe_with_obstruction(df_try, x)

            guard_in_loop = determine_option_obstruction(df_obstruct)

            if guard_in_loop == 1:
                obstructions = obstructions + 1

            print(f"number of obstructions: {obstructions}")

step_2()