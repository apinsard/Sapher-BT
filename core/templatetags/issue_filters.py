from django import template
from core.models import IssueType, IssueState, IssuePriority

register = template.Library()

@register.filter
def labelize(model, large=False):
    if type(model) is IssueType:
        return labelize_type(model, large)
    if type(model) is IssueState:
        return labelize_state(model, large)
    if type(model) is IssuePriority:
        return labelize_priority(model, large)

def labelize_type(issue_type, large=False):
    html = '<span class="label label-%(css_class)s" title="%(name)s"> '\
        + '<span class="glyphicon glyphicon-$(icon)s"></span></span>'

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

