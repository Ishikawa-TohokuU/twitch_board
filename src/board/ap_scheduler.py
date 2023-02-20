from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
from .models import StreamModel, StreamerModel #追記
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

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer " + access_token
    headers["Client-Id"] = settings_board_local.CLIENT_ID

    login_list = ['login=stylishnoob4&',
                  'login=fps_shaka&',
                  'login=SPYGEA&',
                  'login=kato_junichi0817&'
                  'login=k4sen&'
                  'login=jasper7se&',
                  'login=darumaisgod&',
                  'login=sasatikk&',
                  'login=raderaderader&',
                  'login=dmf_kyochan&',
                  'login=yukiofps14&',
                  'login=Euriece&',
                  'login=MOTHER3rd&',
                  'login=vodkavdk&',
                  'login=dasoku_aniki&',
                  'login=sutanmi&',
                  'login=yuyuta0702&',
                  'login=akarindao&',
                  'login=gutitubo&',
                  'login=alfrea&',
                  'login=clutch_fii&',
                  'login=syaruru3&',
                  'login=oniyadayo&',
                  'login=Lazvell&',
                  'login=Anzu_o0',
                  ]
            
    url_streamer = "https://api.twitch.tv/helix/users?"
    for user in login_list:
        url_streamer += str(user)

    resp_streamer = requests.get(url_streamer, headers=headers)
    streamers = resp_streamer.json()['data']

    streamer_list_length = len(streamers)
    for streamer_idx in range(streamer_list_length):
        if not StreamerModel.objects.filter(streamer_id=streamers[streamer_idx]['id']): # 配信者のデータがまだ存在しない場合(配信開始直後)
            obj_streamer = StreamerModel(
                                streamer_id=streamers[streamer_idx]['id'],
                                streamer=streamers[streamer_idx]['login'],
                                streamer_name=streamers[streamer_idx]['display_name'],
                                type='offline',
                                image=streamers[streamer_idx]['profile_image_url'],
                                channel='https://www.twitch.tv/'+str(streamers[streamer_idx]['login']),
            )
            obj_streamer.save()
        else:
            obj_streamer_update = StreamerModel.objects.get(streamer_id=streamers[streamer_idx]['id'])
            obj_streamer_update.streamer = streamers[streamer_idx]['login']
            obj_streamer_update.streamer_name = streamers[streamer_idx]['display_name']
            obj_streamer_update.type = 'offline'
            obj_streamer_update.image = streamers[streamer_idx]['profile_image_url']
            obj_streamer_update.channel='https://www.twitch.tv/'+str(streamers[streamer_idx]['login'])
            obj_streamer_update.save()

    users_list = ['user_login=stylishnoob4&',
                  'user_login=fps_shaka&',
                  'user_login=SPYGEA&',
                  'user_login=kato_junichi0817&'
                  'user_login=k4sen&'
                  'user_login=jasper7se&',
                  'user_login=darumaisgod&',
                  'user_login=sasatikk&',
                  'user_login=raderaderader&',
                  'user_login=dmf_kyochan&',
                  'user_login=yukiofps14&',
                  'user_login=Euriece&',
                  'user_login=MOTHER3rd&',
                  'user_login=vodkavdk&',
                  'user_login=dasoku_aniki&',
                  'user_login=sutanmi&',
                  'user_login=yuyuta0702&',
                  'user_login=akarindao&',
                  'user_login=gutitubo&',
                  'user_login=alfrea&',
                  'user_login=clutch_fii&',
                  'user_login=syaruru3&',
                  'user_login=oniyadayo&',
                  'user_login=Lazvell&',
                  'user_login=Anzu_o0',
                  ]

    url = "https://api.twitch.tv/helix/streams?"
    for user in users_list:
        url += str(user)

    resp = requests.get(url, headers=headers)
    streams = resp.json()['data']

    streams_qs = StreamModel.objects.all()
    for stream in streams_qs:
        stream.type = 'offline'
        stream.viewer_count = 0
    
    streamers_qs = StreamModel.objects.all()
    for streamer in streamers_qs:
        streamer.type = 'offline'

    StreamModel.objects.bulk_update(streams_qs, fields=["type"])
    StreamModel.objects.bulk_update(streams_qs, fields=["viewer_count"]) 
    StreamerModel.objects.bulk_update(streams_qs, fields=["type"]) # 一括更新

    stream_list_length = len(streams)
    for stream_idx in range(stream_list_length):
        # stream_titles.append(streams[stream_idx]['title'])
        if not StreamModel.objects.filter(stream_id=streams[stream_idx]['id']): # 配信のデータがまだ存在しない場合(配信開始直後)
            print(type(streams[stream_idx]['viewer_count']))
            obj = StreamModel(
                              stream_id=streams[stream_idx]['id'],
                              title=streams[stream_idx]['title'],
                              streamer_id=streams[stream_idx]['user_id'],
                              streamer=streams[stream_idx]['user_login'],
                              streamer_name=streams[stream_idx]['user_name'],
                              game_name=streams[stream_idx]['game_name'],
                              starttime=streams[stream_idx]['started_at'],
                              type=streams[stream_idx]['type'],
                              viewer_count=int(streams[stream_idx]['viewer_count']),
                              thumbnail = streams[stream_idx]['thumbnail_url'].replace('{width}', '440').replace('{height}', '228')
            )
            obj.save()
            if not StreamerModel.objects.filter(streamer_id=streams[stream_idx]['user_id']): # 配信者のデータがまだ存在しない場合
                obj_streamer = StreamerModel(
                                streamer_id=streams[stream_idx]['user_id'],
                                streamer=streams[stream_idx]['user_login'],
                                streamer_name=streams[stream_idx]['user_name'],
                                type=streams[stream_idx]['type'],
                )
                obj_streamer.save()
        else:
            obj_type = StreamModel.objects.get(stream_id=streams[stream_idx]['id'])
            obj_type.title=streams[stream_idx]['title']
            obj_type.game_name=streams[stream_idx]['game_name']
            obj_type.type = streams[stream_idx]['type']
            obj_type.viewer_count = int(streams[stream_idx]['viewer_count'])
            obj_type.thumbnail = streams[stream_idx]['thumbnail_url'].replace('{width}', '440').replace('{height}', '228')
            obj_type.save()

            obj_streamer_type = StreamerModel.objects.get(streamer_id=streams[stream_idx]['user_id'])
            obj_streamer_type.type = streams[stream_idx]['type']
            obj_streamer_type.save()


    print('access_token = ', access_token)
    print("1 minute")

    ctx = {'stream_list_length': stream_list_length}

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'interval', seconds=60)# 1分おきに実行
    scheduler.start()