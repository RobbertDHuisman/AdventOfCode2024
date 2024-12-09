from part_1 import load_data, get_locations

def check_if_node_is_possible(antinode, length_x, length_y):
    if antinode[0] >= 0 and antinode[0] < length_x and antinode[1] >= 0 and antinode[1] < length_y:
        return antinode
    else:
        return None
    
def find_all_antinodes(map, locations):
    length_x = len(map)
    length_y = len(map[0])
    antinodes = []
    if len(locations) > 1:
        for i in range(0, len(locations)):
            antinodes.append(locations[i])
            for j in range(i+1, len(locations)):
                distance_x = locations[j][0] - locations[i][0]
                distance_y = locations[j][1] - locations[i][1]

                step = 1
                while step > 0:
                    new_minus_antinode = [locations[i][0] - (distance_x * step), locations[i][1] - (distance_y * step)]
                    possible_minus = check_if_node_is_possible(new_minus_antinode, length_x, length_y)
                    new_plus_antinode = [locations[i][0] + (distance_x * step), locations[i][1] + (distance_y * step)]
                    possible_plus = check_if_node_is_possible(new_plus_antinode, length_x, length_y)
                    if possible_minus is not None:
                        antinodes.append(possible_minus)
                    if possible_plus is not None:
                        antinodes.append(possible_plus)

                    if possible_plus is None and possible_minus is None:
                        step = 0
                    else:
                        step += 1

    return antinodes

def get_unique_list(antinodes):
    unique_antinodes = []
    for i in antinodes:
        if i not in unique_antinodes:
            unique_antinodes.append(i)

    return unique_antinodes
    

def main():
    map, characters = load_data("input.csv")
    antinodes = []
    for i in characters:
        locations = get_locations(map, i)
        for j in find_all_antinodes(map, locations):
            antinodes.append(j)

    true_antinodes = get_unique_list(antinodes)
    print(len(true_antinodes))

main()