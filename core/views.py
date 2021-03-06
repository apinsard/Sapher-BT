# Distributed under the terms of the GNU General Public License v2
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from core.models import *
from core.forms import *

from itertools import chain

import json

def root(request):
    if request.user.is_authenticated():
        return redirect(reverse('issues_list'))
    else:
        return redirect(reverse('signin') + ('?next=%s' % request.path))

def signin(request):
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            login(request, user)

    if request.user.is_authenticated():
        return redirect('/')

    return render_to_response('login.html', {}, RequestContext(request))

def signout(request):
    logout(request)
    return redirect('/')

def home(request):
    if not request.user.is_authenticated():
        return redirect(reverse('signin') + ('?next=%s' % request.path))

    orderby_choices = UserSettings.ORDERBY_CHOICES

    try:
        usersettings = UserSettings.objects.get(user_id=request.user.pk)
    except UserSettings.DoesNotExist:
        usersettings = UserSettings(user_id=request.user.pk)
        usersettings.save()

    issue_types = IssueType.objects.all()
    issue_priorities = IssuePriority.objects.all()
    issue_states = IssueState.objects.all()
    issue_filter_chain = chain(issue_types, issue_priorities, issue_states)

    if request.method == 'POST':
        if request.POST['orderby'] in [u for u,v in orderby_choices]:
            usersettings.orderby = request.POST['orderby']

        usersettings.reset_filters()
        for issue_filter in issue_filter_chain:
            if 'filter_'+ issue_filter.filter_name +'#'+ str(issue_filter.id) not in request.POST:
                usersettings.disable_filter(issue_filter)

        usersettings.save()
        return redirect(reverse('issues_list'))

    issues = Issue.objects.all().order_by(usersettings.orderby)
    for issue_filter in issue_filter_chain:
        if usersettings.filter_disabled(issue_filter):
            issues = issues.exclude(**{issue_filter.filter_name+'_id': issue_filter.id})

    return render_to_response('index.html', {
        'user': request.user,
        'issues': issues,
        'issue_types': issue_types,
        'issue_priorities': issue_priorities,
        'issue_states': issue_states,
        'usersettings': usersettings,
        'orderby_choices': orderby_choices,
        'checks': Check.objects.filter(requested_id=request.user.id).order_by('-requested_on')[:30],
    }, RequestContext(request))

def edit_issue(request, pid=None, id=None):
    if not request.user.is_authenticated():
        return redirect(reverse('signin') + ('?next=%s' % request.path))

    issue = None
    if id is not None:
        issue = Issue.objects.get(pk=id)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            new_issue = form.save(commit=False)
            if not new_issue.reporter_id:
                new_issue.reporter_id = request.user.id
            new_issue.save()

            return redirect(new_issue.get_absolute_url())
    else:
        form = IssueForm(instance=issue)

    return render_to_response('edit.html', {
        'user': request.user,
        'issue': issue,
        'form': form,
    }, RequestContext(request))

def view_issue(request, pid, id, cid=None):
    if not request.user.is_authenticated():
        return redirect(reverse('signin') + ('?next=%s' % request.path))

    issue = get_object_or_404(Issue, pk=id)
    comments = issue.comments.all()
    comment = None

    if cid:
        comment = issue.comments.get(pk=cid)

    if 'check' in request.GET:
        try:
            check = Check.objects.get(pk=request.GET['check'], issue_id=id,
                    requested_id=request.user.id, is_unread=True)
        except Check.DoesNotExist:
            pass
        else:
            check.is_unread = False
            check.save()

    attachments = Attachment.objects.filter(issue_id=id)
    print(attachments)

    comment_form = CommentForm(instance=comment)
    check_form   = CheckForm()

    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                if not new_comment.author_id:
                    new_comment.author_id = request.user.id
                if not new_comment.issue_id:
                    new_comment.issue_id = id
                new_comment.save()

                return redirect(issue.get_absolute_url())
        elif 'check_form' in request.POST:
            check_form = CheckForm(request.POST)
            if check_form.is_valid():
                new_check = check_form.save(commit=False)
                new_check.requester_id = request.user.id
                new_check.issue_id = id
                new_check.save()

    return render_to_response('view.html', {
        'user': request.user,
        'issue': issue,
        'comments': comments,
        'comment_form': comment_form,
        'check_form': check_form,
        'attachments': attachments,
    }, RequestContext(request))


def attach_issue(request, pid, id):

    issue = get_object_or_404(Issue, pk=id)

    required_args = ['type', 'url', 'name', 'description']

    argv = {}

    for arg in required_args:
        if arg in request.GET:
            argv[arg] = request.GET[arg]
        elif arg in request.POST:
            argv[arg] = request.GET[arg]
        else:
            raise Http404("Not found")

    attachment = Attachment(type=argv['type'], url=argv['url'],
                            name=argv['name'], description=argv['description'],
                            issue_id=id)
    attachment.save()

    return HttpResponse("OK")


def json_issue(request, pid, id):

    from core.templatetags.core_filters import labelize_state, \
                                               labelize_priority, \
                                               labelize_type

    issue = get_object_or_404(Issue, pk=id)

    layout = '<table class="table table-condensed">'
    layout += '<tr><td>%(type)s</td><td>%(priority)s</td></tr>'
    layout += '<tr><td colspan="2">%(state)s</td></tr>'
    layout += '<tr><td colspan="2">'+_("reporter")+' %(reporter)s</td></tr>'
    layout += '<tr><td colspan="2">'+_("assignee")+' %(assignee)s</td></tr>'
    layout += '</table>'

    html_summary = layout % {
        'type': labelize_type(issue.type, large=True),
        'priority': labelize_priority(issue.priority, large=True),
        'state': labelize_state(issue.state, large=False),
        'assignee': issue.assignee,
        'reporter': issue.reporter,
    }


    data = json.dumps({
        'id': issue.id,
        '__str__': str(issue),
        'title': issue.title,
        'html_summary': html_summary,
    })
    
    return HttpResponse(data, content_type='application/json')

