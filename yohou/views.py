from django.shortcuts import render
from .forms import Search
from .models import Post

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

        temp_start_range = temperature-2
        temp_end_range = temperature+2

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

        
        posts = Post.objects.filter(
            category=final_category, 
            temperature__range=(temp_start_range, temp_end_range),
            season = final_season
            )
        

        for post in posts:
            resized_photo = post.photo


        #import pdb; pdb.set_trace()
        context = {
            'category' : category,
            'season' : season,
            'temp_start_range' : temp_start_range,
            'temp_end_range' : temp_end_range,
            'posts' : posts,
        }


    return render(request, 'search_results.html', context)

def search_results(request):
    return render(request, 'search_results.html')
