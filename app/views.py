from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Q
from functools import reduce
from operator import and_
from .models import Post, Category
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

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

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        # self.kwargs['pk']でURLのIDを取得することができる
        post_data = Post.objects.get(id=self.kwargs['pk'])
        # 取得したデータをテンプレートに渡す
        return render(request, 'app/post_detail.html', {
            'post_data': post_data
        })

class CreatePostView(LoginRequiredMixin, View):
    # PostFormからフォームデータを取得し、テンプレートに渡す
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        return render(request, 'app/post_form.html', {
            'form': form
        })

    # 送信ボタンを押したときにpost関数がコールされる
    def post(self, request, *args, **kwargs):
        # PostFormからフォームデータを取得し、バリデーションを行う
        form = PostForm(request.POST or None)

        if form.is_valid():
            # 入力されたフォームデータを取得して、新規データとしてデータベースに書き込む
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data["title"]
            # フォームからカテゴリのデータを取得して、post_data.categoryにデータを登録
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data["content"]
            # 画像アップロード用
            # フォームから画像を取得する方法はrequest.FILESを使用
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            # 送信後はリダイレクトして詳細画面に遷移する
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form':form
        })

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            # initialオプションを使うことでフォームに初期データを表示
            initial = {
                'title': post_data.title,
                'category': post_data.category,
                'content': post_data.content,
                # 画像の初期データは他のデータと同様に指定する
                'image': post_data.image,
            }
        )

        return render(request, 'app/post_form.html', {
            'form': form
        })

    # 新規投稿と同様に編集画面で投稿ボタンを押すとpost関数が呼ばれる
    # データをバリデーションして、フォームの内容をデータベースに書き込む
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['title']
            category_data = Category.objects.get(name=category)
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/post_form.html', {
            'form': form
        })

class PostDeleteView(LoginRequiredMixin, View):
    # 削除ボタンをクリックしたら、削除確認画面に進むようにする
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        # deleteを使うことでデータベースからデータを削除できる
        post_data.delete()
        return redirect('index')

# urlからカテゴリの名前を取得して投稿データにフィルターをかける
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'app/index.html', {
            'post_data': post_data
        })

# 検索用のビューを追加
class SearchView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            # 全角と半角の空文字列を除外する
            exclusion_list = set([' ','　'])
            quety_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    quety_list += word
            # reduce関数は、関数内関数を扱うことができる
            # and_は第二引数に、リスト内包表記で[keyword]をひとつずつQオブジェクトに与えている
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in quety_list])
            # 東湖データをフィルターにかけてデータを取得する
            post_data = post_data.filter(query)

        return render(request, 'app/index.html', {
            'keyword': keyword,
            'post_data': post_data,
        })