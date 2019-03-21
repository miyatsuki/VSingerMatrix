# -*- coding: utf-8 -*-

import requests
import csv
import json
from time import sleep

url = 'https://www.googleapis.com/youtube/v3/playlistItems'

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
            singer = row[0]
            playlist_id = row[1]
            param = {
                'key': secrets["youtube_dataAPI_token"]
                , 'playlistId': playlist_id
                , 'part': 'snippet, contentDetails'
                , 'maxResults': '50'
                , 'pageToken': pageToken
            }

            req = requests.get(url, params=param)
            result = req.json()

            for i in range(len(result["items"])):
                song_list.append(singer + "\t" + result["items"][i]["snippet"]["title"] + "\t" + result["items"][i]["contentDetails"]["videoId"])

            print(result)
            sleep(1)

            # 残りのアイテム数がmaxResultsを超えている場合はnextPageTokenが帰ってくる
            if "nextPageToken" in result:
                pageToken = result["nextPageToken"]
            else:
                break

with open('../data/raw_song_list.tsv', "w", encoding='utf-8') as f:
    for i in range(len(song_list)):
        f.write(song_list[i] + "\n")
