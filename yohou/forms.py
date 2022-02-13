from django import forms

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