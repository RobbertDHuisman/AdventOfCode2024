#%%

import csv
import re

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

def find_next_output(start_ids, start_values, inputs, types, outputs):
# def find_next_output(start_ids, start_values, inputs, types, outputs, formula):
    for i in range(0, len(inputs)):
        if inputs[i][0] in start_ids and inputs[i][1] in start_ids:
            index1 = start_ids.index(inputs[i][0])
            index2 = start_ids.index(inputs[i][1])
            start_ids.append(outputs[i])
            start_values.append(calc_outcome(start_values[index1], start_values[index2], types[i]))
            # formula.append([inputs[i], outputs[i]])
            inputs.pop(i)
            types.pop(i)
            outputs.pop(i)
            break

    # return start_ids, start_values, inputs, type, outputs, formula
    return start_ids, start_values, inputs, types, outputs

# def determine_all_outputs(start_ids, start_values, input_ids, type, output_ids, formula):
def determine_all_outputs(start_ids, start_values, input_ids, type, output_ids):
    # formula = []
    inputs = input_ids.copy()
    outputs = output_ids.copy()
    types = type.copy()

    while inputs != []:
        start_ids, start_values, inputs, types, outputs = find_next_output(start_ids, start_values, inputs, types, outputs)
        # start_ids, start_values, input_ids, type, output_ids, formula = find_next_output(start_ids, start_values, input_ids, type, output_ids, formula)

    return start_ids, start_values

def create_decimal_number(start_ids, start_values, character):
    number = []
    values = []
    output = ""
    for i in range(0, len(start_ids)):
        if start_ids[i][0:1] == character:
            number.append(start_ids[i][1:])
            values.append(start_values[i])

    # print(number, values)

    for j in range(len(number) -1, -1, -1):
        for k in range(0, len(number)):
            if int(number[k]) == j:
                output = output + str(values[k])

    # print(output)
    decimal = int(output, 2)
    
    return decimal, output

def main():
    start_ids, start_values, input_ids, type, output_ids = load_data("input.csv")

    original_start_ids, original_start_values = determine_all_outputs(start_ids, start_values, input_ids, type, output_ids)
    
    decimal_x, binary_x = create_decimal_number(original_start_ids, original_start_values, "x")
    decimal_y, binary_y = create_decimal_number(original_start_ids, original_start_values, "y")
    correct_decimal_z = decimal_x + decimal_y
    correct_binary_z = f'{correct_decimal_z:08b}'
    decimal_z, binary_z = create_decimal_number(original_start_ids, original_start_values, "z")

    # print(binary_z, correct_binary_z)

    wrong_index = []
    for i in range(len(binary_z) -1, -1, -1):
        if correct_binary_z[i:i+1] != binary_z[i:i+1]:
            wrong_index.append(f"z{len(binary_z) - 1 - i:02}")

    print(wrong_index)
    print(binary_z, correct_binary_z)
    to_check = []
    for j in wrong_index[0:1]:
        for k in range(0, len(output_ids)):
            if j == output_ids[k]:
                to_check.append(input_ids[k][0])
                to_check.append(input_ids[k][1])
                operatie = type[k]

    for m in to_check:
        for n in range(0, len(output_ids)):
            if m == output_ids[n]:
                if input_ids[n][0][0:1] not in ('x', 'y'):
                    for o in range(2):
                        to_check.append(input_ids[n][o])
                    for p in range(0, len(original_start_ids)):
                        if original_start_ids[p] == m:
                            print(f"{m} heeft als output {original_start_values[p]}, input is {input_ids[n]} en type is {type[n]}")

    print(to_check)

main()