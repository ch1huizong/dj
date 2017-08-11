# -*- coding:UTF-8 -*-
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# 本质是form的构造函数
class RegistrationForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=30)
    email = forms.EmailField(label="邮箱")
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label="再一次输入", widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd['password1']
        password2 = cd['password2']
        if password1 == password2:
            return password2
        else:
            raise forms.ValidationError('密码不匹配')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('用户名需要是字母,数字,下划线')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('用户名已经存在')

class BookmarkForm(forms.Form):
    url = forms.URLField(label='URL',
            widget=forms.TextInput(attrs={'size':64}))
    title = forms.CharField(label='标题',
            widget=forms.TextInput(attrs={'size':64}))
    tags = forms.CharField(label='标签',
            required=False,
            widget=forms.TextInput(attrs={'size':64}))
