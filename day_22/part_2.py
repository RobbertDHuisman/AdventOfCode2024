from tqdm import tqdm
from part_1 import load_data, define_next_secret_number

def get_all_numbers_and_changes(input_secret_numbers):
    all_prizes = []
    all_changes = []
    for i in input_secret_numbers:
        numbers = [i % 10]
        changes = []
        secret_number = i
        for j in range(2000):
            new_secret_number = define_next_secret_number(secret_number)
            numbers.append(new_secret_number % 10)
            changes.append(new_secret_number % 10 - secret_number % 10)
            secret_number = new_secret_number
        all_prizes.append(numbers)
        all_changes.append(changes)

    return all_prizes, all_changes

def main():
    input_secret_numbers = load_data("input.csv")
    best_prize = 0
    
    all_prizes, all_changes = get_all_numbers_and_changes(input_secret_numbers)
        
    with tqdm(total=12697) as pbar:
        for k in range(-5, 5):
            for m in range(max(-9 - k, -5), min(10 - k, 5)):
                for n in range(max(-9 - k - m, -5), min(10 - k - m, 10)):
                    for o in range(max(-9 - k - m, -2), min(10 - k - m - n, 10)):
                        pbar.update(1)
                        prizes_in_range = 0
                        for p in range(0, len(all_changes)):
                            for q in range(0, len(all_changes[p]) - 3):

                                if all_changes[p][q] == k and all_changes[p][q+1] == m and all_changes[p][q+2] == n and all_changes[p][q+3] == o:
                                    prizes_in_range += all_prizes[p][q+4]
                                    break

                        if prizes_in_range > best_prize:
                            best_prize = prizes_in_range

    print(best_prize)

main()