from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2'] 
class BookSearch(forms.Form):
    

    #    search = forms.CharField( label="Search for a book", required=False, widget=forms.TextInput(attrs={'class': "input"}))   
      search= forms.CharField(
        label="Search for a book", required=False, widget=forms.TextInput(attrs={'class': "field__input", 'id': 'search', 'autofocus': True}))