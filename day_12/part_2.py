from part_1 import (
    load_data,
    find_region_area, 
    check_if_other_region, 
    determine_next_region, 
    calculate_price, 
    find_adjacent_locations)

def determine_new_direction(direction, location, areas):
    if direction == "right":
        if [location[0], location[1] + 1] in areas:
            if [location[0] - 1, location[1] + 1] in areas:
                new_direction = "up"
                new_location = [location[0] - 1, location[1] + 1]
                new_sides = 1
            else:
                new_direction = "right"
                new_location = [location[0], location[1] + 1]
                new_sides = 0
        elif [location[0] + 1, location[1]] in areas:
            new_direction = "down"
            new_location = location
            new_sides = 1
        else:
            new_direction = "left"
            new_location = location
            new_sides = 2

    if direction == "down":
        if [location[0] + 1, location[1]] in areas:
            if [location[0] + 1, location[1] + 1] in areas:
                new_direction = "right"
                new_location = [location[0] + 1, location[1] + 1]
                new_sides = 1
            else:
                new_direction = "down"
                new_location = [location[0] + 1, location[1]]
                new_sides = 0
        elif [location[0], location[1] - 1] in areas:
            new_direction = "left"
            new_location = location
            new_sides = 1
        else:
            new_direction = "up"
            new_location = location
            new_sides = 2

    if direction == "left":
        if [location[0], location[1] - 1] in areas:
            if [location[0] + 1, location[1] - 1] in areas:
                new_direction = "down"
                new_location = [location[0] + 1, location[1] - 1]
                new_sides = 1
            else:
                new_direction = "left"
                new_location = [location[0], location[1] - 1]
                new_sides = 0
        elif [location[0] - 1, location[1]] in areas:
            new_direction = "up"
            new_location = location
            new_sides = 1
        else:
            new_direction = "right"
            new_location = location
            new_sides = 2
    
    if direction == "up":
        if [location[0] - 1, location[1]] in areas:
            if [location[0] - 1, location[1] - 1] in areas:
                new_direction = "left"
                new_location = [location[0] - 1, location[1] - 1]
                new_sides = 1
            else:
                new_direction = "up"
                new_location = [location[0] - 1, location[1]]
                new_sides = 0
        elif [location[0], location[1] + 1] in areas:
            new_direction = "right"
            new_location = location
            new_sides = 1
        else:
            new_direction = "down"
            new_location = location
            new_sides = 2

    return new_direction, new_location, new_sides

def find_starting_direction(loc1, loc2):
    if loc1[0] > loc2[0]:
        return "right"
    elif loc1[0] < loc2[0]:
        return "left"
    else:
        if loc1[1] < loc2[1]:
            return "down"
        else:
            return "up"

def get_sides_of_loop(start_direction, start_point, areas):
    steps = []
    areas_visited = []
    sides = 0
    new_direction, new_location, new_sides = determine_new_direction(start_direction, start_point, areas)
    sides += new_sides
    areas_visited.append(new_location)
    steps.append([new_direction, new_location])
    back_at_start = 0

    while back_at_start == 0:
        new_direction, new_location, new_sides = determine_new_direction(new_direction, new_location, areas)
        if new_location not in areas_visited:
            areas_visited.append(new_location)
        sides += new_sides
        if new_direction == start_direction and new_location == start_point:
            back_at_start = 1
        if [new_direction, new_location] in steps:
            back_at_start = 1
            sides -= 1
        steps.append([new_direction, new_location])

    return areas_visited, sides

    

def determine_sides(areas):
    direction = "right"
    starting_point = areas[0]

    areas_visited, sides = get_sides_of_loop(direction, starting_point, areas)

    inside_done = 0
    while inside_done == 0:
        for i in areas:
            run_done = 0
            if i not in areas_visited:
                adjacent_locations = find_adjacent_locations(i)
                for j in adjacent_locations:
                    if j not in areas:
                        print(i)
                        new_starting_point = i
                        new_start_direction = find_starting_direction(i, j)
                        areas_visited_inside, sides_inside = get_sides_of_loop(new_start_direction, new_starting_point, areas)
                        for k in areas_visited_inside:
                            areas_visited.append(k)
                        sides = sides + sides_inside
                        run_done = 1
                        break
            if run_done == 1:
                break
        if i == areas[-1]:
            inside_done = 1


    
    return sides

def main():
    map, regions = load_data("input.csv")
    next_region = regions[0]

    while next_region is not None:
        areas = find_region_area(map, next_region)
        sides = determine_sides(areas)
        for i in areas:
            other_region = check_if_other_region(i, next_region, regions)
            if other_region != []:
                regions.remove(other_region)

        index_region = regions.index(next_region)
        regions[index_region].append(len(areas))
        regions[index_region].append(sides)
        next_region = determine_next_region(regions)

    print(calculate_price(regions))

main()