# Distributed under the terms of the GNU General Public License v2
from django.conf.urls import patterns, url

_pid = r'(?P<pid>[A-Z]{2,3})'
_id  = r'(?P<id>\d+)'
_cid = r'(?P<cid>\d+)'

urlpatterns = patterns('core.views',
    url('^$'                                      , 'home'         , name='issues_list'  ),
    url('^new/$'                                  , 'edit_issue'   , name='new_issue'    ),
    url('^'+ _pid +'-'+ _id +'/$'                 , 'view_issue'   , name='view_issue'   ),
    url('^'+ _pid +'-'+ _id +'/edit$'             , 'edit_issue'   , name='edit_issue'   ),
    url('^'+ _pid +'-'+ _id +'/edit--'+ _cid +'$' , 'view_issue'   , name='edit_comment' ),
    url('^'+ _pid +'-'+ _id +'/attach$'           , 'attach_issue' , name='attach_issue' ),
)
