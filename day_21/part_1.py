import csv

def load_data(filename):
    code = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)

        for row in csv_file:
            code.append(row[0])

    return code

def make_numerical_keypad():
    return [
        ["7", [0,0]],
        ["8", [0,1]],
        ["9", [0,2]],
        ["4", [1,0]],
        ["5", [1,1]],
        ["6", [1,2]],
        ["1", [2,0]],
        ["2", [2,1]],
        ["3", [2,2]],
        ["0", [3,1]],
        ["A", [3,2]]
    ]

def numerical_options():
    return [
        [['0', '2'], ["^A"]], 
        [['2', '9'], ["^^>A", "^>^A", ">^^A"]], 
        [['9', 'A'], ["vvvA"]], 
        [['9', '8'], ["<A"]], 
        [['8', '0'], ["vvvA"]], 
        [['0', 'A'], [">A"]], 
        [['1', '7'], ["^^A"]], 
        [['7', '9'], [">>A"]], 
        [['4', '5'], [">A"]], 
        [['5', '6'], [">A"]], 
        [['6', 'A'], ["vvA"]], 
        [['3', '7'], ["<<^^A", "<^<^A", "^<^<A", "^^<<A"]],
        [['3', '4'], ["<<^A", "<^<A", "^<<A"]], 
        [['4', '0'], [">vvA", "v>vA"]], 
        [['1', '4'], ["^A"]], 
        [['4', '9'], ["^>>A", ">^>A", ">>^A"]], 
        [['5', '8'], ["^A"]], 
        [['8', '2'], ["vvA"]], 
        [['2', 'A'], [">vA", "v>A"]], 
        [['7', '8'], [">A"]], 
        [['4', '6'], [">>A"]], 
        [['6', '3'], ["vA"]], 
        [['3', 'A'], ["vA"]],
        [['A', '0'], ["<A"]],
        [['A', '1'], ["<^<A", "^<<A"]],
        [['A', '3'], ["^A"]],
        [['A', '4'], ["<^<^A", "<^^<A", "^<<^A", "^<^<A", "^^<<A"]],
        [['A', '5'], ["<^^A", "^^<A", "^<^A"]],
        [['A', '7'], ["<^<^^A", "<^^<^A", "<^^^<A", "^<<^^A", "^<^<^A", "^<^^<A", "^^<<^A", "^^<^<A", "^^^<<A"]],
        [['A', '9'], ["^^^A"]]
    ]
 
def make_directional_keypad():
    return [
        ["^", [0,1]],
        ["A", [0,2]],
        ["<", [1,0]],
        ["v", [1,1]],
        [">", [1,2]]
    ]

def directional_options():
    return [
        [['^', 'A'], [">A"]], 
        [['^', '<'], ["v<A"]], 
        [['^', 'v'], ["vA"]], 
        [['^', '>'], ["v>A", ">vA"]], 
        [['^', '^'], ["A"]],
        [['A', '^'], ["<A"]], 
        [['A', '<'], ["<v<A", "v<<A"]], 
        [['A', 'v'], ["<vA", "v<A"]], 
        [['A', '>'], ["vA"]], 
        [['A', 'A'], ["A"]],
        [['<', '^'], [">^A"]], 
        [['<', 'A'], [">>^A", ">^>A"]], 
        [['<', 'v'], [">A"]], 
        [['<', '>'], [">>A"]], 
        [['<', '<'], ["A"]],
        [['v', '^'], ["^A"]], 
        [['v', 'A'], ["^>A", ">^A"]], 
        [['v', '<'], ["<A"]], 
        [['v', '>'], [">A"]], 
        [['v', 'v'], ["A"]],
        [['>', '^'], ["<^A", "^<A"]], 
        [['>', 'A'], ["^A"]], 
        [['>', '<'], ["<<A"]], 
        [['>', 'v'], ["<A"]],
        [['>', '>'], ["A"]]
    ]

def turn_codes_into_locations(codes, keypad):
    locations = []
    for i in codes:
        for j in range(0, len(i)):
            for k in keypad:
                if i[j:j+1] == k[0]:
                    locations.append(k[1])

    return locations

def find_shortest_sequences(sequences):
    short_sequences = []
    length = len(sequences[0])
    for i in sequences:
        if len(i) < length:
            length = len(i)

    for j in sequences:
        if len(j) == length:
            short_sequences.append(j)
        
    return short_sequences

def find_new_sequences(string, options):
    sequences = [""]

    for i in range(1, len(string)):
        for j in range(len(sequences) - 1, -1, -1):
            for k in options:
                if string[i-1] == k[0][0] and string[i] == k[0][1]:
                    for m in k[1]:
                        sequences.append(sequences[j] + m)
            sequences.remove(sequences[j])

    short_sequences = find_shortest_sequences(sequences)

    return short_sequences

def find_similar_parts(sequences):
    similar_ranges = []
    different_ranges = []
    for i in range(0, len(sequences[0])):
        symbol = sequences[0][i]
        different = 0
        for j in sequences:
            if symbol != j[i]:
                different = 1
        if different == 1:
            different_ranges.append(i)
        else:
            similar_ranges.append(i)

def main():
    codes = load_data("input.csv")
    numerical_option = numerical_options()
    directional_option = directional_options()
    complexity = []

    for i in codes:
        i = "A" + i
        lengths_first = []
        for j in range(0, len(i) - 1):
            first_sequence = find_new_sequences(i[j:j+2], numerical_option)
            sum_lengths_first = []

            for k in first_sequence:
                k = "A" + k
                lengths_second = []                
                for m in range(0, len(k) - 1):
                    second_sequence = find_new_sequences(k[m:m+2], directional_option)
                    sum_lengths_final = []

                    for n in second_sequence:
                        n = "A" + n
                        lengths_final = []
                        for o in range(0, len(n) - 1):
                            final_sequence = find_new_sequences(n[o:o+2], directional_option)

                            length = len(final_sequence[0])
                            for p in final_sequence:
                                if len(p) < length:
                                    length = len(p)
                            lengths_final.append(length)

                        sum_lengths_final.append(sum(lengths_final))
                        # print(sum_lengths_final)
                    lengths_second.append(min(sum_lengths_final))
                    # print(lengths_second)
                sum_lengths_first.append(sum(lengths_second))
            lengths_first.append(min(sum_lengths_first))
            # print(lengths_first)
        complexity.append(sum(lengths_first) * int(i[1:-1]))

    print(sum(complexity))

main()