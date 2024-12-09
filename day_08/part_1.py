import csv
import re

def load_data(filename):
    map = []
    all_characters = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, quoting=csv.QUOTE_NONE)

        for row in csv_file:
            map.append(row[0])
            for i in row[0]:
                if i != ".":
                    all_characters.append(i)

    characters = list(set(all_characters))
    return map, characters

def get_locations(map, character):
    locations = []
    for i in range(0, len(map)):
        locations_in_row = re.finditer(f"{character}", map[i])
        if locations_in_row != []:
            for j in locations_in_row:
                locations.append([i, j.start()])

    return locations

def find_all_antinodes(map, locations):
    antinodes = []
    for i in range(0, len(locations)):
        for j in range(i+1, len(locations)):
            distance_x = locations[j][0] - locations[i][0]
            distance_y = locations[j][1] - locations[i][1]
            antinodes.append([locations[i][0] - distance_x, locations[i][1] - distance_y])
            antinodes.append([locations[j][0] + distance_x, locations[j][1] + distance_y])

    return antinodes

def make_set_of_possible_antinodes(map, antinodes):
    unique_antinodes = []
    for i in antinodes:
        if i not in unique_antinodes:
            if i[0] >= 0 and i[0] < len(map) and i[1] >= 0 and i[1] < len(map[0]):
                unique_antinodes.append(i)

    return unique_antinodes

def main():
    map, characters = load_data("input.csv")
    antinodes = []
    for i in characters:
        locations = get_locations(map, i)
        for j in find_all_antinodes(map, locations):
            antinodes.append(j)

    true_antinodes = make_set_of_possible_antinodes(map, antinodes)
    print(len(true_antinodes))

main()