import collections
import time

import networkx as nx
import numpy as np

from colors import Colors
from plot import Plot
from utility import filter_dict
from Print import print
from Print import save


def display_info(sn_graph, _save_file=False):
    now = str(time.time())
    save(_save_file)
    if _save_file:
        plotter = Plot(now + ".pdf")
    else:
        plotter = Plot()
    print(f"{Colors.OKCYAN}******************** Display info ********************{Colors.ENDC}")
    plotter.plot_graph(sn_graph)
    print(nx.info(sn_graph))

    # Number of link
    total_number_of_link = sum(dict(sn_graph.degree).values()) / 2
    total_number_of_link_average = (2 * total_number_of_link) / sn_graph.number_of_nodes()
    print(f"{Colors.OKGREEN}Total Number of Link (L) : {total_number_of_link} {Colors.ENDC}")
    print(f"{Colors.OKGREEN}Average Number of Link <k> : {total_number_of_link_average}{Colors.ENDC}")

    # density
    network_density = total_number_of_link_average / (sn_graph.number_of_nodes() - 1)
    print(f"{Colors.OKGREEN}network_density (P) - our Calculation : {network_density}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}network_density (P) - nx  Calculation : {nx.density(sn_graph)}{Colors.ENDC}")

    # Degree Distribution
    degree_sequence = sorted([d for n, d in sn_graph.degree()], reverse=True)  # degree sequence
    degree_count = collections.Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())
    plotter.plot_deg_dist(filter_dict(degree_count, lambda k, v: v != 0))

    degree_sequence = sorted([d for n, d in sn_graph.degree()], reverse=True)

    # Betweenness
    # cg_list = list(sn_graph.subgraph(c) for c in nx.connected_components(sn_graph))
    if nx.is_directed(sn_graph):
        print(f"{Colors.FAIL}Not implement for direct graph {Colors.ENDC}")
    else:
        betweenness = nx.betweenness_centrality(sn_graph, normalized=True)
        if np.max(np.array(list(betweenness.values()))) == 0.0 and np.mean(np.array(list(betweenness.values()))) == 0.0:
            print(f"{Colors.WARNING}Unable to plot betweenness all values are ZERO! {Colors.ENDC}")
        else:
            plotter.plot_betweeness(betweenness)
            # plotter.plot_betweeness(filter_dict(betweenness, lambda k, v: v != 0.0))
        print(
            f"{Colors.OKGREEN}betweenness centrality (maximum): {np.max(np.array(list(betweenness.values())))}{Colors.ENDC}")
        print(
            f"{Colors.OKGREEN}betweenness centrality (average): {np.mean(np.array(list(betweenness.values())))}{Colors.ENDC}")
        print(
            f"{Colors.OKGREEN}betweenness TOP: {sorted(betweenness.items(), key=lambda item: item[1], reverse=True)[:10 if len(betweenness) > 9 else len(betweenness)]}{Colors.ENDC}")

    # Closeness
    closeness = nx.closeness_centrality(sn_graph)
    if np.max(np.array(list(closeness.values()))) == 0.0 and np.mean(np.array(list(closeness.values()))) == 0.0:
        print(f"{Colors.WARNING}Unable to plot betweenness all values are ZERO! {Colors.ENDC}")
    else:
        plotter.plot_closeness(closeness)
        # plotter.plot_closeness(filter_dict(closeness, lambda k, v: v != 0.0))

    if _save_file:
        plotter.close()

    print(f"{Colors.OKGREEN}closeness centrality (maximum): {np.max(np.array(list(closeness.values())))}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}closeness centrality (average): {np.mean(np.array(list(closeness.values())))}{Colors.ENDC}")
    print(
        f"{Colors.OKGREEN}closeness TOP: {sorted(closeness.items(), key=lambda item: item[1], reverse=False)[:10 if len(closeness) > 9 else len(closeness)]}{Colors.ENDC}")

    print(
        f"{Colors.OKGREEN}TOP Degree: {sorted([(sn_graph.degree(n), n) for n in sn_graph.nodes()], reverse=True)[:10 if len(sn_graph.nodes()) > 9 else len(sn_graph.nodes())]}{Colors.ENDC}")

    # Any Separate node?
    print(f"{Colors.OKGREEN}Any separate node: {nx.number_of_isolates(sn_graph)}{Colors.ENDC}")

    # diameter
    diameter = 0
    if not nx.is_directed(sn_graph) and nx.is_connected(sn_graph):
        diameter = nx.diameter(sn_graph)
    else:
        diameter = max([max(j.values()) for (i, j) in nx.shortest_path_length(sn_graph)])
    print(f"{Colors.OKGREEN}graph diameter : {diameter}{Colors.ENDC}")

    # Component
    if not nx.is_directed(sn_graph):
        print(
            f"{Colors.OKGREEN}Giant Components : {sorted([len(c) for c in sorted(nx.connected_components(sn_graph), key=len, reverse=True)], reverse=True)}{Colors.ENDC}")
    else:
        print(f"{Colors.OKGREEN}Is strongly connected : {nx.is_strongly_connected(sn_graph)}{Colors.ENDC}")
        print(
            f"{Colors.OKGREEN}Number of Strongly component : {nx.number_strongly_connected_components(sn_graph)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Is weakly connected : {nx.is_strongly_connected(sn_graph)}{Colors.ENDC}")
        print(
            f"{Colors.OKGREEN}Number of weakly component : {nx.number_strongly_connected_components(sn_graph)}{Colors.ENDC}")

    print(f"{Colors.OKGREEN}is Directed : {nx.is_directed(sn_graph)}{Colors.ENDC}")
    if not nx.is_directed(sn_graph):
        print(f"{Colors.OKGREEN}is Connected : {nx.is_connected(sn_graph)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Triangles : {nx.triangles(sn_graph)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Cluster : {nx.clustering(sn_graph)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Transitivity : {nx.transitivity(sn_graph)}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Average clustering : {nx.average_clustering(sn_graph)}{Colors.ENDC}")
