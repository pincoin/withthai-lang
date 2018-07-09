from django.conf.urls import url

from .views import PostDetailView

app_name = 'help'

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(), name='post-detail'),
]
