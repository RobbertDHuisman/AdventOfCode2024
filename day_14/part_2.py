from part_1 import load_data, find_location_after_seconds

def check_right_side(locations, top):
    directions = []
    location = [top[0] + 1, top[1] + 1]
    while location[0] != top[0]:
        found_right = 0
        while found_right == 0:
            for j in locations:
                if j[0] == location[0] - 1 and j[1] == location[1]:
                    location = j
                    directions.append("left")
                    found_right = 1
                    break
                elif j[0] == location[0] + 1 and j[1] == location[1] + 1:
                    location = j
                    directions.append("down-right")
                    found_right = 1
                    break
                elif j[0] == location[0] and j[1] == location[1] + 1:
                    location = j
                    directions.append("down")
                    found_right = 1
                    break
            
                if j == locations[-1]:
                    found_right = -1

        if found_right == -1:
            break
    
    if len(directions) > 8:
        if directions[0] == "down-right":
            location = location
    else:
        location = [location[0] + 1, location[1] + 1]

    return location

def check_left_side(locations, top):
    directions = []
    location = [top[0] - 1, top[1] + 1]
    while location[0] != top[0]:
        found_right = 0
        while found_right == 0:
            for j in locations:
                if j[0] == location[0] + 1 and j[1] == location[1]:
                    location = j
                    directions.append("right")
                    found_right = 1
                    break
                elif j[0] == location[0] - 1 and j[1] == location[1] + 1:
                    location = j
                    directions.append("down-left")
                    found_right = 1
                    break
                elif j[0] == location[0] and j[1] == location[1] + 1:
                    location = j
                    directions.append("down")
                    found_right = 1
                    break
            
                if j == locations[-1]:
                    found_right = -1

        if found_right == -1:
            break
    
    if len(directions) > 8:
        if directions[0] == "down-left":
            location = location
    else:
        location = [location[0] - 1, location[1] - 1]

    return location

def is_christmas_tree(locations, top):
    if check_right_side(locations, top) == check_left_side(locations, top):
        return True
    else:
        return False


def find_possible_tops_of_tree(locations):
    tops = []
    for i in locations:
        found_left = 0
        found_right = 0
        while found_left == 0 or found_right == 0:
            for j in locations:
                if j[1] == i[1] + 1:
                    if j[0] == i[0] - 1:
                        found_left = 1
                    elif j[0] == i[0] + 1:
                        found_right = 1

                if j == locations[-1]:
                    if found_left == 0:
                        found_left = -1
                    if found_right == 0:
                        found_right = -1

        if found_left == 1 and found_right == 1:
            tops.append(i)
    
    return tops

def print_map(locations, height, width):
    map = []
    row = []
    for i in range(0, width):
        row.append(0)

    for j in range(0, height):
        map.append(row)

    for k in locations:
        row = map[k[1]].copy()
        row[k[0]] +=1
        map.pop(k[1])
        map.insert(k[1], row)

    print(map)

def main():
    file = "input"
    if file in ("example", "example_tree"):
        height = 9
        width = 11
    else:
        height = 103
        width = 101

    locations, velocity = load_data(f"{file}.csv")
    found_it = 0
    seconds = 1
    while found_it == 0:
        print(seconds)
        locations = find_location_after_seconds(locations, velocity, height, width, 1)
        tops = find_possible_tops_of_tree(locations)
        if tops != []:
            for j in tops:
                if is_christmas_tree(locations, j):
                    found_it = -1
                    print_map(locations, height, width)
                    print(seconds, j)
                    break
        
        if found_it == 1:
            break
    
        seconds += 1

main()