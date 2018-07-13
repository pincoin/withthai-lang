from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import SoftDeletableModel

from rakmai.models import AbstractPage


class Post(SoftDeletableModel, AbstractPage):
    FORMAT_CHOICES = Choices(
        (0, 'html', _('html')),
        (1, 'markdown', _('markdown')),
        (2, 'text', _('text')),
    )

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

    markup = models.IntegerField(
        verbose_name=_('markup'),
        choices=FORMAT_CHOICES,
        default=FORMAT_CHOICES.html,
    )

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('help:post-detail', args=[self.pk])


class NoticeMessage(SoftDeletableModel, AbstractPage):
    FORMAT_CHOICES = Choices(
        (0, 'html', _('html')),
        (1, 'markdown', _('markdown')),
        (2, 'text', _('text')),
    )

    CATEGORY_CHOICES = Choices(
        (0, 'common', _('Common')),
    )

    content = models.TextField(
        verbose_name=_('content'),
    )

    markup = models.IntegerField(
        verbose_name=_('markup'),
        choices=FORMAT_CHOICES,
        default=FORMAT_CHOICES.html,
    )

    category = models.IntegerField(
        verbose_name=_('category'),
        choices=CATEGORY_CHOICES,
        default=CATEGORY_CHOICES.common,
        db_index=True,
    )

    class Meta:
        verbose_name = _('notice')
        verbose_name_plural = _('notice')
        ordering = ['-created']

    def __str__(self):
        return self.title
