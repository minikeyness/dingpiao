from django import forms
from django.forms import ModelForm
from mysite.models import Myuser


class RegForm(forms.Form):
        nickName = forms.CharField(error_messages={"required": "必填项"},
                                   max_length=20, label='用户名:', required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
        userEmail = forms.CharField(error_messages={"required": "必填项"},
                                    max_length=20, label='邮箱', required=True,
                                    widget=forms.EmailInput(attrs={'class': 'form-control'}))
        passPwd = forms.CharField(max_length=20, error_messages={"required": "必填项"},
                                  label='密码:', required=True,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        passPwd2 = forms.CharField(max_length=20, error_messages={"required": "必填项"},
                                   label='确认密码:', required=True,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))

        def clean_passPwd2(self):
            pw1 = self.cleaned_data.get("passPwd")
            pw2 = self.cleaned_data.get("passPwd2")
            if pw1 and pw2:
                if pw1 != pw2:
                    msg = u"两个密码不一致。"
                    raise forms.ValidationError(msg)
                    #self._errors["passPwd2"] = self.error_class([msg])
            return pw2


# class RegForm(ModelForm):
#
#     passPwd2 = forms.CharField(max_length=30, required=True)
#
#     def clean(self):
#         cleaned_data = super(RegForm, self).clean()
#         pw1 = cleaned_data.get("passPwd")
#         pw2 = cleaned_data.get("passPwd2")
#         if pw1 and pw2:
#             if pw1 != pw2:
#                 msg = u"两个密码不一致。"
#                 self._errors["passPwd2"] = self.error_class([msg])
#         return cleaned_data
#
#     class Meta:
#         model = Myuser
#         fields = ('nickName', 'userEmail', 'passPwd')

