from collections import deque
import heapq


CAMPUS_GRAPH = {
    "CS": {
        "E": 2,
        "ECS Lawn": 1,
        "EC": 3,
        "RH": 5
    },
    "E": {
        "CS": 2,
        "ECS Lawn": 1,
        "SHCC": 3,
        "KHS": 4
    },
    "ECS Lawn": {
        "CS": 1,
        "E": 1,
        "PL": 3,
        "EC": 2,
        "SHCC": 3
    },
    "EC": {
        "CS": 3,
        "ECS Lawn": 2,
        "PL": 2,
        "H": 3
    },
    "PL": {
        "ECS Lawn": 3,
        "EC": 2,
        "B": 2,
        "CPAC": 4,
        "H": 4,
        "MH": 5
    },
    "B": {
        "PL": 2,
        "TSU": 3,
        "KHS": 3,
        "CPAC": 3
    },
    "TSU": {
        "B": 3,
        "SRC": 2,
        "VA": 3,
        "TH": 4,
        "CPAC": 4
    },
    "SRC": {
        "TSU": 2,
        "KHS": 2,
        "SCPS": 1
    },
    "KHS": {
        "SRC": 2,
        "B": 3,
        "E": 4,
        "TG": 1,
        "SHCC": 3
    },
    "TG": {
        "KHS": 1,
        "SHCC": 3,
        "TSC": 5
    },
    "SHCC": {
        "TG": 3,
        "KHS": 3,
        "E": 3,
        "ECS Lawn": 3,
        "RG": 2
    },
    "RG": {
        "SHCC": 2,
        "RH": 3,
        "TDH": 4
    },
    "RH": {
        "RG": 3,
        "TDH": 2,
        "CS": 5,
        "ENPS": 4
    },
    "TDH": {
        "RH": 2,
        "RG": 4,
        "ENPS": 4
    },
    "ENPS": {
        "RH": 4,
        "TDH": 4,
        "ESPS": 2,
        "E1": 2
    },
    "ESPS": {
        "ENPS": 2,
        "E1": 2,
        "SGMH": 5
    },
    "E1": {
        "ENPS": 2,
        "ESPS": 2,
        "H": 3,
        "GH": 4
    },
    "H": {
        "EC": 3,
        "PL": 4,
        "E1": 3,
        "GH": 2
    },
    "GH": {
        "H": 2,
        "SGMH": 2,
        "MH": 3,
        "LH": 2,
        "E1": 4
    },
    "SGMH": {
        "GH": 2,
        "LH": 2,
        "ESPS": 5
    },
    "LH": {
        "SGMH": 2,
        "GH": 2,
        "MH": 2,
        "DBH": 2
    },
    "MH": {
        "LH": 2,
        "GH": 3,
        "DBH": 2,
        "PL": 5,
        "CPAC": 4
    },
    "DBH": {
        "MH": 2,
        "LH": 2,
        "GC": 3,
        "MC": 1
    },
    "MC": {
        "DBH": 1,
        "E2": 2
    },
    "GC": {
        "DBH": 3,
        "CPAC": 4
    },
    "CPAC": {
        "PL": 4,
        "B": 3,
        "TSU": 4,
        "VA": 3,
        "GC": 4,
        "MH": 4
    },
    "VA": {
        "CPAC": 3,
        "TSU": 3,
        "NPS": 3,
        "TH": 2
    },
    "TH": {
        "VA": 2,
        "TSU": 4,
        "ASC": 2
    },
    "ASC": {
        "TH": 2
    },
    "NPS": {
        "VA": 3,
        "E2": 2,
        "E3": 2
    },
    "E2": {
        "NPS": 2,
        "MC": 2,
        "E3": 2
    },
    "E3": {
        "NPS": 2,
        "E2": 2
    },
    "SCPS": {
        "SRC": 1,
        "UP": 2
    },
    "UP": {
        "SCPS": 2
    },
    "TSC": {
        "TG": 5,
        "IF": 2,
        "TS": 3,
        "AF": 3
    },
    "IF": {
        "TSC": 2,
        "EP": 2,
        "TTC": 2
    },
    "EP": {
        "IF": 2,
        "TSF": 2
    },
    "TS": {
        "TSC": 3
    },
    "AF": {
        "TSC": 3,
        "GF": 2
    },
    "GF": {
        "AF": 2
    },
    "TTC": {
        "IF": 2
    },
    "TSF": {
        "EP": 2
    }
}


def bfs_path(graph, start, end):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        current, path = queue.popleft()

        if current == end:
            return path

        if current not in visited:
            visited.add(current)

            for neighbor in graph[current]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return None


def dfs_traversal(graph, start):
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return order


def is_connected_to(graph, start, end):
    order = dfs_traversal(graph, start)
    return end in order, order


def dijkstra_shortest_path(graph, start, end):
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(heap, (new_distance, neighbor))

    if distances[end] == float("inf"):
        return None, float("inf")

    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path, distances[end]


def prim_mst(graph, start):
    visited = set()
    mst_edges = []
    total_weight = 0

    heap = [(0, start, None)]

    while heap:
        weight, current_node, previous_node = heapq.heappop(heap)

        if current_node in visited:
            continue

        visited.add(current_node)

        if previous_node is not None:
            mst_edges.append((previous_node, current_node, weight))
            total_weight += weight

        for neighbor, edge_weight in graph[current_node].items():
            if neighbor not in visited:
                heapq.heappush(heap, (edge_weight, neighbor, current_node))

    return mst_edges, total_weight