from django import template
from django.utils.safestring import mark_safe
from core.models import IssueType, IssueState, IssuePriority

register = template.Library()

@register.filter
def labelize(inst, large=False):
    if type(inst) is IssueType:
        html = labelize_type(inst, large)
    elif type(inst) is IssueState:
        html = labelize_state(inst, large)
    elif type(inst) is IssuePriority:
        html = labelize_priority(inst, large)
    else:
        raise TypeError("Invalid argument type")
    return mark_safe(html)

@register.filter
def filter_enabled(user_settings, inst):
    return user_settings.filter_enabled(inst)


def labelize_type(issue_type, large=False):
    html = '<span class="label label-%(css_class)s" title="%(name)s"> '\
        + '<span class="glyphicon glyphicon-%(icon)s"></span></span>'

    return html % {
        'css_class' : issue_type.css_class,
        'name'      : issue_type.name,
        'icon'      : issue_type.icon,
    }

def labelize_state(issue_state, large=False):
    html = '<div class=progress'
    if not large:
        html += ' data-toggle=tooltip data-placement=left title="%(name)s"'
    html += '><div class="progress-bar progress-bar-%(css_class)s" role=progressbar '\
        + 'aria-valuenow=%(percent)d aria-valuemin=0 aria-valuemax=100 '\
        + 'style="width:%(percent)d%%;">'
    if large:
        html += '%(name)s'
    html += '</div></div>'

    return html % {
        'css_class' : issue_state.css_class,
        'name'      : issue_state.name,
        'percent'   : issue_state.progression
    }

def labelize_priority(issue_priority, large=False):
    html = '<span class="glyphicon glyphicon-%(icon)s" title="%(name)s"></span>'

    return html % {
        'name'      : issue_priority.name,
        'icon'      : issue_priority.icon,
    }


