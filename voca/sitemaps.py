from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import (
    Entry
)


class EntrySitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        entries = []

        for entry in Entry.objects.all():
            entries.append(('voca:entry-detail', {'pk': entry.id}))

        return entries

    def location(self, item):
        (name, kwargs) = item
        return reverse(name, kwargs=kwargs)
