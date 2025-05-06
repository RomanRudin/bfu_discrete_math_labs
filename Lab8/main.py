import numpy as np
from collections import deque


class Edge:
    def __init__(self, to, rev, capacity) -> None:
        self.to = to
        self.rev = rev
        self.capacity = capacity


class MaxFlow:
    def __init__(self, size) -> None:
        assert size > 0
        self.size = size
        self.graph = [[] for _ in range(self.size)]

    def add_edge(self, fr, to, cap) -> None:
        forward = Edge(to, len(self.graph[to]), cap)
        backward = Edge(fr, len(self.graph[fr]), 0)
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def bfs_level(self, s, level) -> None:
        q = deque()
        level[:] = [-1] * self.size
        level[s] = 0
        q.append(s)
        while q:
            v = q.popleft()
            for edge in self.graph[v]:
                if edge.capacity > 0 and level[edge.to] < 0:
                    level[edge.to] = level[v] + 1
                    q.append(edge.to)

    def dfs_flow(self, v, t, upTo, iter_, level):
        if v == t:
            return upTo
        for i in range(iter_[v], len(self.graph[v])):
            edge = self.graph[v][i]
            if edge.capacity > 0 and level[v] < level[edge.to]:
                d = self.dfs_flow(edge.to, t, min(upTo, edge.capacity), iter_, level)
                if d > 0:
                    edge.capacity -= d
                    self.graph[edge.to][edge.rev].capacity += d
                    return d
            iter_[v] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        level = [-1] * self.size
        while True:
            self.bfs_level(s, level)
            if level[t] < 0:
                break
            iter_ = [0] * self.size
            while True:
                f = self.dfs_flow(s, t, float('inf'), iter_, level)
                if f == 0:
                    break
                flow += f
            level = [-1] * self.size
        return flow

    def min_cut(self, s) -> list[bool]:
        visited = [False] * self.size
        q = deque()
        q.append(s)
        visited[s] = True
        while q:
            v = q.popleft()
            for edge in self.graph[v]:
                if edge.capacity > 0 and not visited[edge.to]:
                    visited[edge.to] = True
                    q.append(edge.to)
        return visited


def solve_problem(adj_matrix, description) -> None:
    print(f"\n{description}")
    print("Матрица смежности:")
    for row in adj_matrix:
        print(row)

    N = len(adj_matrix)
    mf = MaxFlow(N)

    for i in range(N):
        for j in range(N):
            if adj_matrix[i][j] > 0:
                mf.add_edge(i, j, adj_matrix[i][j])

    max_flow = mf.max_flow(0, N - 1)
    print()
    print(f"Максимальный поток: {max_flow}")

    # Минимальный разрез
    visited = mf.min_cut(0)
    min_cut = []
    for i in range(N):
        for edge in mf.graph[i]:
            if visited[i] and not visited[edge.to] and adj_matrix[i][edge.to] > 0:
                min_cut.append((i, edge.to, adj_matrix[i][edge.to]))

    print()
    print("Минимальный разрез проходит через ребра:")
    for edge in min_cut:
        print(f"{edge[0]} -> {edge[1]} (capacity: {edge[2]})")



if __name__ == "__main__":
    original_matrix = [
    # to A  B  C  D  E  F  G  H  I      from
        [0, 5, 9, 0, 0, 0, 0, 0, 4],    # A
        [0, 0, 2, 0, 0, 0, 2, 0, 2],    # B
        [0, 0, 0, 0, 0, 0, 0, 0, 0],    # C
        [0, 0, 2, 0, 0, 0, 0, 0, 0],    # D
        [0, 0, 0, 2, 0, 0, 0, 0, 0],    # E
        [0, 0, 2, 7, 7, 0, 3, 0, 0],    # F
        [0, 0, 7, 3, 3, 3, 0, 0, 0],    # G
        [0, 0, 7, 0, 0, 7, 7, 0, 0],    # H
        [0, 0, 4, 0, 0, 0, 2, 7, 0],    # I
    ]

    solve_problem(original_matrix, "Исходная задача")

    np.random.seed(7)
    random_matrix = np.array(original_matrix)
    nonzero_indices = np.where(random_matrix > 0)
    random_values = np.random.randint(100, 1000, size=len(nonzero_indices[0]))
    for idx, (i, j) in enumerate(zip(*nonzero_indices)):
        random_matrix[i][j] = random_values[idx]

    print(random_matrix)
    solve_problem(random_matrix, "Задача со случайными пропускными способностями [100, 1000]:")