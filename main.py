from Print import print
import time
import statistics
from itertools import chain

import networkx as nx
import os
import attack as atk
import graph_info as gi
from colors import Colors
import random as rnd
from plot import Plot
import builtins as __builtin__
from Print import save
from ModelGenerator import generate_random_eq_model


def fetch_hugest_subgraph(graph_):
    g_cc = max(nx.connected_components(graph_), key=len)
    giant_c = graph_.subgraph(g_cc)
    return giant_c


def small_world(_graph, _random_eq_graph):
    g_c = nx.average_clustering(_graph)
    g_r = nx.average_clustering(_random_eq_graph)
    data = []
    for component in nx.connected_components(_graph):
        component_ = _graph.subgraph(component)
        temp = nx.average_shortest_path_length(component_)
        if temp > 0:
            data.append(temp)

    data_2 = []
    for component in nx.connected_components(_random_eq_graph):
        component_ = _random_eq_graph.subgraph(component)
        temp = nx.average_shortest_path_length(component_)
        if temp > 0:
            data_2.append(temp)

    # data = [max(j.values()) for (i, j) in nx.shortest_path_length(_graph)]
    l_c = statistics.mean(data)

    # data_2 = [max(j.values()) for (i, j) in nx.shortest_path_length(_random_eq_graph)]
    l_r = statistics.mean(data_2)

    # l_c = nx.average_shortest_path_length(_graph)
    # l_r = nx.average_shortest_path_length(_random_eq_graph)
    s_w = (g_c / g_r) / (l_c / l_r)
    if s_w > 1.0:
        print(f"{Colors.OKGREEN}Does have small-world properties{Colors.ENDC}" + str(s_w))
    else:
        print(f"{Colors.FAIL}Does not have small-world properties{Colors.ENDC}" + str(s_w))


def h_model(_number_of_nodes, _lambda):
    n = _number_of_nodes
    g = nx.Graph()
    g.add_node(0)
    vertices = [0]
    n = n - 1
    node_index = 1
    while n > 0 and len(vertices) > 0:
        v = vertices.pop(0)
        deg = round(_lambda())
        for i in range(deg):
            g.add_node(node_index)
            n = n - 1
            g.add_edge(v, node_index)
            vertices.append(node_index)
            node_index = node_index + 1
            if n <= 0:
                break
    return g


def power_law_seq(number_of_nodes, _lambda, _buit_in):
    if _buit_in:
        return nx.random_powerlaw_tree_sequence(n=number_of_nodes, gamma=_lambda, seed=None, tries=50000)
    else:
        while True:
            sequence = []
            while len(sequence) < number_of_nodes:
                nextval = int(nx.utils.powerlaw_sequence(1, 2.6)[0])  # 100 nodes, power-law exponent 2.5
                if nextval != 0:
                    sequence.append(nextval)
            if sum(sequence) % 2 == 0:
                break
        return sequence


def clear_screen():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def relabel(dataset):
    return nx.convert_node_labels_to_integers(dataset, first_label=0, ordering='default')


def measurement_analysis(_dataset, _save_report):
    print(f"{Colors.OKBLUE}*** Graph analysis{Colors.ENDC}")
    gi.display_info(_dataset, _save_report)


def call_adaption(_dataset, _node, _pay_off, _nodes_adoption):
    payoff_matrix = [
        [1, 0],
        [0, _pay_off]
    ]
    q = payoff_matrix[1][1] / (payoff_matrix[0][0] + payoff_matrix[1][1])
    p = 0
    neighbors = _dataset[_node]
    for d in neighbors:
        if _nodes_adoption[d] == 0:
            p += 1
    if len(neighbors) == 0:
        return _nodes_adoption[_node]
    p /= len(neighbors)
    return 0 if p >= q else 1


def social_contagion(_dataset, _save_report, initial_node, pay_off):
    nodes_count = len(_dataset.nodes())
    nodes_adoption = [0] * nodes_count
    now = str(time.time())
    if _save_report:
        plotter = Plot(now + ".pdf")
    else:
        plotter = Plot()
    print(f"{Colors.OKBLUE}*** social_contagion{Colors.ENDC}")
    for smp in rnd.sample(list(_dataset.nodes()), initial_node):
        nodes_adoption[smp] = 1
    node_changes = True
    step = 1
    data_set_change = []
    while node_changes:

        for item_node in list(_dataset.nodes()):
            if nodes_adoption[item_node] == 1:
                data_set_change.append(item_node)
        if len(data_set_change) > 0:
            print(len(data_set_change))
            plotter.plot_graph_two_color(_dataset, data_set_change)
        step += 1
        node_changes = False
        for node in _dataset.nodes():
            adoption = call_adaption(_dataset, node, pay_off, nodes_adoption)
            if nodes_adoption[node] != 1 and adoption != nodes_adoption[node]:
                node_changes = True
                nodes_adoption[node] = adoption
    green_p = len([0 for x in nodes_adoption if x == 0]) / nodes_count * 100
    blue_p = 100 - green_p
    if blue_p != 100:
        print(f"{Colors.FAIL}steps: {step} red ={green_p} blue = {blue_p}% {Colors.ENDC}")
    else:
        print(f"{Colors.OKGREEN}steps: {step} red ={green_p} blue = {blue_p}% {Colors.ENDC}")
    if _save_report:
        plotter.close()


