import networkx as nx
import matplotlib.pyplot as plt
from typing import Literal, Mapping

# Проверка двудольности
def is_bipartite(graph: nx.Graph) -> tuple[Literal[True], Mapping] | tuple[Literal[False], None]:
    try:
        color = nx.bipartite.color(graph)
        return True, color
    except nx.NetworkXError:
        return False, None


# Форд-Фалкерсон
def ford_fulkerson_matching(graph: nx.Graph, left, right) -> list[tuple[int, int]]:
    flow_network = nx.DiGraph()

    source = 'source'
    sink = 'sink'
    flow_network.add_node(source)
    flow_network.add_node(sink)

    for node in left:
        flow_network.add_edge(source, node, capacity=1)

    for node in right:
        flow_network.add_edge(node, sink, capacity=1)

    for u, v in graph.edges():
        if u in left and v in right:
            flow_network.add_edge(u, v, capacity=1)
        elif v in left and u in right:
            flow_network.add_edge(v, u, capacity=1)

    flow_value, flow_dict = nx.maximum_flow(flow_network, source, sink)

    matching = []
    for u in flow_dict:
        if u == source or u == sink:
            continue
        for v in flow_dict[u]:
            if v != sink and flow_dict[u][v] == 1:
                matching.append((u, v))

    return matching


# Алгоритм Куна
def kuhn_matching(graph: nx.Graph, left, right) -> list[tuple[int, int]]:
    pair_U = {u: None for u in left}
    pair_V = {v: None for v in right}

    def dfs(u, visited) -> bool:
        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                if pair_V[v] is None or dfs(pair_V[v], visited):
                    pair_U[u] = v
                    pair_V[v] = u
                    return True
        return False

    for u in left:
        dfs(u, set())
    matching = [(u, v) for u, v in pair_U.items() if v is not None]
    return matching


def visualize_graph(graph: nx.Graph, left, right, matching: list[tuple[int, int]], title: str) -> None:
    plt.figure(figsize=(12, 8))
    pos = {}
    left_nodes = sorted(left)
    right_nodes = sorted(right)

    for i, node in enumerate(left_nodes):
        pos[node] = (0, -i)

    for i, node in enumerate(right_nodes):
        pos[node] = (1, -i)

    nx.draw_networkx_nodes(graph, pos, nodelist=left, node_color='lightblue', node_size=500)
    nx.draw_networkx_nodes(graph, pos, nodelist=right, node_color='lightgreen', node_size=500)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1)
    nx.draw_networkx_edges(graph, pos, edgelist=matching, edge_color='red', width=2)
    nx.draw_networkx_labels(graph, pos)

    plt.title(title)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    edges = [
        (3, 5), (3, 10), (4, 6), (4, 8), (4, 10), (4, 13),
        (6, 7), (6, 9), (6, 11), (6, 15), (6, 16), (7, 8),
        (7, 17), (8, 11), (9, 10), (9, 12), (10, 15), (12, 16),
        (13, 14), (13, 15), (16, 17)
    ]

    graph = nx.Graph()
    graph.add_edges_from(edges)



    bipartite, coloring = is_bipartite(graph)
    print(f"Граф двудольный: {bipartite}")

    if not bipartite:
        cycles = list(nx.cycle_basis(graph))
        edges_to_remove = set()
        for cycle in cycles:
            if len(cycle) % 2 != 0:
                edges_to_remove.add((cycle[0], cycle[1]))
        print(f"Удаляем рёбра: {edges_to_remove}")
        graph.remove_edges_from(edges_to_remove)
        bipartite, coloring = is_bipartite(graph)
        print(f"После удаления рёбер граф двудольный: {bipartite}")

    if bipartite:
        left = {node for node in coloring if coloring[node] == 0}
        right = set(graph.nodes()) - left
        print(f"Левая доля: {left}")
        print(f"Правая доля: {right}")
    else:
        print("Не удалось сделать граф двудольным")
        exit()


    ff_matching = ford_fulkerson_matching(graph, left, right)
    k_matching = kuhn_matching(graph, left, right)

    print()
    print("Наибольшее паросочетание (Форд-Фалкерсон):")
    print(ff_matching)
    print(f"Размер: {len(ff_matching)}")

    print()
    print("Наибольшее паросочетание (Кун):")
    print(k_matching)
    print(f"Размер: {len(k_matching)}")

    visualize_graph(graph, left, right, ff_matching, "Наибольшее паросочетание (Форд-Фалкерсон)")
    visualize_graph(graph, left, right, k_matching, "Наибольшее паросочетание (Кун)")