
def blink(stones):
    new_stones = []
    for j in stones:
        if j[0] == 0:
            new_stones.append([1, j[1]])
        elif len(str(j[0])) % 2 == 0:
            new_stones.append([int(str(j[0])[0:int(len(str(j[0])) / 2)]), j[1]])
            new_stones.append([int(str(j[0])[int(len(str(j[0])) / 2):int(len(str(j[0])))]), j[1]])
        else:
            new_stones.append([j[0]*2024, j[1]])

    return new_stones

def add_number_of_stones(stones):
    stones_with_amount = []
    for i in stones:
        stones_with_amount.append([i, 1])

    return stones_with_amount

def count_amount(stones):
    length = len(stones)
    for i in range(length - 1, -1, -1):
        for j in range(i-1, -1, -1):
            if stones[i][0] == stones[j][0]:
                stones[j][1] = stones[j][1] + stones[i][1]
                del stones[i]
                break

    return stones

def count_total_amount(stones):
    total = 0
    for i in stones:
        total += i[1]

    return total

def main():
    example = [125, 17]
    input = [3, 386358, 86195, 85, 1267, 3752457, 0, 741]

    new_stones = add_number_of_stones(input)
    for i in range(25):
        stones = new_stones
        stones_after_blink = blink(stones)
        new_stones = count_amount(stones_after_blink)

    print(count_total_amount(new_stones))

main()