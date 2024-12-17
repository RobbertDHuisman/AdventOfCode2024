import csv
import re

def load_data(filename):
    map = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)
        nr_rows = 0

        for row in csv_file:
            map.append(row[0])
            if re.search('S', row[0]) is not None:
                start = [nr_rows, re.search('S', row[0]).start()]
            if re.search('E', row[0]) is not None:
                end = [nr_rows, re.search('E', row[0]).start()]

            nr_rows += 1

    return map, start, end

def find_possible_directions(map, location, current_direction):
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    if current_direction != []:
        previous_direction = [current_direction[0] * -1, current_direction[1] * -1]
    else:
        previous_direction = []
    
    if map[location[0] - 1][location[1]:location[1] + 1] not in (".", "E", "S"):
        directions.remove([-1, 0])
    if map[location[0]][location[1] + 1:location[1] + 2] not in (".", "E", "S"):
        directions.remove([0, 1])
    if map[location[0] + 1][location[1]:location[1] + 1] not in (".", "E", "S"):
        directions.remove([1, 0])
    if map[location[0]][location[1] - 1: location[1]] not in (".", "E", "S"):
        directions.remove([0, -1])
    if previous_direction in directions:
        directions.remove(previous_direction)

    return directions

def find_all_intersections_with_directions(map):
    intersections = []
    for i in range(1, len(map) - 1):
        points = re.finditer('\.', map[i])
        for j in points:
            directions = find_possible_directions(map, [i, j.start()], [])
            if len(directions) > 2:
                intersections.append([[i, j.start()], directions])
        if re.search('S', map[i]) is not None: 
            intersections.append([[i, re.search('S', map[i]).start()], find_possible_directions(map, [i, re.search('S', map[i]).start()], [])])
        if re.search('E', map[i]) is not None: 
            intersections.append([[i, re.search('E', map[i]).start()], find_possible_directions(map, [i, re.search('E', map[i]).start()], [])])

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
                        if new_direction == direction:
                            score += 1
                        else:
                            score += 1001                 

    return subpaths

def remove_paths_too_high_score(paths, score):
    for i in range(0, len(paths)):
        if paths[i][2] > score:
            paths.remove(i)

    return paths

def check_if_intersection_was_reached_with_lower_score(intersection, score, intersections):
    for i in intersections:
        if intersection == i[0] and score > i[1]:
            return True
        
    return False

def make_paths(subpaths, start, end):
    paths = []
    intersections = [[start, 1000]]
    
    for i in subpaths:
        if i[0] == start:
            if i[1] != [0, 1]:
                paths.append([[i[0], i[2]], i[3], i[4] + 1000])
                                
    end_reached = 0
    while end_reached == 0:
        current_path = paths[0].copy()
        current_location = paths[0][0][-1]
        current_direction = paths[0][1]
        current_score = paths[0][2]
        if len(paths) > 1:
            for j in range(1, len(paths)):
                if paths[j][2] < current_score:
                    current_path = paths[j].copy()
                    current_location = paths[j][0][-1]
                    current_direction = paths[j][1]
                    current_score = paths[j][2]

        if current_location == end:
            end_reached = 1
            score = current_score
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
                        if k[1] != current_direction:
                            new_score = current_path[2] + k[4] + 1000
                        else:
                            new_score = current_path[2] + k[4]
                        if check_if_intersection_was_reached_with_lower_score(new_location, new_score, intersections) is False:
                            paths.append([new_path, new_direction, new_score])
                            intersections.append([new_location, new_score])

        if new_location == end:
            paths = remove_paths_too_high_score(paths, new_score)

    return score

def main():
    map, start, end = load_data("input.csv")
    intersections = find_all_intersections_with_directions(map)
    subpaths = get_all_subpaths(map, intersections)
    score = make_paths(subpaths, start, end)
    print(score)

main()