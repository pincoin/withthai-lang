from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from .sitemaps import (
    PageSitemap, ArticleSitemap
)
from .views import (
    BookListView, BookDetailView,
    PageDetailView, PageCreateView, PageUpdateView,
    ArticleListView, ArticleDetailView, ArticleCategoryListView, ArticleCreateView,
)

app_name = 'book'

sitemaps_page = {
    'sitemap': PageSitemap(),
}

sitemaps_article = {
    'sitemap': ArticleSitemap(),
}

urlpatterns = [
    url(r'^$',
        BookListView.as_view(), name='book-list'),
    url(r'^(?P<slug>[-\w]+)/$',
        BookDetailView.as_view(), name='book-detail'),

    url(r'^(?P<book>[-\w]+)/(?P<pk>\d+)/$',
        PageDetailView.as_view(), name='page-detail'),
    url(r'^(?P<book>[-\w]+)/create$',
        PageCreateView.as_view(), name='page-create'),
    url(r'^(?P<book>[-\w]+)/(?P<pk>\d+)/update/',
        PageUpdateView.as_view(), name='page-update'),

    url(r'^article/(?P<category>[-\w]+)/$',
        ArticleListView.as_view(), name='article-list'),
    url(r'^article/(?P<category>[-\w]+)/(?P<pk>\d+)/$',
        ArticleDetailView.as_view(), name='article-detail'),
    url(r'^article/(?P<category>[-\w]+)/create$',
        ArticleCreateView.as_view(), name='article-create'),
    url(r'^article/(?P<category>[-\w]+)/(?P<pk>\d+)/update/',
        PageUpdateView.as_view(), name='article-update'),
    url(r'^article/(?P<category>[-\w]+)/category/(?P<slug>[-\w]+)$',
        ArticleCategoryListView.as_view(), name='article-category-list'),

    url(r'^sitemap-page\.xml$',
        sitemap, {'sitemaps': sitemaps_page}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap-article\.xml$',
        sitemap, {'sitemaps': sitemaps_article}, name='django.contrib.sitemaps.views.sitemap'),
]
