from django.conf.urls import url

from .views import VocaListView

app_name = 'voca'

urlpatterns = [
    url(r'^$',
        VocaListView.as_view(), name='voca_list'),
]
