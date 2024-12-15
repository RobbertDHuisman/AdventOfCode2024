import csv

def load_data_map(filename):
    map = []
    with open(f"{filename}.map.csv", 'r') as file:
        csv_file = csv.reader(file)

        for row in csv_file:
            map.append(row[0])

    return map

def load_data_moves(filename):
    moves = []
    with open(f"{filename}.moves.csv", 'r') as file:
        csv_file = csv.reader(file)

        for row in csv_file:
            for i in row[0]:
                if i == "<":
                    moves.append([0, -1])
                if i == ">":
                    moves.append([0, 1])
                if i == "^":
                    moves.append([-1, 0])
                if i == "v":
                    moves.append([1, 0])

    return moves

def find_starting_point(map):
    for i in range(0, len(map)):
        for j in range(0, len(map[0])):
            if map[i][j] == "@":
                return [i, j]

def find_boxes_to_move(map, location, move):
    stop = 0
    boxes = 0
    while stop == 0:
        new_location = [location[0] + move[0], location[1] + move[1]]
        if map[new_location[0]][new_location[1]] == "O":
            boxes += 1
        if map[new_location[0]][new_location[1]] == "#":
            boxes = -1
            stop = 1
        if map[new_location[0]][new_location[1]] == ".":
            stop = 1

        location = new_location
    
    return boxes

def change_value_in_row(map, location, new_value):
    new_row = map[location[0]][0:location[1]] + new_value + map[location[0]][location[1] + 1:len(map[location[0]])]
    map.pop(location[0])
    map.insert(location[0], new_row)

    return map

def move(map, location, move, boxes):
    if boxes > 0:
        new_location_last_box = [location[0] + (boxes + 1) * move[0], location[1] + (boxes + 1) * move[1]]
        map = change_value_in_row(map, new_location_last_box, "O")

    new_location_robot = [location[0] + move[0], location[1] + move[1]]
    map = change_value_in_row(map, new_location_robot, "@")
    map = change_value_in_row(map, location, ".")

    return map, new_location_robot

def find_boxes(map):
    boxes = []
    for i in range(0, len(map)):
        for j in range(0, len(map[0])):
            if map[i][j] == "O":
                boxes.append([i, j])
    
    return boxes

def calc_gps(locations):
    gps = []
    for i in locations:
        gps.append(100 * i[0] + i[1])

    return gps

def main():
    file = "input"
    map = load_data_map(file)
    moves = load_data_moves(file)
    location = find_starting_point(map)

    for i in moves:
        boxes = find_boxes_to_move(map, location, i)
        if boxes != -1:
            map, location = move(map, location, i, boxes)
    
    boxes = find_boxes(map)
    gps = calc_gps(boxes)
    print(sum(gps))

main()