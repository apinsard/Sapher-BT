from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'core.views.root', name='root'),

    url(r'^issues/$'                     , 'core.views.home'       , name='issues_list' ),
    url(r'^issues/new/$'                 , 'core.views.edit_issue' , name='new_issue'   ),
    url(r'^issues/ALA-(?P<id>\d+)/$'     , 'core.views.view_issue' , name='view_issue'  ),
    url(r'^issues/ALA-(?P<id>\d+)/edit$' , 'core.views.edit_issue' , name='edit_issue'  ),
    url(r'^issues/ALA-(?P<id>\d+)/edit--(?P<cid>\d+)$', 'core.views.view_issue', name='edit_comment'),
    url(r'^signin/$'                     , 'core.views.signin'     , name='signin'      ),
    url(r'^signout/$'                    , 'core.views.signout'    , name='signout'     ),

    url(r'^admin/', include(admin.site.urls)),
)
