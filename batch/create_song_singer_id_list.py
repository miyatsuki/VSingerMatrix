# -*- coding: utf-8 -*-

import csv
import sys

raw_song_list = []
raw_singer_list = []
main_singer_list = []
raw_song_singer_map = {}
with open('../data/song_list.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')

    for row in tsv:
        # コラボ曲等の無視するやつはtitleカラム未記入
        if len(row) < 3 or row[2] == "":
            continue

        song = row[2].strip()
        singers = [row[0].strip()]
        main_singer_list.append(row[0].strip())
        print(row)

        # コラボを考慮するときはコメントを外す
        #for i in range(3, len(row)):
        #    singers.append(row[i].strip())

        if song not in raw_song_list:
            raw_song_list.append(song)

        if song not in raw_song_singer_map:
            raw_song_singer_map[song] = []

        for singer in singers:
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
    if singer not in main_singer_list:
        continue

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

print(raw_song_list)
print(raw_singer_list)
print(raw_song_singer_map)
print(song_list)
print(singer_list)
print(song_singer_map)

with open('../data/song_id.tsv', "w", encoding='utf-8') as f:
    for i in range(len(song_list)):
        f.write(str(i) + "\t" + song_list[i] + "\n")

with open('../data/singer_id.tsv', "w", encoding='utf-8') as f:
    for i in range(len(singer_list)):
        f.write(str(i) + "\t" + singer_list[i] + "\n")

with open('../data/song_singer_list.tsv', "w", encoding='utf-8') as f:
    for song in song_singer_map:
        song_id = song_list.index(song)

        for singer in song_singer_map[song]:
            singer_id = singer_list.index(singer)
            f.write(str(song_id) + "\t" + str(singer_id) + "\n")
