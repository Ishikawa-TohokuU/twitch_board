from django.shortcuts import render
import requests
import json
from requests.structures import CaseInsensitiveDict
from .models import StreamModel #追記
from django.views.generic import ListView

# Create your views here.
def TopView(request):
    template_name = "board/board-top.html"
    return render(request, template_name)

class StreamView(ListView): #クラス作成
    template_name = "board/board-streams.html" #変数
    model = StreamModel #変数
    ordering = '-starttime'
