from sympy.abc import a, b

from part_1 import load_data, calculate_result, calc_tokens_needed

def change_prizes(prizes):
    for i in prizes:
        for j in range(0, len(i)):
            i[j] = i[j] + 10000000000000
    
    return prizes

def option_viable(result):
    if result[0][a] % 1 == 0 and result[0][b] % 1 == 0:
        return True
    else:
        return False

def main():
    button_as, button_bs, prizes = load_data("input.csv")
    prizes = change_prizes(prizes)
    tokens = 0
    for i in range(0, len(prizes)):
        result = calculate_result(button_as[i], button_bs[i], prizes[i])
        if option_viable(result):
            tokens += calc_tokens_needed(result)

    print(tokens)

main()