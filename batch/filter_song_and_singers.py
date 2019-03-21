# -*- coding: utf-8 -*-

import csv
import sys

raw_song_list = []
raw_singer_list = []
raw_song_singer_map = {}
with open('../data/song_list.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')

    for row in tsv:
        song = row[2].strip()
        singer = row[0].strip()
        print(row)

        if song not in raw_song_list:
            raw_song_list.append(song)

        if song not in raw_song_singer_map:
            raw_song_singer_map[song] = []

        if singer not in raw_singer_list:
            raw_singer_list.append(singer)

        if singer not in raw_song_singer_map[song]:
            raw_song_singer_map[song].append(singer)

song_list = []
for song in raw_song_singer_map:
    if len(raw_song_singer_map[song]) >= 3:
        song_list.append(song)


singer_list = []
for singer in raw_singer_list:

    cnt = 0
    for song in song_list:
        if singer in raw_song_singer_map[song]:
            cnt += 1

    if cnt >= 3:
        singer_list.append(singer)
        continue


song_singer_map = {}
for song in song_list:
    song_singer_map[song] = []

    for singer in raw_song_singer_map[song]:
        if singer in singer_list:
            song_singer_map[song].append(singer)

with open('../data/song_list.tsv', "r", encoding='utf-8') as fr:
    with open('../data/filtered_song_list.tsv', "w", encoding='utf-8') as fw:

        tsv = csv.reader(fr, delimiter='\t')
        for row in tsv:
            singer = row[0].strip()
            title = row[1].strip()
            song = row[2].strip()
            video_id = row[3].strip()
            write_row = [singer, title, song, video_id]

            if song not in song_singer_map:
                continue
            
            if singer not in song_singer_map[song]:
                continue
            fw.write("\t".join(write_row) + "\n")
