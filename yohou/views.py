from django.shortcuts import render, redirect
from .forms import Search, NewPost, SignUp, Signin, ChangeLocation
from .models import Post, Advice, WeatherIcon
from django.http import HttpResponseRedirect
import requests
from datetime import datetime
import urllib.request
import pandas as pd
import json
from bs4 import BeautifulSoup
import re
# SignUp
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
def top(request):
    
    # TOPにアクセスした場合はフォームを表示する
    if request.method == 'GET':
        #天気予報API
        default_city_code = '130010'  #東京のcityコード
        url = "https://weather.tsukumijima.net/api/forecast/city/" + default_city_code
        pref_name = '東京都'
        try:
            response = requests.get(url)
            response.raise_for_status()     # ステータスコード200番台以外は例外とする
        except requests.exceptions.RequestException as e:
            print("Error:{}".format(e))
        else:
            weather_json = response.json()
            weather_today = weather_json['forecasts'][0]['telop']
            weather_tomorrow = weather_json['forecasts'][1]['telop']
            weather_day_after_tomorrow = weather_json['forecasts'][2]['telop']
            temperature = weather_json['forecasts'][0]['temperature']['max']['celsius']
            temperature_today_min = weather_json['forecasts'][0]['temperature']['min']['celsius']
            temperature_today_max = weather_json['forecasts'][0]['temperature']['max']['celsius']
            temperature_tomorrow_min = weather_json['forecasts'][1]['temperature']['min']['celsius']
            temperature_tomorrow_max = weather_json['forecasts'][1]['temperature']['max']['celsius']

        if temperature == None:
            temperature = 10
        if temperature_today_min == None:
            temperature_today_min = '-'
        if temperature_today_max == None:
            temperature_today_max = '-'
        if temperature_tomorrow_min == None:
            temperature_tomorrow_min = '-'
        if temperature_tomorrow_max == None:
            temperature_tomorrow_max = '-'

        today = datetime.today()
        season = get_season(today)

        #フォームの初期値
        initial_dict = dict(category = 'WOMEN', temperature = temperature, season = season)

        weather_icon1 = get_weather_icon(weather_today)
        weather_icon2 = get_weather_icon(weather_tomorrow)

        form = Search(initial=initial_dict)

        context = { 
            'form' : form,
            'weather_today' : weather_today,
            'weather_tomorrow' : weather_tomorrow,
            'weather_day_after_tomorrow' : weather_day_after_tomorrow,
            'weather_icon1' : weather_icon1,
            'weather_icon2' : weather_icon2,
            'temperature_today_min' : temperature_today_min,
            'temperature_today_max' : temperature_today_max,
            'temperature_tomorrow_min' : temperature_tomorrow_min,
            'temperature_tomorrow_max' : temperature_tomorrow_max,
            'pref_name' : pref_name
            }
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

        # 気温範囲を取得
        temp_start_range, temp_end_range = get_start_end_temperature(temperature)

        # カテゴリーを数値に変換
        final_category = convert_category(category)

        # 天気を数値に変換
        final_season = convert_season(season)

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

    return render(request, 'search/search_results.html', context)

def search_results(request):
    return render(request, 'search/search_results.html')

def post_detail(request, pk):
    template_name = 'search/post_detail.html'
    try:
        post = Post.objects.get(pk=pk)
        category = convert_category(post.category)
        season = convert_season(post.season)
    except Post.DoesNotExist:
        raise Http404
    context = {
        'post':post,
        'category':category,
        'season':season
    }
    return render(request, template_name, context)

def newpost(request):
    # アクセスした場合はフォームを表示する
    if request.method == 'GET':
        form = NewPost()
        context = { 'form' : form }
        return render(request, 'post/newpost.html', context)
    # フォームが送信された場合
    elif request.method == 'POST':
        form = NewPost(request.POST, request.FILES)
        if not form.is_valid():
            context = { 'form' : form }
            return render(request, 'post/newpost.html', context)
        else:
            form.save()
            form.photo = request.FILES["photo"]
            form.save()
            return render(request, 'post/posted.html')


class SignUp(CreateView):
    form_class = SignUp
    template_name = "accounts/signup.html" 
    success_url = reverse_lazy('top')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url()) # リダイレクト
    
class Login(LoginView):
    form_class = Signin
    template_name = "accounts/signin.html"

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "accounts/signout.html"

