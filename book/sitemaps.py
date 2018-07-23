from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import (
    Page, Article
)


class PageSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        pages = []

        for page in Page.objects.filter(status=Page.STATUS_CHOICES.public):
            pages.append(('book:page-detail', {'book': page.book.slug, 'pk': page.id}))

        return pages

    def location(self, item):
        (name, kwargs) = item
        return reverse(name, kwargs=kwargs)


class ArticleSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        articles = []

        for article in Article.objects.filter(status=Page.STATUS_CHOICES.public):
            articles.append(('book:article-detail', {'category': article.category.slug, 'pk': article.id}))

        return articles

    def location(self, item):
        (name, kwargs) = item
        return reverse(name, kwargs=kwargs)
