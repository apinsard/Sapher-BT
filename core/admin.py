from django.contrib import admin
from core.models import Issue, Comment

class IssueAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
