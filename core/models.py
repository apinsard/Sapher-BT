#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Issue(models.Model):

    class Meta:
        verbose_name = "tâche"
        verbose_name_plural = "tâches"
        ordering = ['-priority', 'state']

    TYPE_BUG         = 1
    TYPE_IMPROVEMENT = 2
    TYPE_FEATURE     = 3

    TYPE_CHOICES = [
            (TYPE_BUG         , "Bug"),
            (TYPE_IMPROVEMENT , "Amélioration"),
            (TYPE_FEATURE     , "Nouvelle fonctionnalité"),
            ]

    STATE_CANCELLED = 0
    STATE_REPORTED  = 1
    STATE_CONFIRMED = 2
    STATE_QUEUED    = 3
    STATE_DONE      = 4
    STATE_TESTED    = 5
    STATE_COMPLETED = 6

    STATE_CHOICES = [
            (STATE_REPORTED  , "Relevé"),
            (STATE_CANCELLED , "Annulé"),
            (STATE_CONFIRMED , "Confirmé"),
            (STATE_QUEUED    , "À faire"),
            (STATE_DONE      , "À tester"),
            (STATE_TESTED    , "Testé"),
            (STATE_COMPLETED , "Terminé"),
            ]

    PRIORITY_ONEDAY   = 1
    PRIORITY_LOW      = 2
    PRIORITY_NORMAL   = 3
    PRIORITY_HIGH     = 4
    PRIORITY_CRITICAL = 5
    PRIORITY_BLOCKER  = 6

    PRIORITY_CHOICES = [
            (PRIORITY_ONEDAY   , "Un jour..."),
            (PRIORITY_LOW      , "Faible"),
            (PRIORITY_NORMAL   , "Normale"),
            (PRIORITY_HIGH     , "Haute"),
            (PRIORITY_CRITICAL , "Critique"),
            (PRIORITY_BLOCKER  , "Bloquant"),
            ]

    type = models.PositiveSmallIntegerField(
            verbose_name = "type",
            choices      = TYPE_CHOICES,
            default      = TYPE_BUG,
            )

    state = models.PositiveSmallIntegerField(
            verbose_name = "statut",
            choices      = STATE_CHOICES,
            default      = STATE_REPORTED,
            )

    priority = models.PositiveSmallIntegerField(
            verbose_name = "priorité",
            choices      = PRIORITY_CHOICES,
            default      = PRIORITY_NORMAL,
            )

    title = models.CharField(
            verbose_name = "titre",
            max_length   = 100,
            )

    description = models.TextField(
            verbose_name = "description",
            )

    reporter = models.ForeignKey('auth.User',
            verbose_name = "relevé par",
            related_name = 'reported',
            )

    assignee = models.ForeignKey('auth.User',
            verbose_name = "assigné à",
            related_name = 'assigned_to',
            blank        = True,
            null         = True,
            )

    created_on = models.DateTimeField(
            verbose_name = "créé le",
            auto_now_add = True,
            )

    updated_on = models.DateTimeField(
            verbose_name = "mis à jour le",
            auto_now     = True,
            )

    def get_absolute_url(self):
        return reverse('view_issue', kwargs={'id': str(self.id)})

    def get_edit_url(self):
        return reverse('edit_issue', kwargs={'id': str(self.id)})

    def type_label(self):
        if self.type is Issue.TYPE_BUG:
            return '<span class="label label-danger" title="Bug"><span class="glyphicon glyphicon-exclamation-sign"></span></span>'
        if self.type is Issue.TYPE_IMPROVEMENT:
            return '<span class="label label-warning" title="Amélioration"><span class="glyphicon glyphicon-wrench"></span></span>'
        if self.type is Issue.TYPE_FEATURE:
            return '<span class="label label-primary" title="Nouvelle Fonctionnalité"><span class="glyphicon glyphicon-plus"></span></span>'

    def type_name(self):
        if self.type is Issue.TYPE_BUG:
            return 'Bug'
        if self.type is Issue.TYPE_IMPROVEMENT:
            return 'Amélioration'
        if self.type is Issue.TYPE_FEATURE:
            return 'Nouvelle Fonctionnalité'

    def priority_label(self):
        if self.priority is Issue.PRIORITY_ONEDAY:
            return '<span class="glyphicon glyphicon-tint" title="Un jour..."></span>'
        if self.priority is Issue.PRIORITY_LOW:
            return '<span class="glyphicon glyphicon-arrow-down" title="Faible"></span>'
        if self.priority is Issue.PRIORITY_NORMAL:
            return '<span class="glyphicon glyphicon-arrow-right" title="Normale"></span>'
        if self.priority is Issue.PRIORITY_HIGH:
            return '<span class="glyphicon glyphicon-arrow-up" title="Haute"></span>'
        if self.priority is Issue.PRIORITY_CRITICAL:
            return '<span class="glyphicon glyphicon-warning-sign" title="Critique"></span>'
        if self.priority is Issue.PRIORITY_BLOCKER:
            return '<span class="glyphicon glyphicon-ban-circle" title="Bloquant"></span>'

    def priority_name(self):
        if self.priority is Issue.PRIORITY_ONEDAY:
            return 'Un jour...'
        if self.priority is Issue.PRIORITY_LOW:
            return 'Faible'
        if self.priority is Issue.PRIORITY_NORMAL:
            return 'Normale'
        if self.priority is Issue.PRIORITY_HIGH:
            return 'Haute'
        if self.priority is Issue.PRIORITY_CRITICAL:
            return 'Critique'
        if self.priority is Issue.PRIORITY_BLOCKER:
            return 'Bloquant'

    def small_state_label(self):
        pcent = None
        label = None
        classes = ['progress-bar']
        if self.state is Issue.STATE_CANCELLED:
            pcent = 0
            label = "Annulé"
            classes.append('progress-bar-info')
        if self.state is Issue.STATE_REPORTED:
            pcent = 100//6
            label = "Relevé"
        if self.state is Issue.STATE_CONFIRMED:
            pcent = 200//6
            label = "Confirmé"
            classes.append('progress-bar-info')
        if self.state is Issue.STATE_QUEUED:
            pcent = 300//6
            label = "À faire"
            classes.append('progress-bar-danger')
        if self.state is Issue.STATE_DONE:
            pcent = 400//6
            label = "À tester"
            classes.append('progress-bar-warning')
        if self.state is Issue.STATE_TESTED:
            pcent = 500//6
            label = "Testé"
            classes.append('progress-bar-success')
        if self.state is Issue.STATE_COMPLETED:
            pcent = 600//6
            label = "Terminé"
            classes.append('progress-bar-success')

        html = '<div class=progress data-toggle="tooltip" data-placement="left" title="'+ label +'">'
        html += '<div class="'+ ' '.join(classes) +'" role=progressbar '
        html += 'aria-valuenow='+ str(pcent) +' aria-valuemin=0 aria-valuemax=100 '
        html += 'style="width:'+ str(pcent) +'%;"></div></div>'
        return html

    def state_label(self):
        pcent = None
        label = None
        classes = ['progress-bar']
        if self.state is Issue.STATE_CANCELLED:
            pcent = 0
            label = "Annulé"
            classes.append('progress-bar-info')
        if self.state is Issue.STATE_REPORTED:
            pcent = 100//6
            label = "Relevé"
        if self.state is Issue.STATE_CONFIRMED:
            pcent = 200//6
            label = "Confirmé"
            classes.append('progress-bar-info')
        if self.state is Issue.STATE_QUEUED:
            pcent = 300//6
            label = "À faire"
            classes.append('progress-bar-danger')
        if self.state is Issue.STATE_DONE:
            pcent = 400//6
            label = "À tester"
            classes.append('progress-bar-warning')
        if self.state is Issue.STATE_TESTED:
            pcent = 500//6
            label = "Testé"
            classes.append('progress-bar-success')
        if self.state is Issue.STATE_COMPLETED:
            pcent = 600//6
            label = "Terminé"
            classes.append('progress-bar-success')

        html = '<div class=progress><div class="'+ ' '.join(classes) +'" role=progressbar '
        html += 'aria-valuenow='+ str(pcent) +' aria-valuemin=0 aria-valuemax=100 '
        html += 'style="width:'+ str(pcent) +'%;">'+ label +'</div></div>'
        return html

