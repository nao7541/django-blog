from django.shortcuts import render
from django.views.generic import View
from .models import Post

# Create your views here.

# Viewを継承して、クラス汎用ビューを作成
class IndexView(View):
    # get関数は、画面が表示されたら必ず最初に呼ばれる
    def get(self, request, *args, **kwargs):
        # postモデルを呼び出し、降順に並べ替える
        post_data = Post.objects.order_by("-id")
        # render関数を使用して、テンプレートにデータを渡す
        return render(request, 'app/index.html', {
            'post_data': post_data,
        })