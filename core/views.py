from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from core.models import Issue, Comment, UserSettings
from core.forms import IssueForm, CommentForm

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

    return render_to_response('login.html')

def signout(request):
    logout(request)
    return redirect('/')

def home(request):
    if not request.user.is_authenticated():
        return redirect(reverse('signin') + ('?next=%s' % request.path))

    try:
        usersettings = UserSettings.objects.get(user_id=request.user.pk)
    except UserSettings.DoesNotExist:
        usersettings = UserSettings(user_id=request.user.pk)
        usersettings.save()

    if request.method == 'POST' and 'orderby' in request.POST:
        usersettings.orderby = request.POST['orderby']
        usersettings.filters = 0
        usersettings.filters |= UserSettings.FILTER_TYPE_BUG * ('filter_type_bug' in request.POST)
        usersettings.filters |= UserSettings.FILTER_TYPE_IMPROVEMENT * ('filter_type_improvement' in request.POST)
        usersettings.filters |= UserSettings.FILTER_TYPE_FEATURE * ('filter_type_feature' in request.POST)
        usersettings.filters |= UserSettings.FILTER_STATE_CANCELLED * ('filter_state_cancelled' in request.POST)
        usersettings.filters |= UserSettings.FILTER_STATE_REPORTED * ('filter_state_reported' in request.POST)
        usersettings.filters |= UserSettings.FILTER_STATE_CONFIRMED * ('filter_state_confirmed' in request.POST)
        usersettings.filters |= UserSettings.FILTER_STATE_QUEUED * ('filter_state_queued' in request.POST)
        usersettings.filters |= UserSettings.FILTER_STATE_DONE * ('filter_state_done' in request.POST)
        usersettings.filters |= UserSettings.FILTER_STATE_TESTED * ('filter_state_tested' in request.POST)
        usersettings.filters |= UserSettings.FILTER_STATE_COMPLETED * ('filter_state_completed' in request.POST)
        usersettings.filters |= UserSettings.FILTER_PRIORITY_ONEDAY * ('filter_priority_oneday' in request.POST)
        usersettings.filters |= UserSettings.FILTER_PRIORITY_LOW * ('filter_priority_low' in request.POST)
        usersettings.filters |= UserSettings.FILTER_PRIORITY_NORMAL * ('filter_priority_normal' in request.POST)
        usersettings.filters |= UserSettings.FILTER_PRIORITY_HIGH * ('filter_priority_high' in request.POST)
        usersettings.filters |= UserSettings.FILTER_PRIORITY_CRITICAL * ('filter_priority_critical' in request.POST)
        usersettings.filters |= UserSettings.FILTER_PRIORITY_BLOCKER * ('filter_priority_blocker' in request.POST)
        usersettings.save()

    issues = Issue.objects.all().order_by(usersettings.orderby)
    if not usersettings.filters & UserSettings.FILTER_STATE_CANCELLED:
        issues = issues.exclude(state=Issue.STATE_CANCELLED)
    if not usersettings.filters & UserSettings.FILTER_STATE_REPORTED:
        issues = issues.exclude(state=Issue.STATE_REPORTED)
    if not usersettings.filters & UserSettings.FILTER_STATE_CONFIRMED:
        issues = issues.exclude(state=Issue.STATE_CONFIRMED)
    if not usersettings.filters & UserSettings.FILTER_STATE_QUEUED:
        issues = issues.exclude(state=Issue.STATE_QUEUED)
    if not usersettings.filters & UserSettings.FILTER_STATE_DONE:
        issues = issues.exclude(state=Issue.STATE_DONE)
    if not usersettings.filters & UserSettings.FILTER_STATE_TESTED:
        issues = issues.exclude(state=Issue.STATE_TESTED)
    if not usersettings.filters & UserSettings.FILTER_STATE_COMPLETED:
        issues = issues.exclude(state=Issue.STATE_COMPLETED)
    if not usersettings.filters & UserSettings.FILTER_PRIORITY_ONEDAY:
        issues = issues.exclude(priority=Issue.PRIORITY_ONEDAY)
    if not usersettings.filters & UserSettings.FILTER_PRIORITY_LOW:
        issues = issues.exclude(priority=Issue.PRIORITY_LOW)
    if not usersettings.filters & UserSettings.FILTER_PRIORITY_NORMAL:
        issues = issues.exclude(priority=Issue.PRIORITY_NORMAL)
    if not usersettings.filters & UserSettings.FILTER_PRIORITY_HIGH:
        issues = issues.exclude(priority=Issue.PRIORITY_HIGH)
    if not usersettings.filters & UserSettings.FILTER_PRIORITY_CRITICAL:
        issues = issues.exclude(priority=Issue.PRIORITY_CRITICAL)
    if not usersettings.filters & UserSettings.FILTER_PRIORITY_BLOCKER:
        issues = issues.exclude(priority=Issue.PRIORITY_BLOCKER)
    if not usersettings.filters & UserSettings.FILTER_TYPE_BUG:
        issues = issues.exclude(type=Issue.TYPE_BUG)
    if not usersettings.filters & UserSettings.FILTER_TYPE_IMPROVEMENT:
        issues = issues.exclude(type=Issue.TYPE_IMPROVEMENT)
    if not usersettings.filters & UserSettings.FILTER_TYPE_FEATURE:
        issues = issues.exclude(type=Issue.TYPE_FEATURE)

    return render_to_response('index.html', {
        'user'   : request.user,
        'usersettings': usersettings,
        'issues' : issues,
        })

def edit_issue(request, id=None):
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
        })

def view_issue(request, id, cid=None):
    if not request.user.is_authenticated():
        return redirect(reverse('signin') + ('?next=%s' % request.path))

    issue = Issue.objects.get(pk=id)
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
        })

