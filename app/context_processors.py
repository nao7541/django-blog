from .models import Category

"""
コンテキストプロセッサーとは
変数をビューからテンプレートに渡さなくても、テンプレート上で変数を使えるようにする
色々なところに表示させたいときに便利
"""

# カテゴリデータを全て取得して、そのデータをreturnで返す
def common(request):
    category_data = Category.objects.all()
    context = {
        'category_data': category_data
    }
    return context