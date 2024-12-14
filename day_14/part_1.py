import csv
import re
import math

def load_data(filename):
    start = []
    velocity = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, delimiter=" ")

        for row in csv_file:
            find_location = re.search('(.*=)(.*)(,)(.*)', row[0])
            start.append([int(find_location.group(2)), int(find_location.group(4))])
            find_velocity = re.search('(.*=)(.*)(,)(.*)', row[1])
            velocity.append([int(find_velocity.group(2)), int(find_velocity.group(4))])

    return start, velocity

def find_location_after_seconds(start, velocity, height, width, seconds):
    final_location = []
    for i in range(0, len(start)):
        final_x = (start[i][0] + seconds * velocity[i][0]) % width
        final_y = (start[i][1] + seconds * velocity[i][1]) % height
        final_location.append([final_x, final_y])
    return final_location

def count_quadrants(locations, height, width):
    counts = [0, 0, 0, 0]
    print(math.floor(width/2), math.floor(height/2))
    for i in locations:
        if i[0] < math.floor(width/2):
            if i[1] < math.floor(height/2):
                counts[0] += 1
            elif i[1] > math.floor(height/2):
                counts[1] += 1
        elif i[0] > math.floor(width/2):
            if i[1] < math.floor(height/2):
                counts[2] += 1
            elif i[1] > math.floor(height/2):
                counts[3] += 1      

    return counts 

def main():
    file = "input"
    if file in "example":
        height = 7
        width = 11
    else:
        height = 103
        width = 101

    start, velocity = load_data(f"{file}.csv")
    final_locations = find_location_after_seconds(start, velocity, height, width, 100)
    counts = count_quadrants(final_locations, height, width)
    print(math.prod(counts))

main()