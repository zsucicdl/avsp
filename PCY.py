from sys import stdin, stdout
import numpy as np
from itertools import combinations


def main():
    #file = open('resources/lab2/R22.in', 'r', encoding='utf-8')
    n = int(stdin.readline())
    s = float(stdin.readline())
    b = int(stdin.readline())
    threshold = (n * s) // 1

    item_count = np.zeros(1000)
    baskets = [[int(x) for x in stdin.readline().split()] for i in range(n)]

    for i in range(n):
        for num in baskets[i]:
            item_count[num] += 1

    item_num = np.count_nonzero(item_count)
    item_count = item_count >= threshold
    # items = set(item for basket in baskets for item in basket)
    item_num_za_ap = np.count_nonzero(item_count)
    buckets = [0] * b
    pairs = {}
    # combos=combinations(items, 2)
    # pairs = {pair: 0 for pair in combinations(items, 2)}
    # pair_hashes = {pair: (((pair[0] * item_num) + pair[1]) % b) for pair in combinations(items, 2)}
    pair_hashes = {}

    for i in range(n):
        for (item1, item2) in combinations(baskets[i], 2):
            if item_count[item1] and item_count[item2]:
                k = (item1 * item_num + item2) % b
                buckets[k] += 1
                pair_hashes[(item1, item2)] = k
                if (item1, item2) in pairs:
                    pairs[(item1, item2)] += 1
                else:
                    pairs[(item1, item2)] = 1

    pairs_new = {}
    for (item1, item2) in pairs:
        if buckets[pair_hashes[(item1, item2)]] >= threshold:
            pairs_new[(item1, item2)] = pairs[(item1, item2)]

    pairs_counter = sorted(pairs_new.values(), reverse=True)

    A = item_num_za_ap * (item_num_za_ap - 1) // 2
    stdout.write(str(A) + '\n')
    stdout.write(str(len(pairs_counter)) + '\n')
    for x in pairs_counter:
        if x >= threshold:
            stdout.write(str(x) + '\n')


if __name__ == '__main__':
    main()
