from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
from .models import StreamModel #追記
import requests
import json
from requests.structures import CaseInsensitiveDict
from . import settings_board_local

def periodic_execution():# 任意の関数名
    template_name = "board/board-streams.html"

    url_token = 'https://id.twitch.tv/oauth2/token'
    body = {'client_id': settings_board_local.CLIENT_ID,
            'client_secret': settings_board_local.CLIENT_SECRET,
            'grant_type': 'client_credentials',
           }

    req_token = requests.post(url_token, body)
    access_token = req_token.json()['access_token']

    users_list = ['user_login=stylishnoob4&',
                  'user_login=fps_shaka&',
                  'user_login=SPYGEA&',
                  'user_login=alfrea&',
                  'user_login=k4sen&',
                  'user_login=yuyuta0702&',
                  'user_login=sutanmi&',
                  'user_login=rikojoy_',
                  ]

    url = "https://api.twitch.tv/helix/streams?"
    for user in users_list:
        url += str(user)

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer " + access_token
    headers["Client-Id"] = settings_board_local.CLIENT_ID

    resp = requests.get(url, headers=headers)
    streams = resp.json()['data']

    streams_qs = StreamModel.objects.all()
    for stream in streams_qs:
        stream.type = 'offline'
    StreamModel.objects.bulk_update(streams_qs, fields=["type"]) # 一括更新

    stream_list_length = len(streams)
    for stream_idx in range(stream_list_length):
        # stream_titles.append(streams[stream_idx]['title'])
        if not StreamModel.objects.filter(stream_id=streams[stream_idx]['id']):
            obj = StreamModel(
                              stream_id=streams[stream_idx]['id'],
                              title=streams[stream_idx]['title'],
                              streamer_id=streams[stream_idx]['user_id'],
                              streamer=streams[stream_idx]['user_login'],
                              streamer_name=streams[stream_idx]['user_name'],
                              game_name=streams[stream_idx]['game_name'],
                              starttime=streams[stream_idx]['started_at'],
                              type=streams[stream_idx]['type'],
            )
            obj.save()
        else:
            obj_type = StreamModel.objects.get(stream_id=streams[stream_idx]['id'])
            obj_type.type = streams[stream_idx]['type']
            obj_type.save()

    print("10 seconds")

    ctx = {'stream_list_length': stream_list_length}

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'interval', seconds=10)# 1分おきに実行
    scheduler.start()