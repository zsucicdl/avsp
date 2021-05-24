from sys import stdin,stdout


def main():
    #stdin. = open('resources/lab4/R4B5.in', 'r', encoding='utf-8')
    lines = stdin.readlines()
    stdin.close()
    n, e = map(int, lines[0].split())

    t_list = [int(line) for line in lines[1:n + 1]]
    edge_list = [[int(x) for x in line.split()] for line in lines[n + 1:n + 1 + e]]
    adjacency_list = [[] for i in range(n)]

    dist_index = [[0, i] if t_list[i] else [-1, -1] for i in range(n)]

    for source, destination in edge_list:
        adjacency_list[source].append(destination)
        adjacency_list[destination].append(source)

    for iteration in range(10):
        for i in range(n):
            current_distance = dist_index[i][0]+1
            current_distance_index = dist_index[i][1]
            if current_distance == 0:
                continue
            for neighbour in adjacency_list[i]:
                if dist_index[neighbour][0] == -1 or dist_index[neighbour][0] > current_distance:
                    dist_index[neighbour] = [current_distance, current_distance_index]
                if dist_index[neighbour][0] == current_distance and current_distance_index < dist_index[neighbour][1]:
                    dist_index[neighbour][1] = current_distance_index

    for dist, index in dist_index:
        stdout.write(str(index) + " " + str(dist) + '\n')


if __name__ == '__main__':
    main()
