from django.conf.urls import url

from .views import (
    VocaListView, VocaDetailView
)

app_name = 'voca'

urlpatterns = [
    url(r'^entries$',
        VocaListView.as_view(), name='entry-list'),
    url(r'^entries/(?P<slug>[-\w]+)/$',
        VocaDetailView.as_view(), name='entry-detail'),
]
