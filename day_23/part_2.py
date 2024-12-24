import networkx as nx

from part_1 import load_data

def get_base_cycles(graph):
    cycles = []
    for i in nx.cycle_basis(graph):
        if len(i) == 3:
            cycles.append(i)

    return cycles

def determine_all_nodes_connected(graph, cycles):
    best_cycles = []
    for i in cycles:
        new_cycle = i
        for j in nx.common_neighbors(graph, i[0], i[1]):
            for k in nx.common_neighbors(graph, i[0], i[2]):
                if j == k:
                    new_cycle.append(j)

        new_cycle.sort()
        if new_cycle not in best_cycles:
            best_cycles.append(new_cycle)

    return best_cycles        

def delete_wrong_nodes(graph, cycles):
    for i in cycles:
        for j in i:
            for k in i:
                if j != k:
                    found = 0
                    neighbors = []
                    for m in nx.all_neighbors(graph, j):
                        neighbors.append(m)
                        if j != k and k == m:
                            found = 1
                    
                    neighbors.sort()
                    if found == 0:
                        i.remove(j)

    return cycles


def determine_longest_cycle(cycles):
    longest_cycle = cycles[0]
    for i in range(0, len(cycles)):
        if len(cycles[i]) > len(longest_cycle):
            longest_cycle = cycles[i]
    
    return longest_cycle

def sort_output_to_string(cycle):
    string = cycle[0]
    for i in range(1, len(cycle)):
        string = string + "," + cycle[i]

    return string

def main():
    graph = load_data("input.csv")
    cycles = get_base_cycles(graph)
    best_cycles = determine_all_nodes_connected(graph, cycles)
    true_cycles = delete_wrong_nodes(graph, best_cycles)
    longest_cycle = determine_longest_cycle(true_cycles)
    string = sort_output_to_string(longest_cycle)
    print(string)

main()