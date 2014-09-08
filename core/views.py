from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from core.models import *
from core.forms import *

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

    if request.method == 'POST':
        if request.POST['orderby'] in [u for u,v in orderby_choices]:
            usersettings.orderby = request.POST['orderby']

        usersettings.type_filters = UserSettings.FILTERS_ALL_ENABLED
        for type in issue_types:
            if 'filter_type#'+str(type.id) not in request.POST:
                usersettings.disable_filter(type)

        usersettings.priority_filters = UserSettings.FILTERS_ALL_ENABLED
        for priority in issue_priorities:
            if 'filter_priority#'+str(priority.id) not in request.POST:
                usersettings.disable_filter(priority)

        usersettings.state_filters = UserSettings.FILTERS_ALL_ENABLED
        for state in issue_states:
            if 'filter_state#'+str(state.id) not in request.POST:
                usersettings.disable_filter(state)

        usersettings.save()

    issues = Issue.objects.all()

    return render_to_response('index.html', {
        'user': request.user,
        'issues': issues,
        'issue_types': issue_types,
        'issue_priorities': issue_priorities,
        'issue_states': issue_states,
        'usersettings': usersettings,
        'orderby_choices': orderby_choices,
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
        form  = IssueForm(instance=issue)

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

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            new_comment = form.save(commit=False)
            if not new_comment.author_id:
                new_comment.author_id = request.user.id
            if not new_comment.issue_id:
                new_comment.issue_id = id
            new_comment.save()
            return redirect(issue.get_absolute_url())
    else:
        form = CommentForm(instance=comment)

    return render_to_response('view.html', {
        'user': request.user,
        'issue': issue,
        'comments': comments,
        'comment_form': form
    }, RequestContext(context))

