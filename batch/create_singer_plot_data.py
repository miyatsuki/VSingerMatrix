import numpy as np
from sklearn.decomposition import PCA
import csv

song_list = []
singer_list = []

singer_song_map = {}
singer_song_videoId_map = {}
with open('../data/filtered_song_list.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        singer = row[0]
        song = row[2]
        videoId = row[3]

        if singer not in singer_list:
            singer_list.append(singer)
            singer_song_map[singer] = []
            singer_song_videoId_map[singer] = {}

        if song not in song_list:
            song_list.append(song)

        singer_song_map[singer].append(song)
        singer_song_videoId_map[singer][song] = videoId

mat = np.zeros((len(singer_list), len(song_list)))
for singer in singer_song_map:
    singer_id = singer_list.index(singer)

    for song in singer_song_map[singer]:
        song_id = song_list.index(song)
        mat[singer_id, song_id] = 1


dist_mat = np.zeros((len(singer_list), len(singer_list)))
for i in range(len(singer_list)):
    for j in range(len(singer_list)):
        if i == j:
            continue

        i_sum = 0
        j_sum = 0
        ij_inner = 0
        for song_id in range(len(song_list)):
            ij_inner += mat[i, song_id] * mat[j, song_id]
            i_sum += mat[i, song_id]*mat[i, song_id]
            j_sum += mat[j, song_id]*mat[j, song_id]

        if ij_inner > 0:
            dist_mat[i, j] = 1 - ij_inner/(np.sqrt(i_sum) * np.sqrt(j_sum))
        else:
            dist_mat[i, j] = len(singer_list) + 1

for k in range(len(singer_list)):
    for i in range(len(singer_list)):
        for j in range(len(singer_list)):
            if dist_mat[i, j] > (dist_mat[i, k] + dist_mat[k, j]):
                dist_mat[i, j] = dist_mat[i, k] + dist_mat[k, j]
np.savetxt('../data/dist.tsv', dist_mat, delimiter='\t')


print("start pca")
singer_plot = PCA(n_components=2).fit_transform(dist_mat)
print("end pca")

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

        f.write("{" + 'singer_id:' + str(i)
                + ', name:"' + singer_list[i]
                + '", posX:' + str(singer_plot[i, 0]*scale)
                + ", posY:" + str(singer_plot[i, 1]*scale)
                + ", song:" + song_list_string +"}")
        if i < len(singer_list) - 1:
            f.write(",\n")
        else:
            f.write("]")
    
    f.write("\n\n")

    # video_id情報
    f.write("videoId_map = {\n")
    singer_count = 0
    for singer in singer_song_videoId_map:
        f.write('"' + singer + '" : {')

        song_count = 0
        for song in singer_song_videoId_map[singer]:
            f.write('"' + song + '":"' + singer_song_videoId_map[singer][song] + '"')
            song_count += 1
            if song_count < len(singer_song_videoId_map[singer]):
                f.write(',') 
        
        f.write('}')
        singer_count += 1
        if singer_count < len(singer_song_videoId_map):
            f.write(',\n')
        else:
            f.write("}")
