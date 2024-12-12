import csv

def load_data(filename):
    map = []
    regions = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)

        nr_rows = 0
        for row in csv_file:
            map.append(row[0])
            regions.append([row[0][0], nr_rows, 0])
            for i in range(1, len(row[0])):
                if row[0][i] != row[0][i-1]:
                    regions.append([row[0][i], nr_rows, i])
            nr_rows += 1

    return map, regions

def find_perimeter(map, location, region_sign):
    perimeter = 0
    if location[0] == 0:
        perimeter += 1   
    elif map[location[0] - 1][location[1]] != region_sign:
        perimeter += 1

    if location[0] == len(map) - 1:
        perimeter += 1
    elif map[location[0] + 1][location[1]] != region_sign:
        perimeter += 1

    if location[1] == 0:
        perimeter += 1
    elif map[location[0]][location[1] - 1] != region_sign:
        perimeter += 1

    if location[1] == len(map[location[0]]) - 1:
        perimeter += 1
    elif map[location[0]][location[1] + 1] != region_sign:
        perimeter += 1
    
    return perimeter

def find_adjacent_locations(location):
    return [[location[0] - 1, location[1]],
        [location[0], location[1] + 1],
        [location[0] + 1, location[1]],
        [location[0], location[1] - 1]
        ]

def check_position_inside_map(height_map, width_map, location):
    if location[0] >= 0 and location[0] < height_map and location[1] >= 0 and location[1] < width_map:
        return True
    else:
        return False

def check_if_other_region(location, region, regions):
    other_region = []
    for j in range(0, len(regions)):
        if location[0] == regions[j][1] and location[1] == regions[j][2] and regions[j] != region:
            other_region = regions[j]
            break

    return other_region

def get_unique_list(list):
    unique_list = []
    for i in list:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list

def find_region_area(map, region):
    height_map = len(map)
    width_map = len(map[0])
    new_areas = [[region[1], region[2]]]
    all_areas = new_areas
    while new_areas != []:
        areas = new_areas.copy()
        new_areas = []
        for i in areas:
            adjacent_locations = find_adjacent_locations(i)
            for j in adjacent_locations:
                if check_position_inside_map(height_map, width_map, j) and map[j[0]][j[1]] == region[0] and j not in all_areas:
                    new_areas.append(j)

        new_areas = get_unique_list(new_areas)
        for k in new_areas:
            all_areas.append(k)  
    
    return all_areas


def determine_next_region(regions):
    for i in regions:
        if len(i) == 3:
            next_region = i
            break
        else:
            next_region = None
    
    
    return next_region

def calculate_price(regions):
    price = 0
    for i in regions:
        price += i[3] * i[4]

    return price

def main():
    map, regions = load_data("input.csv")
    next_region = regions[0]

    while next_region is not None:
        areas = find_region_area(map, next_region)
        perimeter = 0
        for i in areas:
            perimeter += find_perimeter(map, i, next_region[0])
            other_region = check_if_other_region(i, next_region, regions)
            if other_region != []:
                regions.remove(other_region)

        index_region = regions.index(next_region)
        regions[index_region].append(len(areas))
        regions[index_region].append(perimeter)
        next_region = determine_next_region(regions)

    print(calculate_price(regions))

main()