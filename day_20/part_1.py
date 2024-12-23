import csv
import re
from tqdm import tqdm

def load_data(filename):
    map = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)
        for row in csv_file:
            map.append(row[0])

    return map

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
                        score += 1

    return subpaths

def remove_paths_too_high_score(paths, score):
    for i in range(0, len(paths)):
        if paths[i][2] > score:
            paths.remove(i)

    return paths

def check_if_intersection_was_reached_with_lower_score(intersection, direction, score, intersections):
    for i in intersections:
        if intersection == i[0] and direction == i[1] and score > i[2]:
            return True
        
    return False

def make_paths(subpaths, start, end):
    paths = []
    
    for i in subpaths:
        if i[0] == start:
            paths.append([[i[0], i[2]], [i[3]], i[4]])
    
    if paths[0][1] != end:

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
            else:
                paths.remove(current_path)
                for k in subpaths:
                    if k[0] == current_location:
                        new_path = []
                        new_direction = []
                        if k[2] not in current_path[0]:
                            for m in current_path[0]:
                                new_path.append(m)
                            new_path.append(k[2])
                            for n in current_path[1]:
                                new_direction.append(n)
                            new_direction.append(k[3])
                            new_score = current_path[2] + k[4]
                            paths.append([new_path, new_direction, new_score])

    return paths

def get_right_paths(paths, end):
    for i in range(len(paths) -1, -1, -1):
        if paths[i][0][-1] != end:
            paths.pop(i)

    return paths

def find_possible_shortcuts(map):
    possible_shortcuts = []
    for i in range(1, len(map) - 1):
        for j in range(1, len(map[0]) - 4):
            if (map[i][j] in (".", "S", "E") and map[i][j+1] == "#" and map[i][j+2] == "#" and map[i][j+3] in (".", "S", "E")) or \
                (map[i][j] in (".", "S", "E") and map[i][j+1] == "#" and map[i][j+2] in (".", "S", "E")):
                possible_shortcuts.append([[i, j], [i, j+1], [i, j + 2]]) 

        if i < len(map) - 4:
            for k in range(1, len(map[0]) - 1):
                if (map[i][k] in (".", "S", "E") and map[i+1][k] == "#" and map[i+2][k] == "#" and map[i+3][k] in (".", "S", "E")) or \
                    (map[i][k] in (".", "S", "E") and map[i+1][k] == "#" and map[i+2][k] in (".", "S", "E")):
                    possible_shortcuts.append([[i, k], [i+1, k], [i+2, k]])

    return possible_shortcuts

def change_value_in_row(row, location, new_value):
    if row[location[1]] not in ("S", "E"):
        return row[0:location[1]] + new_value + row[location[1] + 1:len(row)]
    else:
        return row

def change_map(map, shortcut):
    new_map = []

    if shortcut[0][0] == shortcut[1][0]:
        new_row = map[shortcut[0][0]]

        for i in shortcut:
            new_row = change_value_in_row(new_row, i, ".")

        for j in range(0, len(map)):
            if j == shortcut[0][0]:
                new_map.append(new_row)
            else:
                new_map.append(map[j])

    else:
        rows_to_change = []
        new_rows = []
        for k in shortcut:
            rows_to_change.append(k[0])
            new_rows.append(change_value_in_row(map[k[0]], k, "."))

        for m in range(0, len(map)):
            if m in rows_to_change:
                new_map.append(new_rows[0])
                new_rows.pop(0)
                rows_to_change.pop(0)
            else:
                new_map.append(map[m])

    return new_map

def find_time_saved(paths):
    min = paths[0][2]
    max = paths[0][2]
    for i in paths:
        if i[2] > max:
            max = i[2]
        if i[2] < min:
            min = i[2]

    return max - min

def main():
    map = load_data("input.csv")
    intersections = find_all_intersections_with_directions(map)
    subpaths = get_all_subpaths(map, intersections)
    time_saved = []

    shortcuts = find_possible_shortcuts(map)
    
    with tqdm(total=6721) as pbar:
    
        for i in shortcuts:
            pbar.update(1)
            new_map = change_map(map, i)

            intersections = find_all_intersections_with_directions(new_map)
            subpaths = get_all_subpaths(map, intersections)
        
            paths = make_paths(subpaths, i[0], i[-1])
            paths = get_right_paths(paths, i[-1])
            
            time_saved.append(find_time_saved(paths))

    count = 0
    for j in time_saved:
        if j >= 100:
            count += 1
    print(count)

main()
