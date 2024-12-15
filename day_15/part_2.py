import csv

from part_1 import load_data_moves, find_starting_point, change_value_in_row, calc_gps

def load_data_map(filename):
    map = []
    with open(f"{filename}.map.csv", 'r') as file:
        csv_file = csv.reader(file)

        for row in csv_file:
            string = ""
            for i in range(0, len(row[0])):
                if row[0][i] == "#":
                    string = string + "##"
                elif row[0][i] == "O":
                    string = string + "[]"
                elif row[0][i] == ".":
                    string = string + ".."
                else:
                    string = string + "@."
            map.append(string)

    return map

def check_boxes_vertically(map, location):
    boxes = []
    stop = 0
    if map[location[0]][location[1]] == "#":
        boxes.append([-1, -1])
        stop = 1
    elif map[location[0]][location[1]] == ".":
        stop = 1
    elif map[location[0]][location[1]] =="[":
        boxes.append(location)
    elif map[location[0]][location[1]] =="]":
        boxes.append([location[0], location[1] - 1])

    return boxes, stop

def find_boxes_to_move(map, location, move):
    stop = 0
    boxes = []
    while stop == 0:
        if move[0] == 0:
            new_location = [location[0], location[1] + move[1]]
            if map[new_location[0]][new_location[1]] == "[":
                boxes.append(new_location)
                location = new_location
            if map[new_location[0]][new_location[1]] == "]":
                location = new_location
            elif map[new_location[0]][new_location[1]] == "#":
                boxes = [-1, -1]
                stop = 1
            elif map[new_location[0]][new_location[1]] == ".":
                stop = 1
        else:
            if boxes == []:
                new_location = [location[0] + move[0], location[1]]    
                new_boxes, stop = check_boxes_vertically(map, new_location)
                for i in new_boxes:
                    if i == [-1, -1]:
                        boxes = [-1, -1]
                    elif i not in boxes:
                        boxes.append(i)
            else:
                for j in boxes:
                    for k in range(2):
                        if boxes != [-1, -1]:
                            new_boxes, stop = check_boxes_vertically(map, [j[0] + move[0], j[1] + k])
                            for m in new_boxes:
                                if m == [-1, -1]:
                                    boxes = [-1, -1]
                                elif m not in boxes:
                                    boxes.append(m)

    return boxes

def move_without_boxes(map, location, move):
    new_location_robot = [location[0] + move[0], location[1] + move[1]]
    map = change_value_in_row(map, new_location_robot, "@")
    map = change_value_in_row(map, location, ".")

    return map

def move_horizontally(map, location, move, boxes):
    if move[1] == -1:
        new_row = map[location[0]][0:location[1] - (len(boxes)*2) - 1] + map[location[0]][location[1] - (len(boxes)*2):location[1] + 1] \
            + "." + map[location[0]][location[1] + 1: len(map[location[0]])]
    else:
        new_row = map[location[0]][0:location[1]] + "." + map[location[0]][location[1]: location[1] + (len(boxes)*2) + 1] \
            + map[location[0]][location[1] + (len(boxes)*2) + 2: len(map[location[0]])]
    map.pop(location[0])
    map.insert(location[0], new_row)

    return map

def move_vertically(map, location, move, boxes):
    for i in range(len(boxes) - 1, -1, -1):
        for j in range(2):
            map = change_value_in_row(map, [boxes[i][0] + move[0], boxes[i][1] + j], map[boxes[i][0]][boxes[i][1] + j])
            map = change_value_in_row(map, [boxes[i][0], boxes[i][1] + j], ".")

    map = change_value_in_row(map, [location[0] + move[0], location[1]], "@")
    map = change_value_in_row(map, location, ".")
    return map

def move(map, location, move, boxes):
    if boxes != []:
        if move[0] == 0:
            map = move_horizontally(map, location, move, boxes)
        else:
            map = move_vertically(map, location, move, boxes)

    else:
        map = move_without_boxes(map, location, move)
        
    new_location_robot = [location[0] + move[0], location[1] + move[1]]

    return map, new_location_robot

def find_boxes(map):
    boxes = []
    for i in range(0, len(map)):
        for j in range(0, len(map[0])):
            if map[i][j:j+1] == "[":
                boxes.append([i, j])
    
    return boxes

def main():
    file = "input"
    map = load_data_map(file)
    moves = load_data_moves(file)
    location = find_starting_point(map)

    for i in moves:
        boxes = find_boxes_to_move(map, location, i)
        if boxes != [-1, -1]:
            map, location = move(map, location, i, boxes)
    
    boxes = find_boxes(map)
    gps = calc_gps(boxes)
    print(sum(gps))

main()