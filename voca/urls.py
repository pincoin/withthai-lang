from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from .sitemaps import EntrySitemap
from .views import (
    EntryListView, EntryDetailView, LevelListView, EntryLevelListView, EntryLevelDetailView,
    EntryCategoryView, CategoryTemplateView,
    TextbookListView, TextbookEntryListView,
)

app_name = 'voca'

sitemaps_entry = {
    'sitemap': EntrySitemap(),
}

urlpatterns = [
    url(r'^entry/$',
        EntryListView.as_view(), name='entry-list'),
    url(r'^entry/(?P<pk>\d+)/$',
        EntryDetailView.as_view(), name='entry-detail'),

    url(r'^level/$',
        LevelListView.as_view(), name='level-list'),
    url(r'^level/(?P<level>[\w]+)$',
        EntryLevelListView.as_view(), name='level-entry-list'),
    url(r'^level/(?P<level>[\w]+)/(?P<pk>\d+)/$',
        EntryLevelDetailView.as_view(), name='level-entry-detail'),

    url(r'^category/$',
        CategoryTemplateView.as_view(), name='category-list'),
    url(r'^category/(?P<slug>[-\w]+)/$',
        EntryCategoryView.as_view(), name='entry-category'),

    url(r'^textbook/$',
        TextbookListView.as_view(), name='textbook-list'),
    url(r'^textbook/(?P<slug>[-\w]+)/$',
        TextbookEntryListView.as_view(), name='textbook-entry-list'),

    url(r'^sitemap-entry\.xml$',
        sitemap, {'sitemaps': sitemaps_entry}, name='django.contrib.sitemaps.views.sitemap'),
]
