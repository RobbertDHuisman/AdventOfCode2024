from tqdm import tqdm
import math
# from part_1 import get_combo_operand

def find_out_number():
    program = [2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0]
    # Volgorde is:
    # modulo 8 van a en stop in b
    # bitwise xor van b en 3 en stop in b
    # floor(a / 2^b) en stop in c
    # bitwise xor van b en c en stop in b
    # bitwise xor van b en 3 en stop in b
    # floor(a / 2^b) en stop in a
    # output b
    # a = 24252841
    # 3, 24, 196
    a = 13513445758112
    end_b = 5

    print(a*8)

    # print(a)
    # print(3*8**15)
    a = 196

    start_a = a*2**3
    end_a = (a+1)*2**3
    # print(start_a, end_a)
    for a in range(start_a, end_a):
        # a = start_a + j
        # print(f"check voor a = {a}, end_b ={end_b}")
        b = a % 8
        b = b ^ 3
        c = math.floor(a/2**b)
        b = b ^ c
        b = b ^ 3
        # if b == end_b:
        # print(a, b, c, end_b)

                    

find_out_number()

