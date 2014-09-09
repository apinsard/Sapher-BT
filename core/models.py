# Distributed under the terms of the GNU General Public License v2
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, RegexValidator
from django.utils.translation import ugettext_lazy as _

CSS_CLASS_HELP_TEXT = _('Predefined styles are "default" (gray), "primary" (blue), "success" '\
    + '(green), "info" (cyan), "warning" (orange) and "danger" (red). You can also create your '\
    + 'own in your stylesheet.')

MARKDOWN_FIELD_HELP_TEXT = _('The text will be formatted in <a target=_blank '\
    + 'href="http://en.wikipedia.com/wiki/Markdown">Mardown</a>. HTML also supported for advanced '\
    + 'formatting. A line break behaves the same as a space. Two consecutive line breaks mark a '\
    + 'new paragraph.')

class IssueType(models.Model):

    class Meta:
        verbose_name = _("type")
        verbose_name_plural = _("types")
        ordering = ['id']

    filter_name = 'type'

    id = models.PositiveSmallIntegerField(
        verbose_name = _("ID"),
        primary_key  = True,
        validators   = [MaxValueValidator(31)],
        help_text    = _("This ID will be used by `UserSettings.type_filters` as 2^(ID)."),
    )

    name = models.CharField(
        verbose_name = _("name"),
        unique       = True,
        max_length   = 50,
    )

    css_class = models.CharField(
        verbose_name = _("CSS class (label-)"),
        max_length   = 50,
        default      = 'default',
        help_text    = CSS_CLASS_HELP_TEXT,
    )

    icon = models.CharField(
        verbose_name = _("glyphicon"),
        max_length   = 50,
        default      = 'asterisk',
        help_text    = _("See http://getbootstrap.com/components/#glyphicons"),
    )

    def __str__(self):
        return self.name

class IssueState(models.Model):

    class Meta:
        verbose_name = _("state of progress")
        verbose_name_plural = _("states of progress")
        ordering = ['progression', 'id']

    filter_name = 'state'

    id = models.PositiveSmallIntegerField(
        verbose_name = _("ID"),
        primary_key  = True,
        validators   = [MaxValueValidator(31)],
        help_text    = _("This ID will be used by `UserSettings.state_filters` as 2^(ID)."),
    )

    name = models.CharField(
        verbose_name = _("name"),
        unique       = True,
        max_length   = 50,
    )

    css_class = models.CharField(
        verbose_name = _("CSS class (progress-bar-)"),
        max_length   = 50,
        default      = 'default',
        help_text    = CSS_CLASS_HELP_TEXT,
    )

    progression = models.PositiveSmallIntegerField(
        verbose_name = _("progression"),
        validators   = [MaxValueValidator(100)],
        default      = 100,
        help_text    = _("Between 0 and 100."),
    )

    def __str__(self):
        return self.name

class IssuePriority(models.Model):

    class Meta:
        verbose_name = _("priority level")
        verbose_name_plural = _("priority levels")
        ordering = ['-level']

    filter_name = 'priority'

    id = models.PositiveSmallIntegerField(
        verbose_name = _("ID"),
        primary_key  = True,
        validators   = [MaxValueValidator(31)],
        help_text    = _("This ID will be used by `UserSettings.priority_filters` as 2^(ID)."),
    )

    name = models.CharField(
        verbose_name = _("name"),
        unique       = True,
        max_length   = 50,
    )

    icon = models.CharField(
        verbose_name = _("glyphicon"),
        max_length   = 50,
        default      = 'asterisk',
        help_text    = _("See http://getbootstrap.com/components/#glyphicons"),
    )

    level = models.PositiveSmallIntegerField(
        verbose_name = "level",
        default      = 100,
        help_text    = _("The higher number, the higher priority."),
    )

    def __str__(self):
        return self.name

class Project(models.Model):

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    id = models.CharField(
        verbose_name = _("ID"),
        primary_key  = True,
        max_length   = 3,
        validators   = [RegexValidator(r"^[A-Z]{2,}$")],
        help_text    = _("Two or three uppercase letters to quickly identify this project"),
    )

    name = models.CharField(
        verbose_name = _("name"),
        unique       = True,
        max_length   = 50,
    )

    def __str__(self):
        return self.id

