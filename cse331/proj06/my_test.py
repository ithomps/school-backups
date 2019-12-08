from Graph import Graph


def read_graph(filename):
    with open(filename, 'r') as reader:
        g = Graph(int(reader.readline()))
        for line in reader:
            (u, v, w) = line.split()
            g.insert_edge(int(u), int(v), float(w))
        return g


def main(filename):
    g = read_graph(filename)


if __name__ == '__main__':
    main('g1.txt')
