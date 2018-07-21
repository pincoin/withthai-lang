from django.conf.urls import url

from .views import (
    BookListView, BookDetailView,
    PageDetailView, PageCreateView, PageUpdateView,
    ArticleListView, ArticleDetailView
)

app_name = 'book'

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
        PageCreateView.as_view(), name='article-create'),
    url(r'^article/(?P<category>[-\w]+)/(?P<pk>\d+)/update/',
        PageUpdateView.as_view(), name='article-update'),
]
