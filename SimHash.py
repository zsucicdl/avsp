from sys import stdin, stdout
from hashlib import md5
import numpy as np


def simhash(text):
    temparray = np.array([np.unpackbits(np.frombuffer(md5(byteword).digest(), dtype='uint8')) for byteword in
                          text.encode().split(b' ')])
    wordcount = temparray.shape[0]
    a = np.sum(temparray, axis=0, dtype='int16')
    a = 2 * a - wordcount
    a[a >= 0] = 1
    a *= (a > 0)
    return a


def main():
    #file = open('resources/lab1/R11.in', 'r', encoding='ascii')
    n = int(stdin.readline())
    simhashes = np.array([simhash(stdin.readline().rstrip()) for i in range(n)], dtype='uint8')
    q = int(stdin.readline())
    for i in range(q):
        j, k = map(int, stdin.readline().split())
        stdout.write(str(sum((np.count_nonzero(sh != simhashes[j]) <= k for sh in simhashes), -1)) + '\n')


if __name__ == '__main__':
    main()