def measurement_and_attack(_dataset_relabel, _save_report):
    node_count = int(input("How many attack : "))

    print(f"{Colors.OKBLUE}*** Graph analysis{Colors.ENDC}")
    dataset_relabel_orginal = _dataset_relabel.copy()
    gi.display_info(dataset_relabel_orginal, _save_report)

    print(f"{Colors.WARNING}*** Random attack{Colors.ENDC}")
    dataset_relabel_randomattak = _dataset_relabel.copy()
    atk.random_attack(dataset_relabel_randomattak, node_count)
    gi.display_info(dataset_relabel_randomattak, _save_report)

    print(f"{Colors.WARNING}*** Highest degree attack{Colors.ENDC}")
    dataset_relabel_maxdattak = _dataset_relabel.copy()
    atk.highest_degree_attack(dataset_relabel_maxdattak, node_count)
    gi.display_info(dataset_relabel_maxdattak, _save_report)

    print(f"{Colors.WARNING}*** Betweenness attack{Colors.ENDC}")
    if nx.is_directed(_dataset_relabel):
        print(f"{Colors.FAIL}Not implement for diGraph{Colors.ENDC}")
    else:
        dataset_relabel_between_ness_attak = _dataset_relabel.copy()
        atk.highest_betweenness_attack(dataset_relabel_between_ness_attak, node_count)
        gi.display_info(dataset_relabel_between_ness_attak, _save_report)

    print(f"{Colors.WARNING}*** Pagerank attack{Colors.ENDC}")
    dataset_relabel_page_rank_attak = _dataset_relabel.copy()
    atk.highest_page_rank_attack(dataset_relabel_page_rank_attak, node_count)
    gi.display_info(dataset_relabel_page_rank_attak, _save_report)


def menu():
    clear_screen()
    __builtin__.print(f"{Colors.OKCYAN}*********** NetWork Analysis ***********{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(1) RandomGraph{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(2) Lattice{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(3) Complete{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(4) Zachary’s Karate Club graph{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(5) Davis Southern women social network{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(6) directed scale free{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(7) directed random k out{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(8) configuration model{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(9) H model{Colors.ENDC}")
    __builtin__.print(f"{Colors.BOLD}(10) graph path{Colors.ENDC}")
    selected_graph = int(input("Enter Graph :"))
    if selected_graph == 1:
        number_of_nodes = int(input("Network size(nodes) : "))
        dataset = nx.fast_gnp_random_graph(number_of_nodes, 0.1)
    elif selected_graph == 2:
        row = int(input("row : "))
        col = int(input("col : "))
        dataset = nx.grid_graph(dim=(row, col))
    elif selected_graph == 3:
        number_of_nodes = int(input("Network size(nodes) : "))
        dataset = nx.complete_graph(number_of_nodes)
    elif selected_graph == 4:
        dataset = nx.karate_club_graph()
    elif selected_graph == 5:
        dataset = nx.davis_southern_women_graph()
    elif selected_graph == 6:
        number_of_nodes = int(input("Network size(nodes) : "))
        dataset = nx.scale_free_graph(number_of_nodes)
    elif selected_graph == 7:
        number_of_nodes = int(input("Network size(nodes) : "))
        dataset = nx.random_k_out_graph(number_of_nodes, 3, 0.3, self_loops=True, seed=None)
    elif selected_graph == 8:
        number_of_nodes = int(input("Network size(nodes) : "))
        _lambda = float(input("Lambda : "))
        is_built_in = input("NX built in method(y/n)? ") == 'y'
        sequence = power_law_seq(number_of_nodes, _lambda, is_built_in)
        dataset = nx.configuration_model(sequence)
        dataset = nx.Graph(dataset)
        dataset.remove_edges_from(nx.selfloop_edges(dataset))
    elif selected_graph == 9:
        number_of_nodes = int(input("Network size(nodes) : "))
        dataset = h_model(number_of_nodes, lambda: rnd.randint(1, 5))
    elif selected_graph == 10:
        database = input("DataBase Path : ")
        if not database.endswith('.gml'):
            dataset = nx.read_adjlist(database)
        else:
            dataset = nx.read_gml(database, label='id')

    __builtin__.print("(1) Analysis Measurement Parameter")
    __builtin__.print("(2) Simulate attacks on network")
    __builtin__.print("(3) Social contagion")
    __builtin__.print("(4) small-world")
    selected_menu = input("Enter Menu number :")
    save_report = input("Save Report(y/n) :") == 'y'
    save(save_report)
    dataset = relabel(dataset)
    if selected_menu == "1":
        measurement_analysis(dataset, save_report)
    elif selected_menu == "2":
        measurement_and_attack(dataset, save_report)
    elif selected_menu == "3":
        iterations = int(input("iterations : "))
        initial_node = int(input("Initial nodes : "))
        pay_off = float(input("payoff : "))
        for _ in range(iterations):
            social_contagion(dataset, save_report, initial_node, pay_off)
    elif selected_menu == "4":
        graph = generate_random_eq_model(dataset)
        small_world(dataset, graph)


if __name__ == '__main__':
    menu()
