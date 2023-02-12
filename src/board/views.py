from django.shortcuts import render, redirect
import requests
import json
from requests.structures import CaseInsensitiveDict
from .models import StreamModel, StreamerModel, CommentModel #追記
from .forms import StreamFormClass
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView
import time

# Create your views here.
def TopView(request):
    template_name = "board/board-top.html"
    return render(request, template_name)

class StreamView(ListView): #クラス作成
    template_name = "board/board-streams.html" #変数
    model = StreamModel #変数
    ordering = '-viewer_count'

    def get_queryset(self):
        # qs = NippoModel.objects.none()
        qs = StreamModel.objects.filter(type='live')
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        return ctx
    
    def get_queryset(self):
        try:
            q = self.request.GET["search"]
        except:
            q = None
        return StreamModel.objects.search(query=q)

class ArchiveView(ListView): #クラス作成
    template_name = "board/board-archives.html" #変数
    model = StreamModel #変数
    ordering = '-starttime'

    def get_queryset(self):
        # qs = NippoModel.objects.none()
        qs = StreamModel.objects.filter(type='offline')
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        return ctx
    
    def get_queryset(self):
        try:
            q = self.request.GET["search"]
        except:
            q = None
        return StreamModel.objects.search(query=q)

class StreamerView(ListView): #クラス作成
    template_name = "board/board-streamers.html" #変数
    model = StreamerModel #変数
    ordering = '-id'

    # if StreamerModel.objects.filter(type=''):
    #     time.sleep(1)

    def get_queryset(self):
        # qs = NippoModel.objects.none()
        qs = StreamerModel.objects.all()
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        return ctx
    
    def get_queryset(self):
        try:
            q = self.request.GET["search"]
        except:
            q = None
        return StreamerModel.objects.search(query=q)
    

class StreamDetailView(DetailView):
    template_name = "board/board-detail.html"
    model = StreamModel

    def get_object(self):
        return super().get_object()

class CommentCreateFormView(FormView):
    template_name = "board/board-commentform.html"
    form_class = StreamFormClass
    # success_url = "/nippo/" #redirectみたいな。送信後どこに行くか
    def get_success_url(self, **kwargs):
        return reverse_lazy("board-detail", kwargs={"pk":self.kwargs["pk"]}) #処理を待ってreverseする。メソッドの中ならreverseでもOK
   
    def form_valid(self, form):
        data = form.cleaned_data #辞書型でformを受け取る
        obj = CommentModel(**data) #forms.pyとmodels.pyの"content"が同じ名前だからこれで展開できる
        obj.save()
        return super().form_valid(form)

class StreamerDetailView(DetailView):
    template_name = "board/board-streamersdetail.html"
    model = StreamerModel

    def get_object(self):
        return super().get_object()

