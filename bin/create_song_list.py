# -*- coding: utf-8 -*-

import csv
import jaconv
import unicodedata
import sys

raw_song_title_list = []
normalize_song_title_list = []
with open('../data/song_title.txt', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')
    for row in tsv:
        title = row[0]
        raw_song_title_list.append(title)

        title = unicodedata.normalize("NFKC", title)
        title = jaconv.z2h(title, kana=False, digit=True, ascii=True).lower()
        normalize_song_title_list.append(title)

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
        check_video_list.append([row[0], row[1], row[2], row[3]])

prefix_punctuations = [" ", "【", "】", "》", "「", "『", "“", "/", "-", "、"]
suffix_punctuations = [" ", "【", "】",  "(", "/", "」", "『", "』", "”", "-", "歌ってみた"]

accept_singer_song_list = []
reject_singer_song_list = []
for row in check_video_list:
    singer = row[0]
    raw_title = row[1]
    title = unicodedata.normalize("NFKC", raw_title)
    video_id = row[2]
    view_count = row[3]
    title = jaconv.z2h(title, kana=False, digit=True, ascii=True).lower()

    if title == "private video" or title == "deleted video":
        continue

    for rename in rename_video_list:
        if raw_title == rename[0] and singer == rename[1]:
            if rename[2] is not None:
                title = rename[2]
                title = unicodedata.normalize("NFKC", title)
                title = jaconv.z2h(title, kana=False, digit=True, ascii=True).lower()
            else:
                title = None
            break

    if title is None:
        continue

    candidate_title = ""
    candidate_title_no_punct = ""

    for i in range(len(raw_song_title_list)):

        raw_test_title = raw_song_title_list[i]
        normalize_test_title = normalize_song_title_list[i]

        if normalize_test_title in title and len(normalize_test_title) > len(candidate_title):

            if len(normalize_test_title) > len(candidate_title_no_punct):
                candidate_title_no_punct = raw_test_title

            if title == normalize_test_title:
                candidate_title = raw_test_title
                continue

            is_split_by_punctuations = False
            for punct_prefix in prefix_punctuations:
                for punct_suffix in suffix_punctuations:
                    if punct_prefix + normalize_test_title + punct_suffix in title:
                        is_split_by_punctuations = True
                        break

            if not is_split_by_punctuations:
                for punct_prefix in prefix_punctuations:
                    if title.endswith(punct_prefix + normalize_test_title):
                        is_split_by_punctuations = True
                        break

            if not is_split_by_punctuations:
                for punct_suffix in suffix_punctuations:
                    if title.startswith(normalize_test_title + punct_suffix):
                        is_split_by_punctuations = True
                        break

            if is_split_by_punctuations:
                candidate_title = raw_test_title

    if candidate_title != "":
        accept_singer_song_list.append(singer + "\t" + raw_title + "\t" + candidate_title  + "\t" + video_id + "\t" + view_count)
    else:
        reject_singer_song_list.append((raw_title + "\t" + singer + "\t" + candidate_title_no_punct).strip())


with open('../data/song_list.tsv', "w", encoding='utf-8') as f:
    for line in accept_singer_song_list:
        f.write(line + "\n")

with open('../data/reject_song_list.tsv', "w", encoding='utf-8') as f:
    for line in reject_singer_song_list:
        f.write(line + "\n")

print("reject list num: " + str(len(reject_singer_song_list)))
