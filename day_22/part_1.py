import csv
import math

def load_data(filename):
    secret_numbers = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)

        for row in csv_file:
            secret_numbers.append(int(row[0]))

    return secret_numbers

def mix(secret_number, new_value):
    return secret_number ^ new_value

def prune(number):
    return number % 16777216

def define_next_secret_number(input_secret_number):
    step_1 = prune(mix(input_secret_number, input_secret_number * 64))
    step_2 = prune(mix(step_1, math.floor(step_1 / 32)))
    step_3 = prune(mix(step_2, step_2 * 2048))

    return step_3

def main():
    input_secret_numbers = load_data("input.csv")
    output_secret_numbers = []
    for i in input_secret_numbers:
        secret_number = i
        for j in range(2000):
            secret_number = define_next_secret_number(secret_number)
        output_secret_numbers.append(secret_number)

    print(sum(output_secret_numbers))

main()