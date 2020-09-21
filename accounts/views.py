from django.shortcuts import render, redirect
from allauth.account import views

# Create your views here.

# allauthのLoginViewクラスを継承する
class LoginView(views.LoginView):
    # template_nameを指定するだけで簡単にログイン機能が使用できる
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # self.logout()でログアウトすることが可能
            self.logout()
        return redirect('/')

# allauthのSighupViewクラスを継承する
class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'