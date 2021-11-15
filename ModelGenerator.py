from Print import print
import networkx as nx
import numpy as np
import random as rnd
from colors import Colors


def generate_random_eq_model(sn_graph):
    node_count = sn_graph.number_of_nodes()
    edge_count = sn_graph.number_of_edges()
    random_graph = nx.fast_gnp_random_graph(node_count, 0.1)
    edge_count_random_graph = random_graph.number_of_edges()
    if edge_count_random_graph == edge_count:
        return random_graph
    elif edge_count_random_graph > edge_count:
        diff = edge_count_random_graph - edge_count
        edge_list = random_graph.edges()
        smp = rnd.sample(list(edge_list), diff)
        for i in smp:
            random_graph.remove_edge(i[0], i[1])
    else:
        diff = edge_count - edge_count_random_graph
        for i in range(0, diff):
            smp = rnd.sample(list(nx.non_edges(sn_graph)), 1)
            random_graph.add_edge(smp[0][0], smp[0][1])
    if edge_count != random_graph.number_of_edges():
        print(f"{Colors.FAIL}ERROR {edge_count} , {edge_count_random_graph} {Colors.ENDC}")
        raise Exception("ERROR in  generate_random_eq_model")
    return random_graph
