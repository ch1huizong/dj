# -*- coding:UTF-8 -*-

from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(label='姓名', max_length=25)
    email = forms.EmailField(label='来自于')
    to = forms.EmailField(label='发送至')
    comments = forms.CharField(label='评论',required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
