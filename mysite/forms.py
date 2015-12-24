from django import forms
from django.forms import ModelForm
from mysite.models import Myuser


class RegForm(ModelForm):
    passPwd2 = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Myuser
        fields = ('nickName', 'userEmail', 'passPwd')

