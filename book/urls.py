from django.conf.urls import url

from .views import (
    BookListView
)

app_name = 'book'

urlpatterns = [
    url(r'^$',
        BookListView.as_view(), name='book-list'),
    url(r'^(?P<pk>\d+)/$',
        BookListView.as_view(), name='book-detail'),
    url(r'^(?P<book>\d+)/(?P<pk>\d+)/$',
        BookListView.as_view(), name='page-detail'),
]
