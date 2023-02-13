from django.db import models
from django.contrib.auth import get_user, get_user_model
from django.db.models import Q #インポート

CustomUser = get_user_model() # AUTH_USER_MODELで指定したモデル

class StreamModelQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        # qs = qs.filter(public=True) #公開済みの日報のみでQuerySetを作成しています
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)|
                Q(streamer__icontains=query)|
                Q(streamer_name__icontains=query)            
            )
            qs = qs.filter(or_lookup).distinct()
        return qs.order_by("-viewer_count", "-starttime") #新しい順に並び替えてます

class StreamModelManager(models.Manager):
    def get_queryset(self):
        return StreamModelQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

# Create your models here.
class StreamModel(models.Model):
    stream_id = models.IntegerField(unique=True, verbose_name="配信id")
    title = models.CharField(max_length=100, verbose_name="配信タイトル")
    streamer_id = models.IntegerField(verbose_name="配信者id")
    streamer = models.CharField(max_length=100, verbose_name="配信者")
    streamer_name = models.CharField(max_length=100, verbose_name="配信者名")
    game_name = models.CharField(max_length=100, verbose_name="ゲーム名")
    # public = models.BooleanField(default=False, verbose_name="公開する")
    starttime = models.DateTimeField()
    type = models.CharField(default='offline', max_length=100, verbose_name="状態")
    viewer_count = models.IntegerField(default=0, verbose_name="視聴者数")

    class Meta:
        verbose_name_plural = "Board" #StreamModels から Board へ

    objects = StreamModelManager()

    def __str__(self):
        return self.streamer_name + ' | ' + self.title





class StreamerModelQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        # qs = qs.filter(public=True) #公開済みの日報のみでQuerySetを作成しています
        if query is not None:
            or_lookup = (
                Q(streamer__icontains=query)|
                Q(streamer_name__icontains=query)            
            )
            qs = qs.filter(or_lookup).distinct()
        return qs.order_by("type", "streamer") 


class StreamerModelManager(models.Manager):
    def get_queryset(self):
        return StreamerModelQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class StreamerModel(models.Model):
    streamer_id = models.IntegerField(unique=True, verbose_name="配信者id")
    streamer = models.CharField(max_length=100, verbose_name="配信者")
    streamer_name = models.CharField(max_length=100, verbose_name="配信者名")
    # public = models.BooleanField(default=False, verbose_name="公開する")
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(default='offline', max_length=100, verbose_name="状態")
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "ストリーマー" #StreamModels から Board へ

    objects = StreamerModelManager()

    def __str__(self):
        return self.streamer_name + ' (' + str(self.streamer) + ')'


class CommentModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="ユーザー名")
    stream_id =  models.IntegerField(null=True, blank=True, verbose_name="配信id")
    streamer_id = models.IntegerField(null=True, blank=True, verbose_name="ストリーマーid")
    content = models.CharField(max_length=400, verbose_name="投稿内容")
    id_for_stream = models.IntegerField(null=True, blank=True, verbose_name="配信毎のid")
    # public = models.BooleanField(default=False, verbose_name="公開する")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Comment" #CommentModels から Comment へ

    def __str__(self):
        return self.content + " @" + str(self.user) + ' to ' + str(self.streamer_id)