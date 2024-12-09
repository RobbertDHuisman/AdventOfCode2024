from part_1 import load_data

def add_id_to_list(files):
    files_with_ids = []
    for i in range(0, len(files)):
        files_with_ids.append([files[i], i])
    
    return files_with_ids

def rearrange(files, free_spaces):
    filesystem = []
    files_moved = []
    for i in range(0, len(files)):
        print(i)
        for j in range(0, int(files[i][0])):
            if files[i] not in files_moved:
                filesystem.append(int(files[i][1]))
            else:
                filesystem.append(".")
        
        if i < len(free_spaces):
            free_space_left = int(free_spaces[i])
            found = 1
            while free_space_left > 0 and found == 1:
                found = 0
                for k in range(len(files) - 1, i, -1):
                    if files[k] not in files_moved and found == 0:
                        if int(files[k][0]) <= free_space_left:
                            for m in range(0, int(files[k][0])):
                                filesystem.append(int(files[k][1]))
                            free_space_left -= int(files[k][0])
                            files_moved.append(files[k])
                            found = 1
            
            if free_space_left > 0:
                for n in range(0, free_space_left):
                    filesystem.append(".")
                
    return filesystem

def calculate_checksum(filesystem):
    checksum = 0
    for i in range(0, len(filesystem)):
        if filesystem[i] != ".":
            checksum += i * filesystem[i]

    return checksum

def main():
    files, free_spaces = load_data("input.csv")
    files_with_id = add_id_to_list(files)
    filesystem = rearrange(files_with_id, free_spaces)
    checksum = calculate_checksum(filesystem)
    print(checksum)

main()