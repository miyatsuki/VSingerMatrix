import numpy as np
import csv
from sklearn import manifold
import math


raw_song_list = []
raw_singer_list = []

raw_singer_song_map = {}
singer_song_videoId_map = {}
singer_song_viewCount_map = {}

song_count_map = {}
with open('../data/song_list.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        singer = row[0]
        song = row[2]
        videoId = row[3]
        view_count = int(row[4])

        if singer not in raw_singer_list:
            raw_singer_list.append(singer)
            raw_singer_song_map[singer] = []
            singer_song_videoId_map[singer] = {}
            singer_song_viewCount_map[singer] = {}

        if song not in raw_song_list:
            raw_song_list.append(song)
        
        if song not in song_count_map:
            song_count_map[song] = 0

        raw_singer_song_map[singer].append(song)
        singer_song_videoId_map[singer][song] = videoId
        singer_song_viewCount_map[singer][song] = view_count
        song_count_map[song] += 1


song_list = []
singer_list = []
singer_num_threashold = 1

singer_song_map = {}
for singer in raw_singer_song_map:
    singer_song_map[singer] = {}
    singer_song_map[singer]["include"] = []
    singer_song_map[singer]["exclude"] = []

    for song in raw_singer_song_map[singer]:
        if song_count_map[song] >= singer_num_threashold:
            singer_song_map[singer]["include"].append(song)
            if song not in song_list:
                song_list.append(song)
        else:
            singer_song_map[singer]["exclude"].append(song)
    
    if len(singer_song_map[singer]["include"]) > 0:
        singer_list.append(singer)


mat = np.zeros((len(singer_list), len(song_list)))
for singer in singer_song_map:
    singer_id = singer_list.index(singer)

    for song in singer_song_map[singer]["include"]:
        song_id = song_list.index(song)
        mat[singer_id, song_id] = math.log10(singer_song_viewCount_map[singer][song])


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

print("start magnetic simulation")
mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
singer_plot = mds.fit_transform(dist_mat)
print("end magnetic simulation")

for row in singer_plot:
    for i in range(len(row)):
        row[i] = np.sign(row[i]) * np.sqrt(np.abs(row[i]))

abs_max = 0
for row in singer_plot:
    for i in range(len(row)):
        if abs(row[i]) > abs_max:
            abs_max = abs(row[i])
scale = 0.9/abs_max

with open('../view/plot_data.js', "w", encoding='utf-8') as f:
    f.write("plot_data = [" + "\n")
    for i in range(len(singer_list)):
        
        song_list_string = '["' + '","'.join(singer_song_map[singer_list[i]]["include"]) + '"]'

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

    f.write("\n\n")
    # distmat
    f.write("dist_mat = [")
    row_count = 0
    for row in dist_mat:
        f.write('[')
        f.write(','.join(map(str, row.tolist())))
        f.write(']')

        
        row_count += 1
        if row_count < len(dist_mat):
            f.write(',\n')
        else:
            f.write("]")

    f.write("\n\n")
    # song_id_list
    f.write("song_list = [\"")
    f.write('","'.join(map(str, raw_song_list)))
    f.write('"]')