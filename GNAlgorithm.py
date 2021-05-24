from decimal import Decimal, ROUND_HALF_UP
from sys import stdin, stdout


def find_paths(initial_path, edge_weights, all_paths):
    end = initial_path[-1]
    for node1, node2 in edge_weights:
        if node1 == end or node2 == end:
            edge_exists = False
            l=len(initial_path)
            if l> 1:
                for i in range(1, l):
                    if (initial_path[i - 1] == node1 and initial_path[i] == node2) or (
                            initial_path[i - 1] == node2 and initial_path[i] == node1):
                        edge_exists = True

            if not edge_exists:
                new_path = initial_path.copy()
                new_path.append(node1 if end == node2 else node2)
                all_paths.append(new_path)
                find_paths(new_path, edge_weights, all_paths)


def filter_paths(all_paths, edge_weights, nodes_list):
    grouped_paths = {tuple((node1, node2)): [] for node1 in nodes_list for node2 in nodes_list}
    for path in all_paths:
        # if path[0]==path[-1]:
        #     continue

        filtered_from_removal = False
        l=len(path)
        length = 0
        for e in zip(path[0:l-1],path[1:l]):
            if e not in edge_weights:
                e = tuple((e[1],e[0]))
            if e not in edge_weights:
                filtered_from_removal = True
                break
            length += edge_weights[e]

        # for i in range(1, l):
        #     if path[i - 1] != path[i]:
        #         e = tuple((path[i - 1], path[i]))
        #         if e not in edge_weights:
        #             e = tuple((path[i], path[i - 1]))
        #         if e not in edge_weights:
        #             filtered_from_removal = True
        #             break
        #         length += edge_weights[e]
        if not filtered_from_removal:
            grouped_paths[(path[0], path[-1])].append([length, path])
    return grouped_paths


def calculate_betweenness(grouped_paths, edge_betweenness):
    for edge in grouped_paths:
        paths = sorted(grouped_paths[edge])
        if edge[0] == edge[1] or len(paths) == 0:
            continue
        mind = paths[0][0]
        shortest_paths = []
        for d, path in paths:
            if d > mind:
                break
            shortest_paths.append(path.copy())
        if edge[0] == edge[1]:
            shortest_paths = [[edge[0], edge[0]]]

        factor = len(shortest_paths)
        l=len(path)
        for path in shortest_paths:
            for e in zip(path[0:l - 1], path[1:l]):
                if e not in edge_betweenness:
                    e = tuple((e[1], e[0]))
                edge_betweenness[e] += 1 / factor

            # for i in range(1, len(path)):
            #     if path[i - 1] != path[i]:
            #         e = tuple((path[i - 1], path[i]))
            #         if e not in edge_betweenness:
            #             e = tuple((path[i], path[i - 1]))
            #         edge_betweenness[e] += 1 / factor


def get_edges_with_highest_betweenness(edge_betweenness):
    max_cent = -1
    edges_to_remove = []
    for k, v in sorted(edge_betweenness.items(), key=lambda item: item[1], reverse=True):
        if max_cent > v:
            break
        edges_to_remove.append(tuple(sorted(k)))
        max_cent = v
    return sorted(edges_to_remove)


def find_communities(edge_weights, neighbours_lists):
    visited = set()
    communities = []
    for node in neighbours_lists:
        if node not in visited:
            community = find_community(node, neighbours_lists, visited)
            communities.append(community)

    return communities


def find_community(root, neighbours_lists, visited):
    community = [root]
    visited.add(root)
    next_queue = [root]
    while next_queue:
        node = next_queue.pop(0)
        for child in neighbours_lists[node]:
            if child not in visited:
                next_queue.append(child)
                community.append(child)
                visited.add(child)
    return community


def calculate_modularity(communities, ks, edge_weights):
    modularity = 0.0
    m = 0
    for val in edge_weights.values():
        m += val
    for community in communities:
        modularity += calculate_q(community, ks, edge_weights, m)
    return modularity / (2.0 * m)


def calculate_q(community, ks, edge_weights, m):
    res = 0.0
    for node1 in community:
        for node2 in community:
            pair = tuple([node1, node2])
            pair2 = tuple([node2, node1])
            if pair in edge_weights:
                a_i_j = edge_weights[pair]
            elif pair2 in edge_weights:
                a_i_j = edge_weights[pair2]
            else:
                a_i_j = 0

            ku = ks[node1]
            kv = ks[node2]
            res += a_i_j - (ku * kv) / (2.0 * m)
    return res


def sort_communities(communities):
    for com in communities:
        com.sort()
    communities.sort()
    communities.sort(key=len)


def main():
    #file = open('resources/lab5/R51.in', 'r', encoding='utf-8')
    #s = stdin
    lines = stdin.readlines()
    stdin.close()
    n_edges = 0
    n = 0
    for line in lines:
        if line in ['\n', '\r\n']:
            break
        n_edges += 1

    edge_list = {tuple((int(line.split()[0]), int(line.split()[1]))): 0 for line in lines[0:n_edges]}

    node_vectors = {}
    n_nodes = 0
    for line in lines[n_edges + 1:]:
        n_nodes += 1
        vec = [int(x) for x in line.split()]
        node = vec[0]
        vec = vec[1:]
        node_vectors[node] = vec
    nodes_list = list(node_vectors.keys())

    edge_weights = dict.fromkeys(edge_list, n_nodes)

    for edge in edge_weights:
        arr1 = node_vectors[edge[0]]
        arr2 = node_vectors[edge[1]]
        count = 0
        for i in range(len(arr1)):
            if arr1[i] == arr2[i]:
                count += 1
        edge_weights[edge] = len(arr1) + 1 - count

    all_paths = []
    for node in nodes_list:
        find_paths([node], edge_list, all_paths)
    highest_modularity = -1.0
    optimal_communities = []

    while len(edge_weights) > 0:
        grouped_paths = filter_paths(all_paths, edge_weights, nodes_list)
        edge_betweenness = dict.fromkeys(edge_weights, 0)
        calculate_betweenness(grouped_paths, edge_betweenness)

        neighbours_lists = {node: set() for node in nodes_list}
        for source, destination in edge_weights:
            neighbours_lists[source].add(destination)
            neighbours_lists[destination].add(source)
        ks = dict.fromkeys(nodes_list, 0)
        for node in neighbours_lists:
            for neighbour in neighbours_lists[node]:
                pair = tuple([node, neighbour])
                pair2 = tuple([neighbour, node])
                if pair in edge_weights:
                    ks[node] += edge_weights[pair]
                elif pair2 in edge_weights:
                    ks[node] += edge_weights[pair2]

        communities = find_communities(edge_weights, neighbours_lists)
        modularity = calculate_modularity(communities, ks, edge_weights)
        if modularity > highest_modularity:
            highest_modularity = modularity
            optimal_communities = communities
        if modularity < 0:
            modularity *= -1
        #stdout.write("MODULARITY " + str(
        #    Decimal(Decimal(modularity).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))) + '\n')

        edges_to_remove = get_edges_with_highest_betweenness(edge_betweenness)
        for edge in edges_to_remove:
            print(str(min(edge[0], edge[1])) + ' ' + str(max(edge[0], edge[1])))
            if edge in edge_weights:
                del edge_weights[edge]
            else:
                del edge_weights[tuple((edge[1],edge[0]))]

    sort_communities(optimal_communities)
    for community in optimal_communities:
        stdout.write("-".join([str(user) for user in community])+" ")


if __name__ == '__main__':
    main()
