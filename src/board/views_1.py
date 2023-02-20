from django.shortcuts import render, redirect
import requests
import json
from requests.structures import CaseInsensitiveDict
from .models import StreamModel, StreamerModel, CommentModel #追記
from .forms import StreamFormClass
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
        obj_stream = StreamModel.objects.filter(type='live')
        stream_count = obj_stream.count()
        print(stream_count)
        obj_streamer = StreamerModel.objects.none()
        for stream in obj_stream:
            comment_num = CommentModel.objects.filter(stream_id=stream.stream_id).count()
            # print('stream_id=', stream.stream_id)
            # print(CommentModel.objects.get(stream_id=stream.stream_id))
            # obj_comment = CommentModel.objects.get(stream_id=stream.stream_id)
            print(type(comment_num))
            print(stream.comment_count)
            stream.comment_count = comment_num
            stream.save()
            # streamer = StreamerModel.objects.get(streamer_id=stream.streamer_id)
            # obj_streamer = obj_streamer.union(streamer, all=True)
        # print(obj_streamer)
        ctx["streamer"] = obj_streamer
        # ctx["comment"] = obj_comment
        print(type(obj_streamer))
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
        obj_stream = StreamModel.objects.filter(type='offline')
        for stream in obj_stream:
            comment_num = CommentModel.objects.filter(stream_id=stream.stream_id).count()
            # print('stream_id=', stream.stream_id)
            # print(CommentModel.objects.get(stream_id=stream.stream_id))
            # obj_comment = CommentModel.objects.get(stream_id=stream.stream_id)
            # print(type(comment_num))
            # print(stream.comment_count)
            stream.comment_count = comment_num
            stream.save()
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
    

# class StreamDetailView(DetailView):
#     template_name = "board/board-detail.html"
#     model = StreamModel
#     model_comment = CommentModel

#     def get_object(self):
#         return super().get_object()

def StreamDetailView(request, **kwargs):
    obj_stream = StreamModel.objects.get(pk=kwargs["pk"])
    obj_comment = CommentModel.objects.filter(stream_id=obj_stream.stream_id).order_by('-created_at')
    comment_count = obj_comment.count()
    # print('count=', comment_count)
    # print(obj_comment[0])
    context = {}
    context["stream"] = obj_stream
    context["comment_list"] = obj_comment
    context["comment_count"] = comment_count
    return render(request, 'board/board-detail.html', context)

#class CommentCreateFormView(LoginRequiredMixin, FormView):    
class CommentCreateFormView(FormView):
    template_name = "board/board-commentform.html"
    form_class = StreamFormClass
    # success_url = "/nippo/" #redirectみたいな。送信後どこに行くか
    def get_success_url(self, **kwargs):
        return reverse_lazy("board-detail", kwargs={"pk":self.kwargs["pk"]}) #処理を待ってreverseする。メソッドの中ならreverseでもOK
   
    # def get_form_kwargs(self, *args, **kwargs):
    #     kwgs = super().get_form_kwargs(*args, **kwargs)
    #     kwgs["user"] = self.request.user
    #     return kwgs

    def form_valid(self, form):
        data = form.cleaned_data #辞書型でformを受け取る
        obj = CommentModel(**data) #forms.pyとmodels.pyの"content"が同じ名前だからこれで展開できる
        obj_stream = StreamModel.objects.get(pk=self.kwargs["pk"])
        # obj_streamer = StreamerModel.objects.filter(streamer_id=obj_stream.streamer_id)
        # obj["user"] = self.request.user
        print(obj_stream, obj_stream.stream_id)
        obj.user = self.request.user
        obj.stream_id = obj_stream.stream_id
        obj.streamer_id = obj_stream.streamer_id
        obj.save()
        return super().form_valid(form)

# class StreamerDetailView(DetailView):
#     template_name = "board/board-streamersdetail.html"
#     model = StreamerModel
#     obj_user_comment = CommentModel.objects.filter()

#     def get_object(self):
#         return super().get_object()

def StreamerDetailView(request, **kwargs):
    obj_streamer = StreamerModel.objects.get(pk=kwargs["pk"])
    obj_comment = CommentModel.objects.filter(streamer_id=obj_streamer.streamer_id).order_by('-created_at')
    obj_stream = StreamModel.objects.filter(streamer_id=obj_streamer.streamer_id).order_by('-starttime')
    comment_count = obj_comment.count()
    # print('count=', comment_count)
    # print(obj_comment[0])
    context = {}
    context["streamer"] = obj_streamer
    context["comment_list"] = obj_comment
    context["stream_list"] = obj_stream
    context["comment_count"] = comment_count
    return render(request, 'board/board-streamersdetail.html', context)