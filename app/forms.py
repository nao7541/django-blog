from django import forms

class PostForm(forms.Form):
    # 改行を想定しない1行のフォームを作る場合はcharfield
    title = forms.CharField(max_length=30, label="タイトル")
    # 複数行のフォームを想定する場合は引数にwidget=forms.Textarea()を追加
    content = forms.CharField(label="内容", widget=forms.Textarea())
    # 画像をアップロードするフォームを追加
    image = forms.ImageField(label='イメージ画像', required=False)