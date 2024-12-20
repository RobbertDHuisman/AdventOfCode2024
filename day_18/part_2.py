from tqdm import tqdm
from part_1 import load_data

def find_corrupted_locations_on_edge(falling_bytes, size):
    corrupted_on_edge = []
    for i in falling_bytes:
        if i[0] in (0, size - 1):
            corrupted_on_edge.append(i)

    return corrupted_on_edge

def find_surrounding_corruptions(location, falling_bytes):
    surrounding_corruptions = []
    for i in falling_bytes:
        if abs(i[0] - location[0]) <= 1 and abs(i[1] - location[1]) <= 1 and i != location:
            surrounding_corruptions.append(i)

    return surrounding_corruptions

def find_next_corruption_to_check(corruptions_in_fence, corruptions_checked):
    for i in corruptions_in_fence:
        if i not in corruptions_checked:
            return i

    return None

def check_if_fence_is_blocking(corruptions_in_fence, size):
    top = 0
    bottom = 0
    left = 0
    right = 0
    for i in corruptions_in_fence:
        if i[0] == 0:
            top += 1
        if i[0] == size - 1:
            bottom += 1
        if i[1] == 0:
            left += 1
        if i[1] == size - 1:
            right += 1          
    
    if (top > 0 and bottom > 0) or (top > 0 and left > 0) or (bottom > 0 and right > 0):
        return True
    else:
        return False


def find_border_blocking_path(falling_bytes, size):
    corrupted_on_edge = find_corrupted_locations_on_edge(falling_bytes, size)
    edges_found = []

    for i in corrupted_on_edge:
        if i not in edges_found:
            corruptions_in_fence = [i]
            corruptions_checked = []
            next_corruption = corruptions_in_fence[0]
            corruptions_to_check = 1
            while corruptions_to_check > 0:
                if next_corruption[0] in (0, size - 1):
                    edges_found.append(next_corruption)
                surrounding_corruptions = find_surrounding_corruptions(next_corruption, falling_bytes)
                for j in surrounding_corruptions:
                    if j not in corruptions_in_fence:
                        corruptions_in_fence.append(j)
                corruptions_checked.append(next_corruption)
                next_corruption = find_next_corruption_to_check(corruptions_in_fence, corruptions_checked)
                if next_corruption is None:
                    corruptions_to_check = 0

            if check_if_fence_is_blocking(corruptions_in_fence, size):
                return True
    
    return False
                
def main():
    size, start, end, nr_bytes, falling_bytes = load_data("input.csv")
    with tqdm(total=3450) as pbar:
        for i in range(0, len(falling_bytes)):
            if find_border_blocking_path(falling_bytes[0:i+1], size):
                print(f"{falling_bytes[i]} is the location, so write it as {falling_bytes[i][1],falling_bytes[i][0]}")
                break
            pbar.update(1)

main()    