# Distributed under the terms of the GNU General Public License v2
from django import forms
from core.models import *

class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['project', 'type', 'priority', 'state', 'assignee', 'title', 'description']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
