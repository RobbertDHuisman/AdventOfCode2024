import csv

def load_data(filename):
    files = []
    free_spaces = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, quoting=csv.QUOTE_NONE)

        for row in csv_file:
            for i in range(0, len(row[0])):
                if i % 2 == 0:
                    files.append(row[0][i])
                else:
                    free_spaces.append(row[0][i])

    return files, free_spaces

def calc_length_files(files):
    total_length = 0
    for i in files:
        total_length += int(i)
    
    return total_length

def rearrange(files, free_spaces):
    filesystem = []
    number_of_ids = len(files)
    total_length_files = calc_length_files(files)
    rearrange_file = -1
    already_moved = 0
    length_subtotal = 0
    for i in range(0, len(files)):
        for j in range(0, int(files[i])):
            if length_subtotal < total_length_files:
                filesystem.append(int(i))
                length_subtotal += 1
        
        if i < len(free_spaces):
            for k in range(0, int(free_spaces[i])):
                if length_subtotal < total_length_files:
                    if already_moved < int(files[rearrange_file]):
                        filesystem.append(number_of_ids + rearrange_file)
                        already_moved += 1
                        length_subtotal += 1
                    else:
                        rearrange_file += -1
                        filesystem.append(number_of_ids + rearrange_file)
                        already_moved = 1
                        length_subtotal += 1

    return filesystem

def calculate_checksum(filesystem):
    checksum = 0
    for i in range(0, len(filesystem)):
        checksum += i * filesystem[i]

    return checksum

def main():
    files, free_spaces = load_data("input.csv")
    filesystem = rearrange(files, free_spaces)
    checksum = calculate_checksum(filesystem)
    print(checksum)

main()