from django.db import models
from django.contrib.auth import get_user, get_user_model

User = get_user_model() # AUTH_USER_MODELで指定したモデル

# Create your models here.
class StreamModel(models.Model):
    stream_id = models.IntegerField(unique=True, verbose_name="配信id")
    title = models.CharField(max_length=100, verbose_name="配信タイトル")
    streamer_id = models.CharField(max_length=100, verbose_name="配信者id")
    streamer = models.CharField(max_length=100, verbose_name="配信者")
    streamer_name = models.CharField(max_length=100, verbose_name="配信者名")
    game_name = models.CharField(max_length=100, verbose_name="ゲーム名")
    # public = models.BooleanField(default=False, verbose_name="公開する")
    starttime = models.DateTimeField()
    type = models.CharField(default='offline', max_length=100, verbose_name="状態")

    class Meta:
        verbose_name_plural = "Board" #StreamModels から Board へ

    def __str__(self):
        return self.streamer_name + ' | ' + self.title

# class CommentModel(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, verbose_name="ユーザー名")
#     # public = models.BooleanField(default=False, verbose_name="公開する")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "Comment" #CommentModels から Comment へ

#     def __str__(self):
#         return self.title + " @" + self.name