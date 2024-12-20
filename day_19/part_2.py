from part_1 import load_data

def choose_next_pattern(possible_patterns):
    next_pattern = possible_patterns[0]
    for i in possible_patterns:
        if len(i) < len(next_pattern):
            next_pattern = i
        
    return next_pattern

def check_pattern_possible(pattern, towels):
    possible_patterns = [""]
    nr_of_pattern = [1]
    current_pattern = possible_patterns[0]
    index = 0
    pattern_found = 0

    while pattern_found == 0 and possible_patterns != []:
        if current_pattern == pattern:
            pattern_found = 1
            break

        for i in towels:
            new_pattern = (current_pattern.strip() + i.strip()).strip()
            if new_pattern == pattern[0:len(new_pattern)]:
                if new_pattern not in possible_patterns:
                    possible_patterns.append(new_pattern)
                    nr_of_pattern.append(nr_of_pattern[index])
                else:
                    for j in range(0, len(possible_patterns)):
                        if new_pattern == possible_patterns[j]:
                            nr_of_pattern[j] += nr_of_pattern[index]

        possible_patterns.pop(index)
        nr_of_pattern.pop(index)

        if possible_patterns != []:
            current_pattern = choose_next_pattern(possible_patterns)
            index = possible_patterns.index(current_pattern)

    if pattern_found == 1:
        return nr_of_pattern[0]
    else:
        return 0

def main():
    towels, patterns = load_data("input.csv")
    patterns_possible = []
    for i in patterns:
        nr_patterns = check_pattern_possible(i, towels)
        patterns_possible.append(nr_patterns)
    
    print(patterns_possible, sum(patterns_possible))

main()