from tqdm import tqdm
import math
from part_1 import load_data, instructions, make_outputs_to_string

def main():
    register_a, register_b, register_c, program = load_data("input")

    number_to_check = 31

    program_string = make_outputs_to_string(program)[-number_to_check:]
    print(program_string)
    output_string = ""
    register_a_start = 108107566064896
    print(register_a_start)

    # with tqdm(total=100) as pbar:

    while output_string != program_string:
    # for i in range(300):
        register_a = register_a_start
        pointer = 0
        outputs = []
        still_going_strong = 1

        # pbar.update(1)

        while pointer < len(program) and still_going_strong == 1:
            register_a, register_b, register_c, output, pointer = instructions(register_a, register_b, register_c, program[pointer], program[pointer+1], pointer)
            if output is not None:
                outputs.append(output)
                pre_output_string = make_outputs_to_string(outputs)
                if pre_output_string != program_string[0:len(pre_output_string)]:
                    # print(pre_output_string, program_string[0:len(pre_output_string)])
                    still_going_strong = 0
            

            # print(register_a, register_b, register_c, output, pointer)

        output_string = make_outputs_to_string(outputs)

        if output_string[-number_to_check:] == program_string:
            print(f"het is {register_a_start}")

        # print(output_string)
        if output_string != program_string:
            register_a_start += 1


    # print(register_a_start)

main()