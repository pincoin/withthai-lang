from django.conf.urls import url

from .views import (
    PostDetailView, NoticeDetailView, NoticeListView
)

app_name = 'help'

urlpatterns = [
    url(r'^pages/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(), name='post-detail'),
    url(r'^notices/$',
        NoticeListView.as_view(), name='notice-list'),
    url(r'^notices/(?P<pk>\d+)/$',
        NoticeDetailView.as_view(), name='notice-detail'),
]
