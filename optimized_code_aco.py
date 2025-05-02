import numpy as np
import random
from concurrent.futures import ProcessPoolExecutor
import copy


# Helper: Create the Graph
class Graph:
    def __init__(self, distances):
        self.distances = np.array(distances)
        self.nodes = len(distances)
        self.intensity = np.ones((self.nodes, self.nodes))  # pheromone matrix


# Helper: Traverse a graph using vectorized node selection
def traverse_graph(graph, start_node, alpha=1.0, beta=3.0):
    visited = set()
    path = []
    current_node = start_node
    visited.add(current_node)

    while len(visited) < graph.nodes:
        not_visited = list(set(range(graph.nodes)) - visited)
        pheromones = graph.intensity[current_node, not_visited]
        dists = graph.distances[current_node, not_visited]

        # Avoid divide-by-zero issues
        with np.errstate(divide='ignore', invalid='ignore'):
            desirability = (pheromones ** alpha) * ((1.0 / dists) ** beta)
            desirability = np.nan_to_num(desirability)

        if np.sum(desirability) == 0:
            weights = np.ones_like(desirability) / len(desirability)
        else:
            weights = desirability / np.sum(desirability)

        next_node = np.random.choice(not_visited, p=weights)
        path.append((current_node, next_node))
        visited.add(next_node)
        current_node = next_node

    path.append((current_node, start_node))  # complete the cycle
    return path


# Helper: Calculate total path cost
def path_cost(graph, path):
    return sum(graph.distances[a][b] for a, b in path)


# Helper: Update pheromone intensities
def update_pheromones(graph, all_paths, decay, Q):
    graph.intensity *= decay
    for path in all_paths:
        cost = path_cost(graph, path)
        for (i, j) in path:
            graph.intensity[i][j] += Q / cost
            graph.intensity[j][i] += Q / cost  # undirected


# Main Ant Colony Optimization function using ProcessPoolExecutor
def aco(graph, iterations=100, ants_per_iteration=10, alpha=1.0, beta=3.0, decay=0.5, Q=100):
    best_path = None
    best_cost = float('inf')
    base_graph = copy.deepcopy(graph)  # For safe multiprocessing

    for _ in range(iterations):
        with ProcessPoolExecutor() as executor:
            starts = [random.randint(0, graph.nodes - 1) for _ in range(ants_per_iteration)]
            args = [(base_graph, start, alpha, beta) for start in starts]
            paths = list(executor.map(lambda args: traverse_graph(*args), args))

        update_pheromones(graph, paths, decay, Q)

        for path in paths:
            cost = path_cost(graph, path)
            if cost < best_cost:
                best_cost = cost
                best_path = path

    return best_path, best_cost

