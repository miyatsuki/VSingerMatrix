# -*- coding: utf-8 -*-

import csv
import jaconv
import unicodedata
import sys

song_title_list = []
with open('../data/song_title.txt', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        song_title_list.append(row[0])

rename_video_list = []
with open('../data/rename_video.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        if len(row) >= 3:
            # from singer to
            rename_video_list.append([row[0], row[1], row[2]])
        else:
            rename_video_list.append([row[0], row[1], None])

check_video_list = []
with open('../data/raw_song_list.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        check_video_list.append([row[0], row[1], row[2]])

prefix_punctuations = [" ", "【", "】", "》", "「", "『", "“", "/", "-", "、"]
suffix_punctuations = [" ", "【", "】",  "(", "/", "」", "『", "』", "”", "/"]

accept_singer_song_list = []
reject_singer_song_list = []
for row in check_video_list:
    singer = row[0]
    title = unicodedata.normalize("NFKC", row[1])
    video_id = row[2]
    title = jaconv.z2h(title, kana=False, digit=True, ascii=True).lower()

    if title == "private video" or title == "deleted video":
        continue

    for rename in rename_video_list:
        if title == rename[0] and singer == rename[1]:
            if rename[2] is not None:
                title = rename[2]
            else:
                title = None

    if title is None:
        continue

    candidate_title = ""
    candidate_title_no_punct = ""
    for test_title in song_title_list:
        if test_title in title and len(test_title) > len(candidate_title):

            if len(test_title) > len(candidate_title_no_punct):
                candidate_title_no_punct = test_title

            if title == test_title:
                candidate_title = test_title
                continue

            is_split_by_punctuations = False
            for punct_prefix in prefix_punctuations:
                for punct_suffix in suffix_punctuations:
                    if punct_prefix + test_title + punct_suffix in title:
                        is_split_by_punctuations = True
                        break

            if not is_split_by_punctuations:
                for punct_prefix in prefix_punctuations:
                    if title.endswith(punct_prefix + test_title):
                        is_split_by_punctuations = True
                        break

            if not is_split_by_punctuations:
                for punct_suffix in suffix_punctuations:
                    if title.startswith(test_title + punct_suffix):
                        is_split_by_punctuations = True
                        break

            if is_split_by_punctuations:
                candidate_title = test_title

    if candidate_title != "":
        accept_singer_song_list.append(singer + "\t" + title + "\t" + candidate_title  + "\t" + video_id)
    else:
        reject_singer_song_list.append((title + "\t" + singer + "\t" + candidate_title_no_punct).strip())


with open('../data/song_list.tsv', "w", encoding='utf-8') as f:
    for line in accept_singer_song_list:
        f.write(line + "\n")

with open('../data/reject_song_list.tsv', "w", encoding='utf-8') as f:
    for line in reject_singer_song_list:
        f.write(line + "\n")

print("reject list num: " + str(len(reject_singer_song_list)))
