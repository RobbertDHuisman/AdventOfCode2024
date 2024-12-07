import csv
import re

def load_data(filename):
    results = []
    numbers = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, delimiter=":")

        for row in csv_file:
            results.append(int(row[0]))
            numbers.append(re.findall('[0-9]{1,4}', row[1]))

    return results, numbers

def test_calibration(result, numbers, operators):
    new_results = [int(numbers[0])]
    for i in range(1, len(numbers)):
        current_results = new_results.copy()
        new_results = []
        for j in operators:
            for k in current_results:
                if j == "+":
                    new_results.append(int(numbers[i]) + k)
                if j == "*":
                    new_results.append(int(numbers[i]) * k)
                if j == "||":
                    new_results.append(int(str(k) + numbers[i]))

    if result in new_results:
        return result
    else:
        return 0                         

def run_all(operators):
    results, numbers = load_data("input.csv")

    correct = 0
    for i in range(0, len(results)):
        print(f"we zijn nu bij rij {i}")
        test_results = test_calibration(results[i], numbers[i], operators)
        correct = correct + test_results

    print(correct)

def part_1():
    operators = ["+", "*"]
    run_all(operators)

def part_2():
    operators = ["+", "*", "||"]
    run_all(operators)

part_2()