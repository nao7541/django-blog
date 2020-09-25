from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
# 投稿機能のモデルを作成

class Post(models.Model):
    # ForeignKeyを利用してログインしているユーザーに紐づける
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    # 画像フィールドを追加
    # upload_toで画像のアップロード先を指定
    image = models.ImageField(upload_to='images', verbose_name="イメージ画像", null=True, blank=True)
    content = models.TextField("本文")
    created = models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):
        return self.title