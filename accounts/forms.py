from django import forms

class SignupForm(forms.Form):

    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    