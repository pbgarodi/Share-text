
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Message

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            
            'password1':None,
            'password2':None
        }


class Share_Text_Form(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=False)
    encrypt = forms.BooleanField(required = False)
    

    class Meta:
        model = Message
        fields = ('message',)

class Share_Text_Decryption_key_Form(forms.ModelForm):
    decryption_key = forms.CharField(required=True)  
    class Meta:
      model = Message
      fields = ('decryption_key',)  