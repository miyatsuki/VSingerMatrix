import numpy as np
from sklearn.decomposition import PCA
import csv

song_id_num = 0
song_list = []
with open('../data/song_id.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        song_id_num += 1
        song_list.append(row[1])

singer_id_num = 0
singer_list = []
with open('../data/singer_id.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        singer_id_num += 1
        singer_list.append(row[1])

mat = np.zeros((singer_id_num, song_id_num))
singer_song_map = {}
with open('../data/song_singer_list.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        mat[int(row[1]), int(row[0])] = 1

        singer_string = singer_list[int(row[1])]
        song_string = song_list[int(row[0])]

        if singer_string not in singer_song_map:
            singer_song_map[singer_string] = []
        singer_song_map[singer_string].append(song_string)

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

abs_max = 0
for row in singer_plot:
    for i in range(len(row)):
        if abs(row[i]) > abs_max:
            abs_max = abs(row[i])
scale = 0.9/abs_max

with open('../data/plot_data.js', "w", encoding='utf-8') as f:
    f.write("plot_data = [" + "\n")
    for i in range(len(singer_list)):
        
        song_list_string = '["' + '","'.join(singer_song_map[singer_list[i]]) + '"]'

        f.write("{" + 'name:"' + singer_list[i] 
                +'", posX:' + str(singer_plot[i, 0]*scale) 
                + ", posY:" + str(singer_plot[i, 1]*scale) 
                + ", song:" + song_list_string +"}")
        if i < len(singer_list) - 1:
            f.write(",\n")
        else:
            f.write("]")
