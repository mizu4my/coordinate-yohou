from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from localflavor.jp.forms import JP_PREFECTURES

class Search(forms.Form):
    category = forms.fields.ChoiceField(
        choices = (
            ('WOMEN', 'WOMEN'),
            ('MEN', 'MEN'),
            ('KIDS', 'KIDS'),
        ),
        required=True,
    )

    temperature = forms.IntegerField(
        required = True
    )

    season = forms.fields.ChoiceField(
        choices = (
            ('春', '春'),
            ('夏', '夏'),
            ('秋', '秋'),
            ('冬', '冬'),
        ),
        required=True
    )

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'username', 'category', 'temperature', 'season', 'text', 'photo'}
        labels = {
            'username':'ユーザー名', 
            'category':'カテゴリー',
            'temperature':'写真撮影日の気温',
            'season':'写真撮影日の季節',
            'text':'コメント',
            'photo':'写真',
            }

class ChangeLocation(forms.Form):
    pref = forms.ChoiceField(choices=JP_PREFECTURES, initial='tokyo')

class SignUp(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class Signin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
