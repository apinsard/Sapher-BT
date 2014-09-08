#-*-coding:utf-8-*-
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator

CSS_CLASS_HELP_TEXT = 'Predefined styles are "default" (gray), "primary" (blue), '\
    + '"success" (green), "info" (cyan), "warning" (orange) and "danger" (red). '\
    + 'You can also create your own in your stylesheet.'

class IssueType(models.Model):

    class Meta:
        verbose_name = "type"
        verbose_name_plural = "types"
        ordering = ['id']

    filter_name = 'type'

    id = models.PositiveSmallIntegerField(
        verbose_name = 'ID',
        primary_key  = True,
        validators   = [MaxValueValidator(31)],
        help_text    = "This ID will be used by `UserSettings.type_filters` as 2^(ID).",
    )

    name = models.CharField(
        verbose_name = "name",
        unique       = True,
        max_length   = 50,
    )

    css_class = models.CharField(
        verbose_name = "CSS class (label-)",
        max_length   = 50,
        default      = 'default',
        help_text    = CSS_CLASS_HELP_TEXT,
    )

    icon = models.CharField(
        verbose_name = "glyphicon",
        max_length   = 50,
        default      = 'asterisk',
        help_text    = "See http://getbootstrap.com/components/#glyphicons"
    )

    def __str__(self):
        return self.name

class IssueState(models.Model):

    class Meta:
        verbose_name = "states of progress"
        verbose_name_plural = "states of progress"
        ordering = ['progression', 'id']

    filter_name = 'state'

    id = models.PositiveSmallIntegerField(
        verbose_name = 'ID',
        primary_key  = True,
        validators   = [MaxValueValidator(31)],
        help_text    = "This ID will be used by `UserSettings.state_filters` as 2^(ID).",
    )

    name = models.CharField(
        verbose_name = "name",
        unique       = True,
        max_length   = 50,
    )

    css_class = models.CharField(
        verbose_name = "CSS class (progress-bar-)",
        max_length   = 50,
        default      = 'default',
        help_text    = CSS_CLASS_HELP_TEXT,
    )

    progression = models.PositiveSmallIntegerField(
        verbose_name = "progression",
        validators   = [MaxValueValidator(100)],
        default      = 100,
    )

    def __str__(self):
        return self.name

class IssuePriority(models.Model):

    class Meta:
        verbose_name = "priority level"
        verbose_name_plural = "priority levels"
        ordering = ['-level']

    filter_name = 'priority'

    id = models.PositiveSmallIntegerField(
        verbose_name = 'ID',
        primary_key  = True,
        validators   = [MaxValueValidator(31)],
        help_text    = "This ID will be used by `UserSettings.priority_filters` as 2^(ID).",
    )

    name = models.CharField(
        verbose_name = "name",
        unique       = True,
        max_length   = 50,
    )

    icon = models.CharField(
        verbose_name = "glyphicon",
        max_length   = 50,
        default      = 'asterisk',
        help_text    = "See http://getbootstrap.com/components/#glyphicons"
    )

    level = models.PositiveSmallIntegerField(
        verbose_name = "level",
        default      = 100,
        help_text    = "The higher number, the higher priority.",
    )

    def __str__(self):
        return self.name

class Project(models.Model):

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"

    id = models.CharField(
        verbose_name = "ID",
        primary_key  = True,
        max_length   = 3,
    )

    name = models.CharField(
        verbose_name = "name",
        unique       = True,
        max_length   = 50,
    )

    def __str__(self):
        return self.id

