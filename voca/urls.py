from django.conf.urls import url

from .views import (
    EntryListView, EntryDetailView, EntryCategoryView, EntryLevelListView,
    TextbookListView, TextbookEntryListView, LevelListView
)

app_name = 'voca'

urlpatterns = [
    url(r'^entry/$',
        EntryListView.as_view(), name='entry-list'),
    url(r'^entry/(?P<pk>\d+)/$',
        EntryDetailView.as_view(), name='entry-detail'),

    url(r'^level/$',
        LevelListView.as_view(), name='level-list'),
    url(r'^level/(?P<level>[\w]+)$',
        EntryLevelListView.as_view(), name='level-entry-list'),

    url(r'^category/(?P<slug>[-\w]+)/$',
        EntryCategoryView.as_view(), name='entry-category'),

    url(r'^textbook/$',
        TextbookListView.as_view(), name='textbook-list'),
    url(r'^textbook/(?P<slug>[-\w]+)/$',
        TextbookEntryListView.as_view(), name='textbook-entry-list'),
]
