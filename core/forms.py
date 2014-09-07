#-*-coding:utf-8-*-
from django import forms
from core.models import Issue, Comment

class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['project', 'type', 'priority', 'state', 'assignee', 'title', 'description']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

