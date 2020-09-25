from django import forms
from .models import Category

class PostForm(forms.Form):
    # カテゴリのデータを全て取得する
    category_data = Category.objects.all()
    category_choice = {}
    for category in category_data:
        category_choice[category] = category
    # 改行を想定しない1行のフォームを作る場合はcharfield
    title = forms.CharField(max_length=30, label="タイトル")
    # ChoiceFieldを使用して、登録されたカテゴリを選ぶようにする
    category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=list(category_choice.items()))
    # 複数行のフォームを想定する場合は引数にwidget=forms.Textarea()を追加
    content = forms.CharField(label="内容", widget=forms.Textarea())
    # 画像をアップロードするフォームを追加
    image = forms.ImageField(label='イメージ画像', required=False)