class Comment(models.Model):

    class Meta:
        verbose_name = u"commentaire"
        verbose_name_plural = u"commentaires"

    author = models.ForeignKey('auth.User',
            verbose_name = u"auteur",
            related_name = 'comments'
            )

    issue = models.ForeignKey(Issue,
            verbose_name = u"tâche",
            related_name = 'comments'
            )

    content = models.TextField(
            verbose_name = u"commentaire"
            )

    posted_on = models.DateTimeField(
            verbose_name = u"posté le",
            auto_now_add = True
            )

    edited_on = models.DateTimeField(
            verbose_name = u"modifié le",
            auto_now     = True
            )

    def get_edit_url(self):
        return reverse('edit_comment', kwargs={'id': str(self.issue_id), 'cid': str(self.id)}) +'#'+ str(self.id)

class UserSettings(models.Model):

    FILTER_TYPE_BUG          = 0x1
    FILTER_TYPE_IMPROVEMENT  = 0x2
    FILTER_TYPE_FEATURE      = 0x4
    FILTER_STATE_CANCELLED   = 0x8
    FILTER_STATE_REPORTED    = 0x10
    FILTER_STATE_CONFIRMED   = 0x20
    FILTER_STATE_QUEUED      = 0x40
    FILTER_STATE_DONE        = 0x80
    FILTER_STATE_TESTED      = 0x100
    FILTER_STATE_COMPLETED   = 0x200
    FILTER_PRIORITY_ONEDAY   = 0x400
    FILTER_PRIORITY_LOW      = 0x800
    FILTER_PRIORITY_NORMAL   = 0x1000
    FILTER_PRIORITY_HIGH     = 0x2000
    FILTER_PRIORITY_CRITICAL = 0x4000
    FILTER_PRIORITY_BLOCKER  = 0x8000

    FILTERS_DEFAULT = \
            FILTER_TYPE_BUG          | \
            FILTER_TYPE_IMPROVEMENT  | \
            FILTER_TYPE_FEATURE      | \
            FILTER_STATE_REPORTED    | \
            FILTER_STATE_CONFIRMED   | \
            FILTER_STATE_QUEUED      | \
            FILTER_STATE_DONE        | \
            FILTER_STATE_TESTED      | \
            FILTER_PRIORITY_ONEDAY   | \
            FILTER_PRIORITY_LOW      | \
            FILTER_PRIORITY_NORMAL   | \
            FILTER_PRIORITY_HIGH     | \
            FILTER_PRIORITY_CRITICAL | \
            FILTER_PRIORITY_BLOCKER

    user = models.OneToOneField(User)

    filters = models.PositiveIntegerField(
            verbose_name = "filtres",
            default      = FILTERS_DEFAULT,
            )

    ORDERBY_CHOICES = [
            ('-priority' , "Priorité décroissante"),
            ('priority'  , "Priorité croissante"),
            ('-state'    , "État décroissant"),
            ('state'     , "État croissant"),
            ]

    orderby = models.CharField(
            verbose_name = "trier par",
            max_length   = 20,
            choices      = ORDERBY_CHOICES,
            default      = ORDERBY_CHOICES[0][0],
            )

    def html_orderby_select(self):
        html = '<select name=orderby id=id_orderby class=form-control>';
        for value, label in UserSettings.ORDERBY_CHOICES:
            html += '<option value="'+ value +'"'
            if value == self.orderby:
                html += ' selected'
            html += '>'+ label +'</option>'
        html += '</select>'
        return html

    def html_filter_type_checkboxes(self):
        html = '<div class="checkbox">'
        html += '<label><input type=checkbox name=filter_type_bug'
        if self.filters & UserSettings.FILTER_TYPE_BUG:
            html += ' checked'
        html += '>&nbsp;Bug</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_type_improvement'
        if self.filters & UserSettings.FILTER_TYPE_IMPROVEMENT:
            html += ' checked'
        html += '>&nbsp;Amélioration</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_type_feature'
        if self.filters & UserSettings.FILTER_TYPE_FEATURE:
            html += ' checked'
        html += '>&nbsp;Nouvelle&nbsp;Fonctionnalité</label>'
        html += '</div>'
        return html

    def html_filter_priority_checkboxes(self):
        html = '<div class="checkbox">'
        html += '<label><input type=checkbox name=filter_priority_oneday'
        if self.filters & UserSettings.FILTER_PRIORITY_ONEDAY:
            html += ' checked'
        html += '>&nbsp;<span class="glyphicon glyphicon-tint"></span></label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_priority_low'
        if self.filters & UserSettings.FILTER_PRIORITY_LOW:
            html += ' checked'
        html += '>&nbsp;<span class="glyphicon glyphicon-arrow-down"></span></label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_priority_normal'
        if self.filters & UserSettings.FILTER_PRIORITY_NORMAL:
            html += ' checked'
        html += '>&nbsp;<span class="glyphicon glyphicon-arrow-right"></span></label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_priority_high'
        if self.filters & UserSettings.FILTER_PRIORITY_HIGH:
            html += ' checked'
        html += '>&nbsp;<span class="glyphicon glyphicon-arrow-up"></span></label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_priority_critical'
        if self.filters & UserSettings.FILTER_PRIORITY_CRITICAL:
            html += ' checked'
        html += '>&nbsp;<span class="glyphicon glyphicon-warning-sign"></span></label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_priority_blocker'
        if self.filters & UserSettings.FILTER_PRIORITY_BLOCKER:
            html += ' checked'
        html += '>&nbsp;<span class="glyphicon glyphicon-ban-circle"></span></label>'
        html += '</div>'
        return html

    def html_filter_state_checkboxes(self):
        html = '<div class="checkbox">'
        html += '<label><input type=checkbox name=filter_state_cancelled'
        if self.filters & UserSettings.FILTER_STATE_CANCELLED:
            html += ' checked'
        html += '>&nbsp;Annulé</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_state_reported'
        if self.filters & UserSettings.FILTER_STATE_REPORTED:
            html += ' checked'
        html += '>&nbsp;Relevé</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_state_confirmed'
        if self.filters & UserSettings.FILTER_STATE_CONFIRMED:
            html += ' checked'
        html += '>&nbsp;Confirmé</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_state_queued'
        if self.filters & UserSettings.FILTER_STATE_QUEUED:
            html += ' checked'
        html += '>&nbsp;À faire</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_state_done'
        if self.filters & UserSettings.FILTER_STATE_DONE:
            html += ' checked'
        html += '>&nbsp;À tester</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_state_tested'
        if self.filters & UserSettings.FILTER_STATE_TESTED:
            html += ' checked'
        html += '>&nbsp;Testé</label>'
        html += '&emsp;'
        html += '<label><input type=checkbox name=filter_state_completed'
        if self.filters & UserSettings.FILTER_STATE_COMPLETED:
            html += ' checked'
        html += '>&nbsp;Terminé</label>'
        html += '</div>'
        return html

