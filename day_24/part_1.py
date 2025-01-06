import csv

def load_data(filename):
    start_ids = []
    start_values = []
    input_ids = []
    type = []
    output_ids = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, delimiter=" ")

        for row in csv_file:
            if len(row) == 2:
                start_ids.append(row[0][0:-1])
                start_values.append(int(row[1]))
            elif len(row) == 5:
                input_ids.append([row[0], row[2]])
                output_ids.append(row[4])
                type.append(row[1])

    return start_ids, start_values, input_ids, type, output_ids

def calc_outcome(input1, input2, type):
    if (type == "AND" and input1 == 1 and input2 == 1) or \
        (type == "OR" and not (input1 == 0 and input2 == 0)) or \
        (type == "XOR" and input1 != input2):
        output = 1
    else:
        output = 0
    
    return output

def find_next_output(start_ids, start_values, input_ids, type, output_ids):
    for i in range(0, len(input_ids)):
        if input_ids[i][0] in start_ids and input_ids[i][1] in start_ids:
            index1 = start_ids.index(input_ids[i][0])
            index2 = start_ids.index(input_ids[i][1])
            start_ids.append(output_ids[i])
            start_values.append(calc_outcome(start_values[index1], start_values[index2], type[i]))
            input_ids.pop(i)
            type.pop(i)
            output_ids.pop(i)
            break

    return start_ids, start_values, input_ids, type, output_ids

def create_decimal_number(start_ids, start_values):
    number = []
    values = []
    output = ""
    for i in range(0, len(start_ids)):
        if start_ids[i][0:1] == "z":
            number.append(start_ids[i][1:])
            values.append(start_values[i])

    for j in range(len(number) -1, -1, -1):
        for k in range(0, len(number)):
            if int(number[k]) == j:
                output = output + str(values[k])

    decimal = int(output, 2)
    
    return decimal


def main():
    start_ids, start_values, input_ids, type, output_ids = load_data("input.csv")

    while input_ids != []:
        start_ids, start_values, input_ids, type, output_ids = find_next_output(start_ids, start_values, input_ids, type, output_ids)
 
    decimal = create_decimal_number(start_ids, start_values)
    print(decimal)

main()