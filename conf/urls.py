from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from rakmai.views import HomeView

urlpatterns = [
    url(r'^$',
        HomeView.as_view(), name='home'),
    url(r'{}'.format(settings.ADMIN_URL),
        admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
