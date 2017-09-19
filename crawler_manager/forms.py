from django import forms

class ScapperForm(forms.Form):
    city_name = forms.CharField(label='City Name', max_length=100, required=True)
    keyword = forms.CharField(label='Search Keyword', max_length=50)
