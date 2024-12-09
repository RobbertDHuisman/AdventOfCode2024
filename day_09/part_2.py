from part_1 import load_data

def add_id_to_list(files):
    files_with_ids = []
    for i in range(0, len(files)):
        files_with_ids.append([files[i], i])
    
    return files_with_ids

def find_free_space(file_size, free_spaces, index_file):
    found = 0
    tried = 0
    while found == 0 and tried < index_file - 1:
        if file_size <= int(free_spaces[tried]):
            found = 1
            return tried
        else:
            tried += 1

def update_filesystem(filesystem, file, index_free_space):
    new_filesystem = filesystem.copy()
    new_filesystem.remove(file)
    new_filesystem.insert(index_free_space + 1, file)
    return new_filesystem

def update_free_spaces(free_spaces, index_free_space, index_file, file_size):
    new_free_spaces = free_spaces.copy()
    new_space = int(new_free_spaces[index_free_space]) - file_size
    if index_file < len(free_spaces):
        new_free_spaces[index_file-1] = int(free_spaces[index_file-1]) + file_size + int(free_spaces[index_file])
        new_free_spaces.pop(index_file)
    else:
        new_free_spaces[index_file-1] = int(free_spaces[index_file-1]) + file_size
    new_free_spaces[index_free_space] = 0
    new_free_spaces.insert(index_free_space + 1, new_space)

    return new_free_spaces


def calculate_checksum_with_ids(filesystem, free_spaces):
    checksum = 0
    step = 0
    print(len(filesystem), len(free_spaces))
    for i in range(0, len(filesystem)):
        for j in range(0, int(filesystem[i][0])):
            checksum += step * filesystem[i][1]
            step += 1

        for k in range(0, int(free_spaces[i])):
            step += 1

    return checksum    

def calc_total_length(filesystem, free_spaces):
    total_file = 0
    total_file_id = 0
    total_space = 0
    for i in filesystem:
        total_file += int(i[0])
        total_file_id += int(i[1])

    for j in free_spaces:
        total_space += int(j)
    return total_file, total_file_id, total_space

def main():
    files, free_spaces, string = load_data("input.csv")
    files_with_ids = add_id_to_list(files)
    new_filesystem = files_with_ids.copy()
    new_free_spaces = free_spaces.copy()
    files_moved = []
    files_not_moved = []

    # for i in range(len(files_with_ids) -1, 9990, -1):
    for i in range(len(files_with_ids) -1, 0, -1):
        # print(files_with_ids[i],  free_spaces[0:20])
        filesystem = []
        free_spaces = []
        filesystem = new_filesystem.copy()
        free_spaces = new_free_spaces.copy()
        file = files_with_ids[i]
        file_size = int(file[0])
        index_file = filesystem.index(file)
        index_free_space = find_free_space(file_size, free_spaces, index_file)
        # if file_size != int(free_spaces[index_free_space]):
        #     print(f"the file is {file} the file size is {file_size} and the free space is {free_spaces[index_free_space]}")
        if index_free_space is not None and index_free_space < index_file - 1:
            new_filesystem = update_filesystem(filesystem, file, index_free_space)
            new_free_spaces = update_free_spaces(free_spaces, index_free_space, index_file, file_size)
            files_moved.append(file)
        else:
            files_not_moved.append(file)
            # print(file)
    checksum = calculate_checksum_with_ids(new_filesystem, new_free_spaces)

    previous_free_space = []
    for i in files_moved:
        if new_free_spaces[new_filesystem.index(i) - 1] != 0:
            previous_free_space.append([i, new_free_spaces[new_filesystem.index(i) - 1]])

    print(previous_free_space)
    print(checksum)

main()