class Issue(models.Model):

    class Meta:
        verbose_name = _("issue")
        verbose_name_plural = _("issues")
        ordering = ['-priority', 'state']

    project = models.ForeignKey(Project,
        verbose_name = _("project"),
    )

    type = models.ForeignKey(IssueType,
        verbose_name = _("type"),
        default      = 0,
    )

    state = models.ForeignKey(IssueState,
        verbose_name = _("state"),
        default      = 0,
    )

    priority = models.ForeignKey(IssuePriority,
        verbose_name = _("priority"),
        default      = 0,
    )

    title = models.CharField(
        verbose_name = _("title"),
        max_length   = 100,
    )

    description = models.TextField(
        verbose_name = _("description"),
        help_text    = MARKDOWN_FIELD_HELP_TEXT,
    )

    reporter = models.ForeignKey('auth.User',
        verbose_name = _("reporter"),
        related_name = 'reported',
    )

    assignee = models.ForeignKey('auth.User',
        verbose_name = _("assignee"),
        related_name = 'assigned_to',
        blank        = True,
        null         = True,
    )

    created_on = models.DateTimeField(
        verbose_name = _("created on"),
        auto_now_add = True,
    )

    updated_on = models.DateTimeField(
        verbose_name = _("updated on"),
        auto_now     = True,
        blank        = True,
        null         = True,
    )

    def __str__(self):
        return "%s-%d / %s" % (self.project_id, self.id, self.title)

    def get_absolute_url(self):
        return reverse('view_issue', kwargs={'pid': self.project_id, 'id': str(self.id)})

    def get_edit_url(self):
        return reverse('edit_issue', kwargs={'pid': self.project_id, 'id': str(self.id)})

class Comment(models.Model):

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    author = models.ForeignKey('auth.User',
        verbose_name = _("author"),
        related_name = 'comments',
    )

    issue = models.ForeignKey(Issue,
        verbose_name = _("task"),
        related_name = 'comments',
    )

    content = models.TextField(
        verbose_name = _("comment"),
        help_text    = MARKDOWN_FIELD_HELP_TEXT,
    )

    posted_on = models.DateTimeField(
        verbose_name = _("posted on"),
        auto_now_add = True,
    )

    edited_on = models.DateTimeField(
        verbose_name = _("edited on"),
        auto_now     = True,
        blank        = True,
        null         = True,
    )

    def get_edit_url(self):
        return reverse('edit_comment', kwargs={
            'pid' : self.issue.project_id,
            'id'  : str(self.issue_id),
            'cid' : str(self.id),
        }) +'#'+ str(self.id)

class UserSettings(models.Model):

    ORDERBY_CHOICES = [
        ('-priority__level'    , _("Descending priority level")),
        ('priority__level'     , _("Ascending priority level")),
        ('-state__progression' , _("Descending state progression")),
        ('state__progression'  , _("Ascending state progression")),
    ]

    FILTERS_ALL_ENABLED = 2**31-1

    user = models.OneToOneField('auth.User')

    type_filters = models.PositiveIntegerField(
        verbose_name = _("type filters"),
        default      = FILTERS_ALL_ENABLED,
    )

    state_filters = models.PositiveIntegerField(
        verbose_name = _("state filters"),
        default      = FILTERS_ALL_ENABLED,
    )

    priority_filters = models.PositiveIntegerField(
        verbose_name = _("priority filters"),
        default      = FILTERS_ALL_ENABLED,
    )

    orderby = models.CharField(
        verbose_name = _("sort by"),
        max_length   = 100,
        choices      = ORDERBY_CHOICES,
        default      = ORDERBY_CHOICES[0][0],
    )

    def filter_enabled(self, issue_filter):
        if type(issue_filter) is IssueType:
            return self.type_filters & (2**issue_filter.id)
        elif type(issue_filter) is IssueState:
            return self.state_filters & (2**issue_filter.id)
        elif type(issue_filter) is IssuePriority:
            return self.priority_filters & (2**issue_filter.id)
        else:
            raise TypeError("Unexpected type: %r" % type(issue_filter))

    def filter_disabled(self, issue_filter):
        return not self.filter_enabled(issue_filter)

    def disable_filter(self, issue_filter):
        reverted_mask = ~ 2**issue_filter.id % (UserSettings.FILTERS_ALL_ENABLED+1)
        if type(issue_filter) is IssueType:
            self.type_filters &= reverted_mask
        elif type(issue_filter) is IssueState:
            self.state_filters &= reverted_mask
        elif type(issue_filter) is IssuePriority:
            self.priority_filters &= reverted_mask
        else:
            raise TypeError("Unexpected type: %r" % type(issue_filter))

    def reset_filters(self):
        self.type_filters, self.state_filters, self.priority_filters
            = (UserSettings.FILTERS_ALL_ENABLED,)*3

