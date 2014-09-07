from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$'         , 'core.views.root'    , name='root'    ),
    url(r'^signin/$'  , 'core.views.signin'  , name='signin'  ),
    url(r'^signout/$' , 'core.views.signout' , name='signout' ),

    url(r'^issues/' , include('core.urls')),
    url(r'^admin/'  , include('django.contrib.admin.site.urls')),
)
