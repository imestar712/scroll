__author__ = 'ict'

import calculate.feature.core
import calculate.similarity.core
import calculate.helper.importance

from calculate.graph import Graph


def graph_relation(data, ft_mtd, sim_mtd, importance=False):
    g = Graph(True)
    data_list = list(data.items())
    ft_dict = {}
    for key, odata in data_list:
        ft_dict[key] = calculate.feature.core.method(ft_mtd, odata)
    if importance:
        calculate.helper.importance.importance(ft_dict)
    for i in range(len(data_list)):
        for j in range(i + 1):
            id_a = data_list[i][0]
            id_b = data_list[j][0]
            if g.node(id_a) is None:
                g.add_node(id_a)
            if g.node(id_b) is None:
                g.add_node(id_b)
            g.add_edge((id_a, id_b), calculate.similarity.core.method(sim_mtd, ft_dict[id_a], ft_dict[id_b]))
    return g


def graph_edge(data):
    g = Graph()
    for edge in data:
        if len(edge) != 2:
            continue
        if g.node(edge[0]) is None:
            g.add_node(edge[0])
        if g.node(edge[1]) is None:
            g.add_node(edge[1])
        g.add_edge(edge)
    return g


def graphs_node_set(super, node_set):
    graphs = []
    for nodes in node_set:
        g = Graph()
        for node in nodes:
            g.add_node(node)
        g.complete()
        graphs.append(g)
    return graphs