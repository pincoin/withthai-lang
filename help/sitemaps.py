from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import (
    NoticeMessage, Post
)


class NoticeSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        messages = []

        for message in NoticeMessage.objects.filter(is_removed=False):
            messages.append(('help:notice-detail', {'pk': message.id}))

        return messages

    def location(self, item):
        (name, kwargs) = item
        return reverse(name, kwargs=kwargs)


class PostSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        posts = []

        for post in Post.objects.filter(is_removed=False):
            posts.append(('help:post-detail', {'slug': post.slug}))

        return posts

    def location(self, item):
        (name, kwargs) = item
        return reverse(name, kwargs=kwargs)
