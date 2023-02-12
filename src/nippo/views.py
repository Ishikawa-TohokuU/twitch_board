from django.shortcuts import render, get_object_or_404, redirect
from random import randint
from .models import NippoModel
from .forms import NippoModelForm, NippoFormClass
from django.views.generic import ListView, DetailView, FormView #インポート
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

class OwnerOnly(UserPassesTestMixin):
    # アクセス制限を行う関数
    def test_func(self):
        nippo_instance = self.get_object()
        # print(nippo_instance.user)
        return nippo_instance.user == self.request.user
    
    # Falseだったときのリダイレクト先を指定
    def handle_no_permission(self):
        messages.error(self.request, "ご自身の日報でのみ編集・削除可能です。")
        return redirect("nippo-detail", pk=self.kwargs["pk"])

class NippoListView(ListView): #クラス作成
    template_name = "nippo/nippo-list.html" #変数
    model = NippoModel #変数

    def get_queryset(self):
        # qs = NippoModel.objects.none()
        qs = NippoModel.objects.all()
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["myname"] = "後藤ひとり"
        return ctx
    
    def get_queryset(self):
        try:
            q = self.request.GET["search"]
        except:
            q = None
        return NippoModel.objects.search(query=q)

def nippoListView(request):
    template_name = "nippo/nippo-list.html"
    ctx = {}
    qs = NippoModel.objects.all()
    ctx["object_list"] = qs

    return render(request, template_name, ctx)

class NippoDetailView(DetailView):
    template_name = "nippo/nippo-detail.html"
    model = NippoModel

    def get_object(self):
        return super().get_object()

def nippoDetailView(request, pk):
     template_name = "nippo/nippo-detail.html"
     ctx = {}
    #  q = NippoModel.objects.get(pk=pk)
     q = get_object_or_404(NippoModel, pk=pk)
     ctx["object"] = q
     return render(request, template_name, ctx)

# def nippoCreateView(request):
#     template_name = "nippo/nippo-form.html"
#     title = request.GET.get("title")
#     content = request.GET.get("content")
#     print(title)
#     return render(request, template_name)

class NippoCreateFormView(FormView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoFormClass
    # success_url = "/nippo/" #redirectみたいな。送信後どこに行くか
    success_url = reverse_lazy("nippo-list") #処理を待ってreverseする。メソッドの中ならreverseでもOK
   
    def form_valid(self, form):
        data = form.cleaned_data #辞書型でformを受け取る
        obj = NippoModel(**data) #forms.pyとmodels.pyの"title"と"content"が同じ名前だからこれで展開できる
        obj.save()
        return super().form_valid(form)


class NippoCreateModelFormView(LoginRequiredMixin, CreateView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoModelForm
    success_url = reverse_lazy("nippo-list")

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        kwgs["user"] = self.request.user
        return kwgs
# nippoCreateViewでいうvalid関数が無くとも保存までできる

def nippoCreateView(request):
    template_name="nippo/nippo-form.html"
    form = NippoFormClass(request.POST or None) # どちらかが入る
    ctx = {}
    ctx["form"] = form
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = NippoModel(title=title, content=content)
        obj.save()
        return redirect("nippo-list")
    return render(request, template_name, ctx)

class NippoUpdateModelFormView(OwnerOnly, UpdateView):
    template_name = "nippo/nippo-form.html"
    model = NippoModel
    form_class = NippoModelForm
    success_url = reverse_lazy("nippo-list")


class NippoDeleteView(OwnerOnly, DeleteView):
    template_name = "nippo/nippo-delete.html"
    model = NippoModel
    success_url = reverse_lazy("nippo-list")

def nippoUpdateFormView(request, pk):
    template_name = "nippo/nippo-form.html"
    # obj = NippoModel.objects.get(pk=pk)
    obj = get_object_or_404(NippoModel, pk=pk)
    initial_values = {"title": obj.title, "content":obj.content}
    form = NippoFormClass(request.POST or initial_values)
    ctx = {"form": form}
    ctx["object"] = obj
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
        if request.POST:
            return redirect("nippo-list")
    return render(request, template_name, ctx)

def nippoDeleteView(request, pk):
    template_name = "nippo/nippo-delete.html"
    obj = get_object_or_404(NippoModel, pk=pk)
    ctx = {"object": obj}
    if request.POST:
        obj.delete()
        return redirect("nippo-list")
    return render(request, template_name, ctx)




import requests
import json
from requests.structures import CaseInsensitiveDict

def TwitchApi(request):
    template_name = "nippo/nippo-twitchapi.html"

    users_list = ['user_login=alfrea&',
                  'user_login=k4sen&',
                  'user_login=rikojoy_',
                 ]

    url = "https://api.twitch.tv/helix/streams?"
    user_url = "https://api.twitch.tv/helix/users?login=k4sen"

    # url = "https://api.twitch.tv/helix/streams?user_login=fps_shaka"
    for user in users_list:
        url += str(user)

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer "
    headers["Client-Id"] = ""

    resp = requests.get(url, headers=headers)
    user_resp = requests.get(user_url, headers=headers)

    # json_response = resp.json()['data'][0]['from_id']
    streams = resp.json()['data']
    print(streams)

    # streams = resp.json()['data'][0]['title']
    # print(streams)

    stream_list_length = len(streams)

    stream_titles = []
    for stream_idx in range(stream_list_length):
        stream_titles.append(streams[stream_idx]['title'])

    users = user_resp.json()['data']
    print(users)

    ctx = {'stream_list_length': stream_list_length, 'title': stream_titles}
    return render(request, template_name, ctx)

