import csv
import networkx as nx

def load_data(filename):
    graph = nx.Graph()
    with open(filename, 'r') as file:
        csv_file = csv.reader(file, delimiter="-")

        for row in csv_file:
            graph.add_edge(row[0], row[1])

    return graph

def find_cycles(graph, length):
    cycles = []
    for i in nx.simple_cycles(graph, length):
        if len(i) == length:
            for j in i:
                if j[0:1] == "t":
                    cycles.append(i)
                    break

    return cycles

def main():
    graph = load_data("input.csv")
    cycles = find_cycles(graph, 3)
    print(len(cycles))

main()