import os
from unittest import TestCase

import matplotlib.pyplot as plt
import networkx as nx

from idleiss.universe import Universe

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def draw_graph(graph):
    nx.draw_networkx(graph, pos=nx.spring_layout(graph), with_labels=True)
    plt.show()


def save_graph(graph, universe, name_of_file):
    plt.figure(figsize=(24, 14))
    color_array = []
    for node in graph:
        if universe.master_dict[node].security == 'High':
            color_array.append('b')
        elif universe.master_dict[node].security == 'Low':
            color_array.append('y')
        elif universe.master_dict[node].security == 'Null':
            color_array.append('r')
        else:
            raise ValueError(node + ": did not have a valid security rating")
    nx.draw_networkx(graph, pos=nx.spring_layout(graph),
                     node_size=24, font_size=16, with_labels=True, node_color=color_array)
    plt.savefig(name_of_file, bbox_inches='tight')
    plt.close()


class UserTestCase(TestCase):

    def setUp(self):
        pass

    def test_load_universe_config(self):
        uni = Universe(os.path.join(__location__, 'config/Universe_Config.json'))
        graph = uni.generate_networkx(uni.systems)
        self.assertEqual(graph.number_of_nodes(), 5100)
        self.assertTrue(nx.is_connected(graph))

    def test_consistent_generation(self):
        uni1 = Universe(os.path.join(__location__, 'config/Universe_Config.json'))
        uni2 = Universe(os.path.join(__location__, 'config/Universe_Config.json'))
        g1 = uni1.generate_networkx(uni1.systems)
        g2 = uni2.generate_networkx(uni2.systems)
        d1 = nx.symmetric_difference(g1, g2)
        d2 = nx.symmetric_difference(g2, g1)
        # d1 and d2 contain only the edges which are different,
        # 0 edges in the d# graph means they are the same
        self.assertEqual(d1.number_of_edges(), 0)
        self.assertEqual(d2.number_of_edges(), 0)

    def test_highsec_is_connected(self):
        uni = Universe(os.path.join(__location__, 'config/Universe_Config.json'))
        highsec_regions_only = [r for r in uni.regions if r.security == 'High']
        self.assertGreater(len(highsec_regions_only), 0)
        highsec_systems_only = []
        for r in highsec_regions_only:
            for c in r.constellations:
                for solar in c.systems:
                    if solar.security == 'High':
                        highsec_systems_only.append(solar)
                        valid_adj = []
                        for adj_solar in solar.connections:
                            if adj_solar.security == "High":
                                valid_adj.append(adj_solar)
                        solar.connections = valid_adj
        graph = uni.generate_networkx(highsec_systems_only)
        self.assertEqual(len(graph), len(highsec_systems_only))
        self.assertTrue(nx.is_connected(graph))
