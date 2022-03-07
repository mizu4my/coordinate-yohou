from django.shortcuts import render, redirect
from .forms import Search, NewPost, SignUp, Signin
from .models import Post, Advice
from django.http import HttpResponseRedirect
# SignUp
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
def top(request):
    
    # TOPにアクセスした場合はフォームを表示する
    if request.method == 'GET':
        form = Search()
        context = { 'form' : form }
        return render(request, 'top.html', context)
    
    # 検索条件を入力した場合は検索結果を表示する
    elif request.method == 'POST':
        form = Search(request.POST)
        if not form.is_valid():
            context = { 'form' : form }
            return render(request, 'top.html', context)
        
        category = form.cleaned_data["category"]
        temperature = form.cleaned_data["temperature"]
        season = form.cleaned_data["season"]

        # 気温の範囲を判定
        if -5 <= temperature <= 0 :
            temp_start_range = -5
            temp_end_range = 0
        elif 1 <= temperature <= 5 :
            temp_start_range = 1
            temp_end_range = 5
        elif 1 <= temperature <= 5 :
            temp_start_range = 1
            temp_end_range = 5
        elif 6 <= temperature <= 10 :
            temp_start_range = 6
            temp_end_range = 10
        elif 11 <= temperature <= 15 :
            temp_start_range = 11
            temp_end_range = 15
        elif 16 <= temperature <= 20 :
            temp_start_range = 16
            temp_end_range = 20
        elif 21 <= temperature <= 25 :
            temp_start_range = 21
            temp_end_range = 25
        elif 26 <= temperature <= 30 :
            temp_start_range = 26
            temp_end_range = 30
        elif 31 <= temperature <= 35 :
            temp_start_range =31
            temp_end_range = 35
        elif 36 <= temperature <= 40 :
            temp_start_range = 36
            temp_end_range = 40

        # カテゴリーを数値に変換
        if category == "WOMEN":
            final_category = 1
        elif category == "MEN":
            final_category = 2
        elif category == "KIDS":
            final_category = 3

        # 天気を数値に変換
        if season == "春":
            final_season = 1
        elif season == "夏":
            final_season = 2
        elif season == "秋":
            final_season = 3
        elif season == "冬":
            final_season = 4


        #import pdb; pdb.set_trace()
        # アドバイスの取得
        advice = Advice.objects.filter(
            category=final_category,
            start_temp=temp_start_range,
            end_temp=temp_end_range,
            season=final_season
        )

        # 投稿データの取得
        posts = Post.objects.filter(
            category=final_category, 
            temperature__range=(temp_start_range, temp_end_range),
            season = final_season
            )

        context = {
            'category' : category,
            'season' : season,
            'temp_start_range' : temp_start_range,
            'temp_end_range' : temp_end_range,
            'advice' : advice,
            'posts' : posts,
        }

    return render(request, 'search_results.html', context)

def search_results(request):
    return render(request, 'search_results.html')

def newpost(request):
    # アクセスした場合はフォームを表示する
    if request.method == 'GET':
        form = NewPost()
        context = { 'form' : form }
        return render(request, 'newpost.html', context)
    # フォームが送信された場合
    elif request.method == 'POST':
        form = NewPost(request.POST, request.FILES)
        if not form.is_valid():
            context = { 'form' : form }
            return render(request, 'newpost.html', context)
        else:
            form.save()
            form.photo = request.FILES["photo"]
            form.save()
            return render(request, 'posted.html')

# class SignIn(LoginView):
#     form_class = SignUp
#     template_name = "signin.html" 

# class SignOut(LoginRequiredMixin, LogoutView):
#     template_name = 'top.html'

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get['username']
#             raw_password = form.cleaned_data.get['password1']
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('')
#         else:
#             form = UserCreationForm()
#             context = {'form':form}
#         return render(request, 'signin.html', context)

class SignUp(CreateView):
    form_class = SignUp
    template_name = "signup.html" 
    success_url = reverse_lazy('top')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url()) # リダイレクト
    

# class Login(View):
#     def post(self, request, *arg, **kwargs):
#         form = SignIn(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             user = User.objects.get(username=username)
#             login(request, user)
#             return redirect('/')
#         context = {'form': form,}
#         return render(request, 'signin.html', context)

#     def get(self, request, *args, **kwargs):
#         form = SignIn(request.POST)
#         context = {'form': form,}
#         return render(request, 'signin.html', context)

# account_login = Login.as_view()

class Login(LoginView):
    form_class = Signin
    template_name = "signin.html"

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "signout.html"

