from django.contrib import admin
from .models import Post
# Register your models here.

# admin.site.registerの引数にモデルを指定することで管理画面からデータベースを操作できるようにする
admin.site.register(Post)