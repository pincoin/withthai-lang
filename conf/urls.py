from django.conf import settings
from django.conf.urls import (
    url, include
)
from django.conf.urls.static import static
from django.contrib import admin

from rakmai.views import HomeView

urlpatterns = [
    url(r'^$',
        HomeView.as_view(), name='home'),
    url(r'{}'.format(settings.ADMIN_URL),
        admin.site.urls),
    url(r'^voca/', include('voca.urls', namespace='voca')),
    url(r'^book/', include('book.urls', namespace='book')),
    url(r'^help/', include('help.urls', namespace='help'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.GOOGLE_OTP_ENABLED:
    from django_otp.admin import OTPAdminSite

    admin.site.__class__ = OTPAdminSite
