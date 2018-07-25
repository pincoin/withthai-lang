from django.conf.urls import url

from .views import (
    MessageListView, MessageDetailView
)

app_name = 'board'

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$',
        MessageListView.as_view(), name='message-list'),
    url(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/$',
        MessageDetailView.as_view(), name='message-detail'),
]
