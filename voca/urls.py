from django.conf.urls import url

from .views import (
    EntryListView, EntryDetailView
)

app_name = 'voca'

urlpatterns = [
    url(r'^entries/$',
        EntryListView.as_view(), name='entry-list'),
    url(r'^entries/(?P<pk>\d+)/$',
        EntryDetailView.as_view(), name='entry-detail'),
]
