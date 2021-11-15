from random import choice

import networkx as nx


def random_attack(sn_graph, count):
    node_list = [i for i in sn_graph.nodes()]
    for index in range(0, count):
        rem_node = choice(node_list)
        node_list.remove(rem_node)
        sn_graph.remove_node(rem_node)


def highest_degree_attack(sn_graph, count):
    degrees = dict((node, val) for (node, val) in sn_graph.degree())
    for index in range(0, count):
        rem_node = max(degrees, key=lambda key: degrees[key])
        sn_graph.remove_node(rem_node)
        degrees.pop(rem_node, None)


def highest_betweenness_attack(sn_graph, count):
    between_ness = nx.betweenness_centrality(sn_graph, normalized=True)
    for index in range(0, count):
        rem_node = max(between_ness, key=lambda key: between_ness[key])
        sn_graph.remove_node(rem_node)
        between_ness.pop(rem_node, None)


def highest_page_rank_attack(sn_graph, count):
    page_rank = nx.pagerank(sn_graph)
    for index in range(0, count):
        rem_node = max(page_rank, key=lambda key: page_rank[key])
        sn_graph.remove_node(rem_node)
        page_rank.pop(rem_node, None)
