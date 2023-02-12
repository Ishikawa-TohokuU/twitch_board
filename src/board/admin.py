from django.contrib import admin
from .models import StreamModel, StreamerModel, CommentModel #追記

# Register your models here.
admin.site.register(StreamModel) #追記
admin.site.register(StreamerModel)
admin.site.register(CommentModel)