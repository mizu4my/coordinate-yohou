from django.urls import path
from . import views
from django.views.generic import FormView
from . import forms

urlpatterns = [
    path('', views.top, name='top'),
    path('search_results', views.search_results, name="search_results"),
    path('newpost', views.newpost, name="newpost"),
    path('posted', views.newpost, name="posted"),
    path('signup', views.SignUp.as_view(), name="signup"),
    path('signin', views.Login.as_view(), name="login"),
    path('signout', views.Logout.as_view(), name="logout"),
    path('search_results/<int:pk>/',views.post_detail,name="post_detail"),
    path('change_location', views.changeLocation, name="change_location") 
]