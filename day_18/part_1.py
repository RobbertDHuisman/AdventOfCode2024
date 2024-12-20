import csv
import re

def load_data(filename):
    if filename == "example.csv":
        size = 7
        start = [0, 0]
        end = [size - 1, size - 1]
        nr_bytes = 12
    else:
        size = 71
        start = [0, 0]
        end = [size - 1, size - 1]
        nr_bytes = 1024
    
    falling_bytes = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)

        for row in csv_file:
            falling_bytes.append([int(row[1]), int(row[0])])

    return size, start, end, nr_bytes, falling_bytes

def create_map(size_map, falling_bytes):
    map = []
    for i in range(0, size_map):
        row = ""
        bytes_in_row = []
        for j in falling_bytes:
            if j[0] == i:
                bytes_in_row.append(j[1])
        for k in range(0, size_map):
            if k in bytes_in_row:
                row = row + "#"
            else:
                row = row + "."

        map.append(row)
        
    return map

def check_position_inside_map(height_map, width_map, location):
    if location[0] >= 0 and location[0] < height_map and location[1] >= 0 and location[1] < width_map:
        return True
    else:
        return False


def find_possible_directions(map, location, current_direction):
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    if current_direction != []:
        previous_direction = [current_direction[0] * -1, current_direction[1] * -1]
    else:
        previous_direction = []

    if check_position_inside_map(len(map), len(map[0]), [location[0] - 1, location[1]]) is False:
        directions.remove([-1, 0])
    elif map[location[0] - 1][location[1]:location[1] + 1] != ".":
        directions.remove([-1, 0])
    if check_position_inside_map(len(map), len(map[0]), [location[0], location[1] + 1]) is False:
        directions.remove([0, 1])
    elif map[location[0]][location[1] + 1:location[1] + 2] != ".":
        directions.remove([0, 1])
    if check_position_inside_map(len(map), len(map[0]), [location[0] + 1, location[1]]) is False:
        directions.remove([1, 0])
    elif map[location[0] + 1][location[1]:location[1] + 1] != ".":
        directions.remove([1, 0])
    if check_position_inside_map(len(map), len(map[0]), [location[0], location[1] - 1]) is False:
        directions.remove([0, -1])
    elif map[location[0]][location[1] - 1: location[1]] != ".":
        directions.remove([0, -1])
    if previous_direction in directions:
        directions.remove(previous_direction)

    return directions

def find_all_intersections_with_directions(map, start, end):
    intersections = []
    for i in range(0, len(map)):
        points = re.finditer('\.', map[i])
        for j in points:
            directions = find_possible_directions(map, [i, j.start()], [])
            if [i, j.start()] in [start, end]:
                intersections.append([[i, j.start()], directions])
            if len(directions) > 2:
                intersections.append([[i, j.start()], directions])

    return intersections

def check_if_arrive_at_other_intersection(location, intersections):
    for i in intersections:
        if location == i[0]:
            return True
        
    return False

def get_all_subpaths(map, intersections):
    subpaths = []
    for i in intersections:
        for j in i[1]:
            # print(i, j)
            new_location = [i[0][0] + j[0], i[0][1] + j[1]] 
            new_direction = j
            score = 1
            at_next_intersection = 0
            while at_next_intersection == 0:
                location = new_location
                direction = new_direction
                if check_if_arrive_at_other_intersection(location, intersections):
                    subpaths.append([i[0], j, location, direction, score])
                    at_next_intersection = 1

                else:
                    directions = find_possible_directions(map, location, direction)
                    if len(directions) == 0:
                        at_next_intersection = -1
                    else:
                        new_direction = directions[0]
                        new_location = [location[0] + new_direction[0], location[1] + new_direction[1]] 
                        score += 1

    return subpaths

def remove_paths_too_high_score(paths, score):
    for i in range(len(paths) -1, -1, -1):
        if paths[i][2] >= score:
            paths.pop(i)

    return paths

def check_if_intersection_was_reached_with_lower_score(intersection, score, intersections):
    for i in intersections:
        if intersection == i[0] and score > i[1]:
            return True
        
    return False

def make_paths(subpaths, start, end):
    paths = []
    intersections = [[start, 0]]
    
    for i in subpaths:
        if i[0] == start:
            paths.append([[i[0], i[2]], i[3], i[4]])
                                
    end_reached = 0
    while end_reached == 0:
        current_path = paths[0].copy()
        current_location = paths[0][0][-1]
        current_score = paths[0][2]
        if len(paths) > 1:
            for j in range(1, len(paths)):
                if paths[j][2] < current_score:
                    current_path = paths[j].copy()
                    current_location = paths[j][0][-1]
                    current_score = paths[j][2]

        if current_location == end:
            end_reached = 1
            end_location = current_location
            score = current_score
            print(current_path)
        else:
            paths.remove(current_path)
            for k in subpaths:
                if k[0] == current_location:
                    new_path = []
                    if k[2] not in current_path[0]:
                        for m in current_path[0]:
                            new_path.append(m)
                        new_path.append(k[2])
                        new_location = k[2]
                        new_direction = k[3]
                        new_score = current_path[2] + k[4]
                        if check_if_intersection_was_reached_with_lower_score(new_location, new_score, intersections) is False:
                            paths.append([new_path, new_direction, new_score])
                            intersections.append([new_location, new_score])

        if new_location == end:
            paths = remove_paths_too_high_score(paths, new_score)

    return end_location, score

def calc_total_score(score_start, score_end, location_start, location_end):

    return score_start + score_end + abs(location_end[0] - location_start[0]) + abs(location_end[1] - location_start[1]) + 4 # + 4 is from sight

def main():
    size, start, end, nr_bytes, falling_bytes = load_data("input.csv")
    map = create_map(size, falling_bytes[0:nr_bytes])

    # If to do all by code: make code that check on the top and bottom row where the border starts and follow that border to see what the lowest and highest row
    # of that border are. that would then be the input for make_paths's last input.

    intersections = find_all_intersections_with_directions(map, start, end)
    subpaths = get_all_subpaths(map, intersections)
    end_location_start, score_start = make_paths(subpaths, start, [54, 7])
    end_location_end, score_end = make_paths(subpaths, end, [13, 62])
    total_score = calc_total_score(score_start, score_end, end_location_start, end_location_end)
    
    print(total_score)

main()