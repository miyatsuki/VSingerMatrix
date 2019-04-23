# -*- coding: utf-8 -*-

import requests
import csv
import json
from time import sleep


playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
video_url = 'https://www.googleapis.com/youtube/v3/videos'

# this file is not shared with github
# create own secrets.json like
#{
#    "youtube_dataAPI_token": "YOUR API TOKEN"
#}
with open('../secrets.json', "r") as f:
    secrets = json.load(f)

with open('../data/playlist.tsv', "r", encoding='utf-8') as f:
    tsv = csv.reader(f, delimiter='\t')

    song_list = []
    for row in tsv:
        pageToken = ""
        while True:
            print("\n")
            singer = row[0]
            playlist_id = row[1]
            param = {
                'key': secrets["youtube_dataAPI_token"]
                , 'playlistId': playlist_id
                , 'part': 'snippet, contentDetails'
                , 'maxResults': '50'
                , 'pageToken': pageToken
            }

            req = requests.get(playlist_url, params=param)
            playlist_result = req.json()

            id_list = []
            for i in range(len(playlist_result["items"])):
                id_list.append(playlist_result["items"][i]["contentDetails"]["videoId"])

            sleep(1)

            param = {
                'key': secrets["youtube_dataAPI_token"]
                , 'part': 'snippet,statistics'
                , 'id': ','.join(id_list)
            }

            req = requests.get(video_url, params=param)
            video_result = req.json()

            for i in range(len(video_result["items"])):
                print(video_result["items"][i])
                if "statistics" in video_result["items"][i]:
                    data = [singer, video_result["items"][i]["snippet"]["title"], video_result["items"][i]["id"], video_result["items"][i]["statistics"]["viewCount"]]
                    song_list.append("\t".join(data))

            sleep(1)

            # 残りのアイテム数がmaxResultsを超えている場合はnextPageTokenが帰ってくる
            if "nextPageToken" in playlist_result:
                pageToken = playlist_result["nextPageToken"]
            else:
                break


with open('../data/raw_song_list.tsv', "w", encoding='utf-8') as f:
    for i in range(len(song_list)):
        f.write(song_list[i] + "\n")
