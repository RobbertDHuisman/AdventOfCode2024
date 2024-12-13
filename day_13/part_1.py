import csv
import re
from sympy.solvers import solve
from sympy.abc import a, b

def load_data(filename):
    button_as = []
    button_bs = []
    prizes = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, delimiter=":")

        for row in csv_file:
            if row != []:
                numbers = re.findall('([0-9]{1,6})', row[1])
                for i in range(0, len(numbers)):
                    numbers[i] = int(numbers[i])
                if row[0] == "Button A":
                    button_as.append(numbers)
                if row[0] == "Button B":
                    button_bs.append(numbers)
                if row[0] == "Prize":
                    prizes.append(numbers)

    return button_as, button_bs, prizes

def calculate_result(button_a, button_b, prize):
    result = solve([a*button_a[0] + b*button_b[0] - prize[0], a*button_a[1] + b*button_b[1] - prize[1]], [a, b], dict=True)
    return result

def option_viable(result):
    if result[0][a] <= 100 and result[0][b] <= 100 and result[0][a] % 1 == 0 and result[0][b] % 1 == 0:
        return True
    else:
        return False

def calc_tokens_needed(result):
    return result[0][a] * 3 + result[0][b]

def main():
    button_as, button_bs, prizes = load_data("input.csv")
    tokens = 0
    for i in range(0, len(prizes)):
        result = calculate_result(button_as[i], button_bs[i], prizes[i])
        if option_viable(result):
            tokens += calc_tokens_needed(result)

    print(tokens)

main()