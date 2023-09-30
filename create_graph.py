import random
import networkx as nx
import matplotlib.pyplot as plt


def random_idx(lst):
    idx = random.randrange(0, len(lst))
    return lst[idx]


def add_edges(G,l):
    edge_count = 25 
    c = 0
    while c<edge_count:
        rand1 = random_idx(l)
        rand2 = random_idx(l)
        if rand1!=rand2:
            G.add_edge(rand1,rand2)
            c+=1
    nx.draw_circular(G,with_labels=True)
    plt.show()


def add_nodes(G,l):
    for val in l:
        G.add_node(val)
    add_edges(G,l)


def main():
    num_nodes = 15
    l = [val for val in range(15)]
    G1 = nx.Graph()
    add_nodes(G1,l)
    #G2 = nx.complete_graph(10)

if __name__=="__main__":
    main()
