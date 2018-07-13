from django.conf.urls import url

from .views import (
    PostDetailView, NoticeDetailView
)

app_name = 'help'

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(), name='post-detail'),
    url(r'^/notices/(?P<pk>\d+)/$',
        NoticeDetailView.as_view(), name='notice-detail'),
]
