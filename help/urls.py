from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from .sitemaps import (
    NoticeSitemap, PostSitemap
)
from .views import (
    PostDetailView, NoticeDetailView, NoticeListView,
    ContactCreateView, ContactDoneView,
)

app_name = 'help'

sitemaps_notice = {
    'sitemap': NoticeSitemap(),
}

sitemaps_post = {
    'sitemap': PostSitemap(),
}

urlpatterns = [
    url(r'^page/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(), name='post-detail'),

    url(r'^notice/$',
        NoticeListView.as_view(), name='notice-list'),
    url(r'^notice/(?P<pk>\d+)/$',
        NoticeDetailView.as_view(), name='notice-detail'),

    url(r'^contact/create$',
        ContactCreateView.as_view(), name='contact-create'),
    url(r'^contact/done$',
        ContactDoneView.as_view(), name='contact-done'),

    url(r'^sitemap-notice\.xml$',
        sitemap, {'sitemaps': sitemaps_notice}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap-post\.xml$',
        sitemap, {'sitemaps': sitemaps_post}, name='django.contrib.sitemaps.views.sitemap'),
]
