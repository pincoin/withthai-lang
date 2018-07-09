from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel

from rakmai.models import AbstractPage


class Post(SoftDeletableModel, AbstractPage):
    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('help:post-detail', args=[self.pk, self.slug])