def changeLocation(request):
    if request.method == 'GET':
        template_name = "search/change_location.html"
        form = ChangeLocation()
        context = {"form" : form}
        return render(request, template_name, context)
    if request.method == 'POST':
        form = ChangeLocation(request.POST)
        if not form.is_valid():
            template_name = "search/change_location.html"
            context = {'form' : form}
            return render(request, template_name, context)
        else:
            pref = form.cleaned_data["pref"]
            p = str(form.as_p())
            p_location = p.find('selected>')
            start = p_location + 9
            end = start + 3
            selected_pref = p[start:end]
            url = 'https://weather.tsukumijima.net/primary_area.xml'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            res.close()
            all_pref = soup.find_all("pref")
            for i in range(47):
                title = all_pref[i].attrs['title']
                if selected_pref in title:
                    for i, child in enumerate(all_pref[i].children):
                        print(child)
                        if i == 2:
                            city_code = child.attrs['id']
                            pref_name = title
                            break
                else:
                    i += 1


            # with open('resas_api_key.json') as f:
            #         resas_api_key = json.load(f)
            # resas_url1 = 'https://opendata.resas-portal.go.jp/api/v1/prefectures'
            # req = urllib.request.Request(resas_url1, headers=resas_api_key)
            # with urllib.request.urlopen(req) as response:
            #     data = response.read()
            #     d = json.loads(data.decode())
            #     j = pd.json_normalize(d['result'])
            #     s_name = j.set_index('prefName')['prefCode']
            #     pref_code = s_name[selected_pref]

            # resas_url2 = 'https://opendata.resas-portal.go.jp/api/v1/cities?prefCode='+str(pref_code)
            # req = urllib.request.Request(resas_url2, headers=resas_api_key)
            # with urllib.request.urlopen(req) as response:
            #     data = response.read()
            #     d = json.loads(data.decode())
            #     j = pd.json_normalize(d['result'])
            #     city_code = j.iloc[0, 1]

            url = "https://weather.tsukumijima.net/api/forecast/city/" + city_code
            try:
                response = requests.get(url)
                response.raise_for_status()     # ステータスコード200番台以外は例外とする
            except requests.exceptions.RequestException as e:
                print("Error:{}".format(e))
            else:
                weather_json = response.json()
                weather_today = weather_json['forecasts'][0]['telop']
                weather_tomorrow = weather_json['forecasts'][1]['telop']
                weather_day_after_tomorrow = weather_json['forecasts'][2]['telop']
                temperature = weather_json['forecasts'][0]['temperature']['max']['celsius']
                temperature_today_min = weather_json['forecasts'][0]['temperature']['min']['celsius']
                temperature_today_max = weather_json['forecasts'][0]['temperature']['max']['celsius']
                temperature_tomorrow_min = weather_json['forecasts'][1]['temperature']['min']['celsius']
                temperature_tomorrow_max = weather_json['forecasts'][1]['temperature']['max']['celsius']

            if temperature == None:
                temperature = 10
            if temperature_today_min == None:
                temperature_today_min = '-'
            if temperature_today_max == None:
                temperature_today_max = '-'
            if temperature_tomorrow_min == None:
                temperature_tomorrow_min = '-'
            if temperature_tomorrow_max == None:
                temperature_tomorrow_max = '-'

            today = datetime.today()
            season = get_season(today)

            #フォームの初期値
            initial_dict = dict(category = 'WOMEN', temperature = temperature, season = season)

            weather_icon1 = get_weather_icon(weather_today)
            weather_icon2 = get_weather_icon(weather_tomorrow)

            form = Search(initial=initial_dict)

            context = { 
                'form' : form,
                'weather_today' : weather_today,
                'weather_tomorrow' : weather_tomorrow,
                'weather_day_after_tomorrow' : weather_day_after_tomorrow,
                'weather_icon1' : weather_icon1,
                'weather_icon2' : weather_icon2,
                'temperature_today_min' : temperature_today_min,
                'temperature_today_max' : temperature_today_max,
                'temperature_tomorrow_min' : temperature_tomorrow_min,
                'temperature_tomorrow_max' : temperature_tomorrow_max,
                'pref_name' : pref_name
                }
            return render(request, 'top.html', context)
            


def get_start_end_temperature(temperature):
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
        
        return temp_start_range, temp_end_range

def convert_category(category):
        if category == "WOMEN":
            final_category = 1
        elif category == "MEN":
            final_category = 2
        elif category == "KIDS":
            final_category = 3
        elif category == 1:
            final_category = "WOMEN"
        elif category == 2:
            final_category = "MEN"
        elif category == 3:
            final_category = "KIDS"

        return final_category

def convert_season(season):
        if season == "春":
            final_season = 1
        elif season == "夏":
            final_season = 2
        elif season == "秋":
            final_season = 3
        elif season == "冬":
            final_season = 4
        elif season == 1:
            final_season = "春"
        elif season == 2:
            final_season = "夏"
        elif season == 3:
            final_season = "秋"
        elif season == 4:
            final_season = "冬"

        return final_season

def get_season(today):
    month = today.month
    if month == 12 or 1 <= month <= 3:
        season = "冬"
    elif 4 <= month <= 6:
        season = "春"
    elif 7 <= month <= 9:
        season = "夏"
    elif 10 <= month <= 11:
        season = "秋" 

    return season

def get_weather_icon(weather):
    if weather.count('晴') == 1 and weather.count('曇') == 1:
        weather_icon = WeatherIcon.objects.filter(weather="晴曇")
    elif weather.count('晴') == 1:
        weather_icon = WeatherIcon.objects.filter(weather="晴")
    elif weather.count('曇') == 1:
        weather_icon = WeatherIcon.objects.filter(weather="曇")
    elif weather.find('雨'):
        weather_icon = WeatherIcon.objects.filter(weather="雨")
    
    return weather_icon
    
