import csv
import re

def blink(stones, blinks):
    new_stones = stones
    for i in range(0, blinks):
        print(i)
        stones = new_stones
        new_stones = []
        for j in stones:
            if j == 0:
                new_stones.append(1)
            elif len(str(j)) % 2 == 0:
                new_stones.append(int(str(j)[0:int(len(str(j)) / 2)]))
                new_stones.append(int(str(j)[int(len(str(j)) / 2):int(len(str(j)))]))
            else:
                new_stones.append(j*2024)

    return new_stones

def main():
    example = [125, 17]
    input = [3, 386358, 86195, 85, 1267, 3752457, 0, 741]

    new_stones = blink(input, 75)

    print(len(new_stones))

main()