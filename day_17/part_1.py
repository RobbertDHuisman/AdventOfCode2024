import math

def load_data(filename):
    if filename == "example":
        register_a = 729
        register_b = 0
        register_c = 0
        program = [0,1,5,4,3,0]
    elif filename == "example1":
        register_a = 2024
        register_b = 0
        register_c = 0
        program = [0,1,5,4,3,0]
    if filename == "example2":
        register_a = 2024
        register_b = 0
        register_c = 0
        program = [0,3,5,4,3,0]
    elif filename == "input":
        # register_a = 37283687
        register_a = 107752139522048
        register_b = 0
        register_c = 0
        program = [2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0]

    return register_a, register_b, register_c, program

def get_combo_operand(register_a, register_b, register_c, operand):
    if operand < 4:
        combo_operand = operand
    elif operand == 4:
        combo_operand = register_a
    elif operand == 5:
        combo_operand = register_b
    elif operand == 6:
        combo_operand = register_c
    else:
        combo_operand = None

    return combo_operand

def adv(register_a, combo_operand):
    return int(math.floor(register_a / 2**combo_operand))   

def bxl(register_b, operand):
    return register_b ^ operand

def bst(combo_operand):
    return combo_operand % 8

def jnz(register_a, operand, pointer):
    if register_a == 0:
        return pointer
    else:
        return operand
    
def bxc(register_b, register_c, operand):
    return register_b ^ register_c

def out(combo_operand):
    return combo_operand % 8

def instructions(register_a, register_b, register_c, opcode, operand, pointer):
    output = None
    pointer += 2
    combo_operand = get_combo_operand(register_a, register_b, register_c, operand)
    # print(combo_operand)
    if opcode == 0:
        register_a = adv(register_a, combo_operand)
    elif opcode == 1:
        register_b = bxl(register_b, operand)
    elif opcode == 2:
        register_b = bst(combo_operand)
    elif opcode == 3:
        pointer = jnz(register_a, operand, pointer)
    elif opcode == 4:
        register_b = bxc(register_b, register_c, operand)
    elif opcode == 5:
        output = out(combo_operand)
    elif opcode == 6:
        register_b = adv(register_a, combo_operand)
    elif opcode == 7:
        register_c = adv(register_a, combo_operand)

    return register_a, register_b, register_c, output, pointer

def make_outputs_to_string(outputs):
    string = f"{outputs[0]}"
    for i in range(1, len(outputs)):
        string = string + "," + str(outputs[i])
    
    return string

def main():
    register_a, register_b, register_c, program = load_data("input")
    outputs = []
    pointer = 0
    counter = 0

    while pointer < len(program):
        register_a, register_b, register_c, output, pointer = instructions(register_a, register_b, register_c, program[pointer], program[pointer+1], pointer)
        if output is not None:
            # print(counter)
            outputs.append(output)

            print(register_a, register_b, register_c, output, pointer)
        counter += 1
    output_string = make_outputs_to_string(outputs)

    print(output_string)


# main()