import csv

def load_data(filename):

    all_rows = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, delimiter=" ")

        locks = []
        keys = []

        lock = []
        key = []
        empty_row = 1

        for row in csv_file:
            if empty_row == 1:
                if row[0][0:1] == "#":
                    is_lock = 1
                    lock.append(row[0])
                else:
                    is_lock = 0
                    key.append(row[0])

                empty_row = 0
                
            else:
                if len(row) == 0:
                    if is_lock == 1:
                        locks.append(lock)
                        lock = []
                    else:
                        keys.append(key)
                        key = []

                    empty_row = 1

                else:
                    if is_lock == 1:
                        lock.append(row[0])
                    else:
                        key.append(row[0])

        if is_lock == 1:
            locks.append(lock)
        else:
            keys.append(key)


    return locks, keys

def get_lengths(scheme):
    lengths = []
    for i in range(0, len(scheme[0])):
        length = -1
        for j in scheme:
            if j[i:i+1] == "#":
                length += 1
        
        lengths.append(length)
    
    return lengths

def combination_fits(lengths_lock, lengths_key, total_length):
    for i in range(0, len(lengths_lock)):
        if lengths_lock[i] + lengths_key[i] > total_length:
            return False

    return True

def main():
    locks, keys = load_data("input.csv")
    length_lock = len(locks[0]) - 2
    lengths_locks = []
    lengths_keys = []

    for i in locks:
        lengths_locks.append(get_lengths(i))

    for j in keys:
        lengths_keys.append(get_lengths(j))

    unique_combinations = 0
    for k in lengths_locks:
        for m in lengths_keys:
            if combination_fits(k, m, length_lock):
                # print(k, m)
                unique_combinations += 1

    print(unique_combinations)

main()