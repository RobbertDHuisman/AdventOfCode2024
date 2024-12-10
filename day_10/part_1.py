import csv
import re

def load_data(filename):
    map = []
    trailheads = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)

        nr_rows = 0
        for row in csv_file:
            map.append(row[0])
            for i in range(0, len(row)):
                trailheads_found = re.finditer('0', row[0])
                for j in trailheads_found:
                    trailheads.append([nr_rows, j.start()])
            nr_rows += 1

    return map, trailheads

def find_adjacent_locations(location):
    return [[location[0] - 1, location[1]],
        [location[0], location[1] + 1],
        [location[0] + 1, location[1]],
        [location[0], location[1] - 1]
        ]

def check_position_inside_map(height_map, width_map, location):
    if location[0] >= 0 and location[0] < height_map and location[1] >= 0 and location[1] < width_map:
        return True
    else:
        return False

def check_height_next_step(current_height, new_height):
    if new_height - current_height == 1:
        return True
    else:
        return False

def get_unique_list(list):
    unique_list = []
    for i in list:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list

def find_trails(map, trailhead, part):
    height_map = len(map)
    width_map = len(map[0])
    trail_positions = []
    trail_positions.append(trailhead)
    current_height = 0
    while trail_positions != [] and current_height < 9:
        new_positions = []
        for i in trail_positions:
            adjacent_locations = find_adjacent_locations(i)
            for j in adjacent_locations:
                if check_position_inside_map(height_map, width_map, j) and check_height_next_step(current_height, int(map[j[0]][j[1]])):
                    new_positions.append(j)
        if part == 1:
            trail_positions = get_unique_list(new_positions)
        elif part == 2:
            trail_positions = new_positions
        current_height += 1
    nr_of_trails = len(trail_positions)

    return nr_of_trails

def main():
    part = 2
    map, trailheads = load_data("input.csv")
    trail_ends = []
    for i in trailheads:
        trail_ends_found = find_trails(map, i, part) 
        trail_ends.append(trail_ends_found)

    print(sum(trail_ends))


main()