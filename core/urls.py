from django.conf.urls import patterns, url

_pid = r'(?P<pid>[A-Z]{2,3})'
_id  = r'(?P<id>\d+)'
_cid = r'(?P(cid>\d+)'

urlpatterns = patterns('core.views',
    url(r'^$'                                         , 'home'       , name='issues_list'  ),
    url(r'^new/$'                                     , 'edit_issue' , name='new_issue'    ),
    url(r'^'+ _pid +r'-'+ _id +r'/$'                  , 'view_issue' , name='view_issue'   ),
    url(r'^'+ _pid +r'-'+ _id +r'/edit$'              , 'edit_issue' , name='edit_issue'   ),
    url(r'^'+ _pid +r'-'+ _id +r'/edit--'+ _cid +r'$' , 'view_issue' , name='edit_comment' ),
)