class Issue(models.Model):

    class Meta:
        verbose_name = "issue"
        verbose_name_plural = "issues"
        ordering = ['-priority', 'state']

    project = models.ForeignKey(Project,
        verbose_name = "project",
    )

    type = models.ForeignKey(IssueType,
        verbose_name = "type",
        default      = 0,
    )

    state = models.ForeignKey(IssueState,
        verbose_name = "state",
        default      = 0,
    )

    priority = models.ForeignKey(IssuePriority,
        verbose_name = "priority",
        default      = 0,
    )

    title = models.CharField(
        verbose_name = "title",
        max_length   = 100,
    )

    description = models.TextField(
        verbose_name = "description",
    )

    reporter = models.ForeignKey('auth.User',
        verbose_name = "reporter",
        related_name = 'reported',
    )

    assignee = models.ForeignKey('auth.User',
        verbose_name = "assignee",
        related_name = 'assigned_to',
        blank        = True,
        null         = True,
    )

    created_on = models.DateTimeField(
        verbose_name = "created on",
        auto_now_add = True,
    )

    updated_on = models.DateTimeField(
        verbose_name = "updated on",
        auto_now     = True,
    )

    def __str__(self):
        return "%s-%d / %s" % (self.project_id, self.id, self.title)

    def get_absolute_url(self):
        return reverse('view_issue', kwargs={'pid': self.project_id, 'id': str(self.id)})

    def get_edit_url(self):
        return reverse('edit_issue', kwargs={'pid': self.project_id, 'id': str(self.id)})

class Comment(models.Model):

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    author = models.ForeignKey('auth.User',
        verbose_name = "author",
        related_name = 'comments'
    )

    issue = models.ForeignKey(Issue,
        verbose_name = "task",
        related_name = 'comments'
    )

    content = models.TextField(
        verbose_name = "comment"
    )

    posted_on = models.DateTimeField(
        verbose_name = "posted on",
        auto_now_add = True
    )

    edited_on = models.DateTimeField(
        verbose_name = "edited on",
        auto_now     = True
    )

    def get_edit_url(self):
        return reverse('edit_comment', kwargs={
            'pid' : self.issue.project_id,
            'id'  : str(self.issue_id),
            'cid' : str(self.id)}
        ) +'#'+ str(self.id)

class UserSettings(models.Model):

    ORDERBY_CHOICES = [
        ('-priority__level'    , "Descending priority level"),
        ('priority__level'     , "Ascending priority level"),
        ('-state__progression' , "Descending state progression"),
        ('state__progression'  , "Ascending state progression"),
    ]

    FILTERS_ALL_ENABLED = 2**31-1

    user = models.OneToOneField('auth.User')

    type_filters = models.PositiveIntegerField(
        verbose_name = "type filters",
        default      = FILTERS_ALL_ENABLED,
    )

    state_filters = models.PositiveIntegerField(
        verbose_name = "state filters",
        default      = FILTERS_ALL_ENABLED,
    )

    priority_filters = models.PositiveIntegerField(
        verbose_name = "priority filters",
        default      = FILTERS_ALL_ENABLED,
    )

    orderby = models.CharField(
        verbose_name = "sort by",
        max_length   = 100,
        choices      = ORDERBY_CHOICES,
        default      = ORDERBY_CHOICES[0][0],
    )

    def filter_enabled(self, inst):
        if type(inst) is IssueType:
            return self.type_filters & (2**inst.id)
        elif type(inst) is IssueState:
            return self.state_filters & (2**inst.id)
        elif type(inst) is IssuePriority:
            return self.priority_filters & (2**inst.id)
        else:
            raise TypeError("Invalid argument type")

    def filter_disabled(self, inst):
        return not self.filter_enabled(inst)

    def disable_filter(self, inst):
        reverted_mask = ~ 2**inst.id % (UserSettings.FILTERS_ALL_ENABLED+1)
        if type(inst) is IssueType:
            self.type_filters &= reverted_mask
        elif type(inst) is IssueState:
            self.state_filters &= reverted_mask
        elif type(inst) is IssuePriority:
            self.priority_filters &= reverted_mask
        else:
            raise TypeError("Invalid argument type")

    def reset_filters(self):
        self.type_filters, self.state_filters, self.priority_filters = (UserSettings.FILTERS_ALL_ENABLED,)*3

