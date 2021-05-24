import numpy as np
from scipy.sparse import csr_matrix
from sys import stdin

def main():
    #file = open('resources/lab4/R4A1.in', 'r', encoding='utf-8')
    lines = stdin.readlines()
    stdin.close()
    n, beta = map(float, lines[0].split())
    n = round(n)

    rows = []
    columns = []
    data = []

    for i, line in enumerate(lines[1:n + 1]):
        a = [int(x) for x in line.split()]
        length = len(a)
        columns.extend(a)
        rows.extend([i] * length)
        val = beta / length
        data.extend([val] * length)

    adjacency_matrix = csr_matrix((data, (rows, columns)), shape=(n, n))

    # q = int(lines[n + 1].rstrip())
    queries = [[int(x) for x in line.split()] for line in lines[n + 2:]]

    rs = np.full(shape=(101, n), fill_value=(1 - beta) / n)
    rs[0] = np.full(shape=n, fill_value=1 / n)

    for iteration in range(1, 101):
        rs[iteration] += rs[iteration - 1] * adjacency_matrix

    for q1, q2 in queries:
        print('%.10f' % rs[q2][q1])


if __name__ == '__main__':
    main()
