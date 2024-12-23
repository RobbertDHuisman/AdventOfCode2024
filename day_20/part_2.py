import re
from tqdm import tqdm

from part_1 import (
    load_data, 
    find_possible_directions, 
)

def find_all_points_on_racetrack(map):
    track = []
    for i in range(0, len(map)):
        points = re.finditer("\.|S|E", map[i])
        for j in points:
            track.append([i, j.start()])

    return track

def find_all_shortcuts(track):
    shortcuts = []
    for i in range(0, len(track) - 1):
        for j in range(i+1, len(track)):
            if abs(track[i][0] - track[j][0]) + abs(track[i][1] - track[j][1]) <= 20 and \
                abs(track[i][0] - track[j][0]) + abs(track[i][1] - track[j][1]) > 1:

                if track[i][0] == track[j][0]:
                    one_line = 1
                    for k in range(track[i][1], track[j][1]):
                        point_on_line_found = 0
                        for m in range(i, j):
                            if track[m] == [track[i][0], k]:
                                point_on_line_found = 1
                        if point_on_line_found == 0:
                            one_line = 0
                            break

                elif track[i][1] == track[j][1]:
                    one_line = 1
                    for k in range(track[i][0], track[j][0]):
                        point_on_line_found = 0
                        for m in range(i, j):
                            if track[m] == [k, track[i][1]]:
                                point_on_line_found = 1
                        if point_on_line_found == 0:
                            one_line = 0
                            break

                else:
                    one_line = 0

                if one_line != 1:
                    shortcuts.append([track[i], track[j]])

    return shortcuts

def get_path(map, intersections):
    path = [[intersections[0], 0]]
    new_location = intersections[0]
    new_direction = find_possible_directions(map, new_location, [])[0]
    score = 0
    at_next_intersection = 0
    while at_next_intersection == 0:
        location = new_location
        direction = new_direction
        if location == intersections[1]:
            at_next_intersection = 1
            break

        else:
            directions = find_possible_directions(map, location, direction)
            new_direction = directions[0]
            new_location = [location[0] + new_direction[0], location[1] + new_direction[1]] 
            score += 1
            path.append([new_location, score])

    return path

def find_time_saved(path, shortcut):
    shortcut_time = abs(shortcut[0][0] - shortcut[1][0]) + abs(shortcut[0][1] - shortcut[1][1])
    for i in path:
        if i[0] == shortcut[0]:
            normal_start = i[1]
        elif i[0] == shortcut[1]:
            normal_end = i[1]

    normal_time = abs(normal_end - normal_start)
    
    return normal_time - shortcut_time

def main():
    map, start, end = load_data("input.csv")
    time_saved = []

    track = find_all_points_on_racetrack(map)
    shortcuts = find_all_shortcuts(track)
    path = get_path(map, [start, end])

    with tqdm(total=len(shortcuts)) as pbar:
    
        for i in shortcuts:
            pbar.update(1)

            time = find_time_saved(path, i)
            if time >= 100:
                time_saved.append(time)

    print(len(time_saved))

main()