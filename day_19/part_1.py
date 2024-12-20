import csv

def load_data(filename):       
    towels = []
    patterns = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)

        nr_rows = 0
        for row in csv_file:
            if nr_rows == 0:
                for i in row:
                    towels.append(i)
            elif nr_rows > 1:
                patterns.append(row[0])
            nr_rows += 1

    return towels, patterns

def check_pattern_possible(pattern, towels):
    possible_patterns = [""]
    current_pattern = possible_patterns[0]
    pattern_found = 0

    while pattern_found == 0 or possible_patterns == []:
        for i in towels:
            new_pattern = current_pattern + i
            if new_pattern == pattern[0:len(new_pattern) + 1]:
                possible_patterns.append(new_pattern)

        possible_patterns.remove(current_pattern)

        if pattern in possible_patterns:
            pattern_found = 1

        if possible_patterns != []:
            current_pattern = possible_patterns[0]

    if pattern_found == 1:
        return True
    else:
        return False

def main():
    towels, patterns = load_data("example.csv")
    print(towels, patterns)
    patterns_possible = []
    for i in patterns:
        if check_pattern_possible(i, towels):
            patterns_possible.append(i)
            print(f"this pattern in possible: {i}")
    
    print(len(patterns_possible))

main()