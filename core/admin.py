# Distributed under the terms of the GNU General Public License v2
from django.contrib import admin
from core.models import *

class IssueAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class IssueTypeAdmin(admin.ModelAdmin):
    pass

class IssueStateAdmin(admin.ModelAdmin):
    pass

class IssuePriorityAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(IssueType, IssueTypeAdmin)
admin.site.register(IssueState, IssueStateAdmin)
admin.site.register(IssuePriority, IssuePriorityAdmin)
admin.site.register(Project, ProjectAdmin)
