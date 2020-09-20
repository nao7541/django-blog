from django.shortcuts import render, redirect
from allauth.account import views

# Create your views here.

# allauthのLoginViewクラスを継承する
class LoginView(views.LoginView):
    # template_nameを指定するだけで簡単にログイン機能が使用できる
    template_name = 'accounts/login.html'