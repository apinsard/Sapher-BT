from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
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

    return render_to_response('login.html')

def signout(request):
    logout(request)
    return redirect('/')

def home(request):
    if not request.user.is_authenticated():
        return redirect(reverse('signin') + ('?next=%s' % request.path))

    issues = Issue.objects.all()

    return render_to_response('index.html', {
        'user'   : request.user,
        'issues' : issues,
    })

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
        })

def view_issue(request, pid, id, cid=None):
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

