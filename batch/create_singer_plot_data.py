import numpy as np
from sklearn.decomposition import PCA
import csv

song_id_num = 0
with open('../data/song_id.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        song_id_num += 1

singer_id_num = 0
with open('../data/singer_id.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        singer_id_num += 1

mat = np.zeros((singer_id_num, song_id_num))
with open('../data/song_singer_list.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        mat[int(row[1]), int(row[0])] = 1

dist_mat = np.zeros((singer_id_num, singer_id_num))
for i in range(singer_id_num):
    for j in range(singer_id_num):
        if i == j:
            continue

        i_sum = 0
        j_sum = 0
        ij_inner = 0
        for song_id in range(song_id_num):
            ij_inner += mat[i, song_id] * mat[j, song_id]
            i_sum += mat[i, song_id]*mat[i, song_id]
            j_sum += mat[j, song_id]*mat[j, song_id]

        if ij_inner > 0:
            dist_mat[i, j] = 1 - ij_inner/(np.sqrt(i_sum) * np.sqrt(j_sum))
        else:
            dist_mat[i, j] = singer_id_num + 1

for k in range(singer_id_num):
    for i in range(singer_id_num):
        for j in range(singer_id_num):
            if dist_mat[i, j] > (dist_mat[i, k] + dist_mat[k, j]):
                dist_mat[i, j] = dist_mat[i, k] + dist_mat[k, j]
np.savetxt('../data/dist.tsv', dist_mat, delimiter='\t')


print("start pca")
singer_plot = PCA(n_components=2).fit_transform(dist_mat)
print("end pca")
np.savetxt('../data/singer_plot_dist_pca.tsv', singer_plot, delimiter='\t')
