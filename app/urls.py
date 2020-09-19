from django.urls import path
from app import views

# トップページviewのIndexView関数を割り当てる
"""
as_viewメソッドは、クラス汎用ビューを関数化する
具体的には、IndexViewはクラス汎用ビューといい、Djangoが用意した関数を継承して作る
そのため、クラス汎用ビューを使用する際は必須となる

nameにはルーティングの名前を付けており、これをすることで、名前からurlを逆引きすることができる
"""
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # pkには投稿のIDが入るため、どの投稿の詳細画面かがわかる
    path('post/<int:pk>', views.PostDetailView.as_view(), name="post_detail"),
    path("post/new/", views.CreatePostView.as_view(), name="post_new")
]
