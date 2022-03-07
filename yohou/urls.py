from django.urls import path
from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('search_results', views.search_results, name="search_results"),
    path('newpost', views.newpost, name="newpost"),
    path('posted', views.newpost, name="posted"),
    path('signup', views.SignUp.as_view(), name="signup"),
    path('signin', views.Login.as_view(), name="login"),
    path('signout', views.Logout.as_view(), name="logout"),
    
]