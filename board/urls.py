from django.conf.urls import url

from .views import (
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView,
)

app_name = 'board'

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$',
        MessageListView.as_view(), name='message-list'),
    url(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/$',
        MessageDetailView.as_view(), name='message-detail'),
    url(r'^(?P<slug>[-\w]+)/new/$',
        MessageCreateView.as_view(), name='message-new'),
    url(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/edit/$',
        MessageUpdateView.as_view(), name='message-edit'),
    url(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/delete/$',
        MessageDeleteView.as_view(), name='message-delete'),
]
