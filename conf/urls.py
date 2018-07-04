from django.conf import settings
from django.conf.urls import url
from django.contrib import admin

from .views import HomeView

urlpatterns = [
    url(r'^$',
        HomeView.as_view(), name='home'),
    url(r'{}'.format(settings.ADMIN_URL),
        admin.site.urls),
]
