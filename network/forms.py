from django import forms


class SearchForm(forms.Form):
    username = forms.CharField(max_length=255, label='username', required=False)
    first_name = forms.CharField(max_length=255, label='first name', required=False)
    last_name = forms.CharField(max_length=255, label='last name', required=False)