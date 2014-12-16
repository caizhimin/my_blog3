#coding:utf8
__author__ = 'cai'

from django import forms


class CzmBlogForm(forms.Form):
    title = forms.CharField(required=True, label='title', max_length=100)
    content = forms.CharField(required=True, widget=forms.Textarea)


class TagForm(forms.Form):
    tag_name = forms.CharField(required=True)
