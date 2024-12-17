from part_1 import (
    load_data, 
    find_all_intersections_with_directions, 
    get_all_subpaths, 
    remove_paths_too_high_score)

def check_if_intersection_was_reached_with_lower_score(intersection, direction, score, intersections):
    for i in intersections:
        if intersection == i[0] and direction == i[1] and score > i[2]:
            return True
        
    return False

def make_paths(subpaths, start, end):
    paths = []
    intersections = [[start, 1000]]
    
    for i in subpaths:
        if i[0] == start:
            if i[1] != [0, 1]:
                paths.append([[i[0], i[2]], [i[3]], i[4] + 1000])
                                
    end_reached = 0
    while end_reached == 0:
        current_path = paths[0].copy()
        current_location = paths[0][0][-1]
        current_direction = paths[0][1][-1]
        current_score = paths[0][2]
        if len(paths) > 1:
            for j in range(1, len(paths)):
                if paths[j][2] < current_score:
                    current_path = paths[j].copy()
                    current_location = paths[j][0][-1]
                    current_direction = paths[j][1][-1]
                    current_score = paths[j][2]

        if current_location == end:
            end_reached = 1
            score = current_score
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
                        new_location = k[2]
                        if k[1] != current_direction:
                            new_score = current_path[2] + k[4] + 1000
                        else:
                            new_score = current_path[2] + k[4]
                        if check_if_intersection_was_reached_with_lower_score(new_location, new_direction[-1], new_score, intersections) is False:
                            paths.append([new_path, new_direction, new_score])
                            intersections.append([new_location, new_direction[-1], new_score])

        if new_location == end:
            paths = remove_paths_too_high_score(paths, new_score)

    return paths, score

def get_subpaths_from_path(path):
    subpaths = []
    for i in range(1, len(path[0])):
        subpaths.append([[path[0][i-1], path[0][i]], path[1][i-1]])
    
    return subpaths

def count_double_ends(ends):
    too_much = 0
    unique = []
    for k in ends:
        if k not in unique:
            unique.append(k)
        else:
            too_much += 1
            
    return too_much


def find_nr_good_seats(subpaths_in_paths, all_subpaths):
    ends = []
    nr_good_seats = 1
    for i in subpaths_in_paths:
        ends.append(i[0][1])
        seats = 0
        for j in all_subpaths:
            if i[0][0] == j[0] and i[0][1] == j[2] and i[1] == j[3]:
                seats = j[4]
        nr_good_seats += seats % 1000

    too_much = count_double_ends(ends)
    nr_good_seats -= too_much

    return nr_good_seats

def get_right_paths(paths, score, end):
    for i in range(len(paths) -1, -1, -1):
        if paths[i][2] != score or paths[i][0][-1] != end:
            paths.pop(i)

    return paths

def main():
    map, start, end = load_data("input.csv")
    intersections = find_all_intersections_with_directions(map)
    subpaths = get_all_subpaths(map, intersections)
    paths, score = make_paths(subpaths, start, end)

    paths = get_right_paths(paths, score, end)

    subpaths_in_paths = []
    for i in paths:
        subpaths_in_path = get_subpaths_from_path(i)
        for j in subpaths_in_path:
            if j not in subpaths_in_paths:
                subpaths_in_paths.append(j)

    nr_good_seats = find_nr_good_seats(subpaths_in_paths, subpaths)
    print(nr_good_seats)

main()