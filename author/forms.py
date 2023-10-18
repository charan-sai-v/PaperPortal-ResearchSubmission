from django import forms


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)



