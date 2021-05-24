from decimal import Decimal, ROUND_HALF_UP
from sys import stdin,stdout
import numpy as np

#file = open('resources/lab3/R31.in', 'r', encoding='ascii')
n, m = map(int, stdin.buffer.readline().split())
user_item_matrix = np.genfromtxt((stdin.buffer.readline() for i in range(n)), missing_values='X', filling_values=0)

mask = user_item_matrix > 0

i_norm = np.transpose(user_item_matrix) - np.average(user_item_matrix, weights=mask, axis=1)
i_norm = np.transpose(i_norm) * mask

u_norm = user_item_matrix - np.average(user_item_matrix, weights=mask, axis=0)
u_norm = np.transpose(u_norm * mask)

corr_item = np.corrcoef(i_norm)
corr_user = np.corrcoef(u_norm)
np.fill_diagonal(corr_item, 0)
np.fill_diagonal(corr_user, 0)

q = int(stdin.buffer.readline())
for z in range(q):
    i, j, t, k = map(int, stdin.buffer.readline().split())
    i -= 1
    j -= 1

    ui_query = np.copy(user_item_matrix[:, j]) if t == 0 else np.copy(user_item_matrix[i])
    corrs_query = np.copy(corr_item[i]) if t == 0 else np.copy(corr_user[j])
    corrs_query[ui_query == 0] = 0
    sor = np.sort(corrs_query)

    threshold = sor[corrs_query.shape[0] - k]
    corrs_query[corrs_query < max(0, threshold)] = 0

    s = np.sum(corrs_query)
    d = np.dot(corrs_query, ui_query)
    stdout.write(str(Decimal(Decimal(d / s).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))) + '\n')
