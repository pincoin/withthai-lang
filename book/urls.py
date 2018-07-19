from django.conf.urls import url

from .views import (
    BookListView, BookDetailView,
    PageDetailView, PageCreateView
)

app_name = 'book'

urlpatterns = [
    url(r'^$',
        BookListView.as_view(), name='book-list'),
    url(r'^(?P<pk>\d+)/$',
        BookDetailView.as_view(), name='book-detail'),
    url(r'^(?P<book>\d+)/(?P<pk>\d+)/$',
        PageDetailView.as_view(), name='page-detail'),
    url(r'^(?P<book>\d+)/create$',
        PageCreateView.as_view(), name='page-create'),
]
