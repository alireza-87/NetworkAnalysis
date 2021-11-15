import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_pdf import PdfPages


class Plot:
    pdf = None

    def __init__(self, _name=""):
        self.name = _name
        if not self.name == "":
            self.pdf = PdfPages(self.name)

    def plot_deg_dist(self, data_to_plot):
        names, counts = zip(*data_to_plot.items())
        plt.bar(names, counts)
        plt.title("Degree Dist")
        plt.xlabel("Nodes name")
        plt.ylabel("Value")
        fig = plt.gcf()
        if not self.name == "":
            self.pdf.savefig(fig)
        plt.show()

    def plot_betweeness(self, data_to_plot):
        names, counts = zip(*data_to_plot.items())
        plt.bar(range(0, len(counts)), counts)
        plt.title("Betweenness")
        plt.xlabel("Nodes name")
        plt.ylabel("Value")
        fig = plt.gcf()
        if not self.name == "":
            self.pdf.savefig(fig)
        plt.show()

    def plot_closeness(self, data_to_plot):
        names, counts = zip(*data_to_plot.items())
        plt.bar(range(0, len(counts)), counts)
        plt.title("Closenedd")
        plt.xlabel("Nodes name")
        plt.ylabel("Value")
        fig = plt.gcf()
        if not self.name == "":
            self.pdf.savefig(fig)
        plt.show()

    def plot_graph(self, sn_graph):
        d = dict(sn_graph.degree)
        if len(list(sn_graph.nodes)) < 35:
            node_size = [v * 50 if v > 0 else 100 for v in d.values()]
            edge_size = 1
        else:
            node_size = 10
            edge_size = 0.1
        nx.draw_random(sn_graph, alpha=0.8, edge_color='black', node_color='red', node_size=node_size,
                with_labels=len(list(sn_graph.nodes)) < 35, font_size=10, width=edge_size)

        fig = plt.gcf()
        if not self.name == "":
            self.pdf.savefig(fig, bbox_inches='tight')
        plt.show()

    def plot_graph_two_color(self, sn_graph, node_list):
        colors = []
        d = dict(sn_graph.degree)
        if len(list(sn_graph.nodes)) < 35:
            node_size = [v * 50 if v > 0 else 100 for v in d.values()]
            edge_size = 1
        else:
            node_size = 10
            edge_size = 0.1

        for nodes in sn_graph.nodes():
            if nodes in node_list:
                colors.append('blue')
            else:
                colors.append('red')
        nx.draw(sn_graph, alpha=0.8, edge_color='black', node_color=colors, node_size=node_size,
                with_labels=len(list(sn_graph.nodes)) < 35,font_size=10, width=edge_size)
        fig = plt.gcf()
        if not self.name == "":
            self.pdf.savefig(fig, bbox_inches='tight')
        plt.show()

    def close(self):
        self.pdf.close()
