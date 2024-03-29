from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import (
    TimeStampedModel, SoftDeletableModel
)
from mptt.fields import TreeForeignKey

from rakmai.models import AbstractCategory


class Entry(SoftDeletableModel, TimeStampedModel):
    LEVEL_CHOICES = Choices(
        (0, 'beginner', _('beginner')),
        (1, 'intermediate', _('intermediate')),
        (2, 'advanced', _('advanced')),
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )

    pronunciation = models.CharField(
        verbose_name=_('pronunciation'),
        max_length=250,
    )

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    level = models.IntegerField(
        verbose_name=_('level'),
        choices=LEVEL_CHOICES,
        default=LEVEL_CHOICES.beginner,
        db_index=True,
    )

    categories = models.ManyToManyField(
        'voca.EntryCategory',
        through='voca.EntryCategoryMembership',
        blank=True,
        symmetrical=False,
    )

    components = models.ManyToManyField(
        'self',
        through='voca.EntryCompound',
        blank=True,
        symmetrical=False,
    )

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __str__(self):
        return self.title


class EntryCompound(models.Model):
    from_entry = models.ForeignKey(
        'voca.Entry',
        related_name='from_entry',
        db_index=True,
        on_delete=models.CASCADE,
    )

    to_entry = models.ForeignKey(
        'voca.Entry',
        verbose_name=_('compound word'),
        related_name='to_entry',
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    class Meta:
        verbose_name = _('compound word')
        verbose_name_plural = _('compound words')
        ordering = ('position',)


class EntryMeaning(TimeStampedModel):
    PART_CHOICES = Choices(
        (0, 'noun', _('noun')),
        (1, 'pronoun', _('pronoun')),
        (2, 'verb', _('verb')),
        (3, 'modifier', _('modifier')),
        (4, 'preposition', _('preposition')),
        (5, 'conjunction', _('conjunction')),
        (6, 'interjection', _('interjection')),
        (7, 'classifier', _('classifier')),
    )

    part = models.IntegerField(
        verbose_name=_('part of speech'),
        choices=PART_CHOICES,
        default=PART_CHOICES.noun,
        db_index=True,
    )

    entry = models.ForeignKey(
        'voca.Entry',
        verbose_name=_('entry'),
        related_name='meanings',
        on_delete=models.CASCADE,
    )

    meaning = models.CharField(
        verbose_name=_('meaning'),
        max_length=250,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    class Meta:
        verbose_name = _('meaning')
        verbose_name_plural = _('meanings')
        ordering = ['position']

    def __str__(self):
        return '{} {}'.format(self.entry.title, self.meaning)


class EntryCategory(AbstractCategory):
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    class Meta:
        verbose_name = _('entry category')
        verbose_name_plural = _('entry categories')

    def __str__(self):
        return self.title


class EntryCategoryMembership(models.Model):
    entry = models.ForeignKey(
        'voca.Entry',
        db_index=True,
        on_delete=models.CASCADE,
    )

    category = TreeForeignKey(
        'voca.EntryCategory',
        verbose_name=_('entry category'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    class Meta:
        verbose_name = _('category membership')
        verbose_name_plural = _('category memberships')
        ordering = ['position']


class EntrySentence(SoftDeletableModel, TimeStampedModel):
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )

    pronunciation = models.CharField(
        verbose_name=_('pronunciation'),
        max_length=250,
    )

    meaning = models.TextField(
        verbose_name=_('meaning'),
        blank=True,
    )

    words = models.ManyToManyField(
        'voca.Entry',
        through='voca.EntrySentenceCompound',
        blank=True,
        symmetrical=False,
    )

    class Meta:
        verbose_name = _('entry sentence')
        verbose_name_plural = _('entry sentences')

    def __str__(self):
        return self.title


class EntrySentenceCompound(models.Model):
    from_sentence = models.ForeignKey(
        'voca.EntrySentence',
        db_index=True,
        on_delete=models.CASCADE,
    )

    to_entry = models.ForeignKey(
        'voca.Entry',
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    class Meta:
        verbose_name = _('word')
        verbose_name_plural = _('words')
        ordering = ['position']


class Textbook(TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'public', _('public')),
        (1, 'private', _('private')),
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    author = models.CharField(
        verbose_name=_('author'),
        max_length=255,
    )

    publisher = models.CharField(
        verbose_name=_('publisher'),
        max_length=255,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    words = models.ManyToManyField(
        'voca.Entry',
        through='voca.EntryTextbookCompound',
        blank=True,
        symmetrical=False,
    )

    chapter = models.IntegerField(
        verbose_name=_('chapter'),
    )

    status = models.IntegerField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.public,
        db_index=True,
    )

    class Meta:
        verbose_name = _('textbook')
        verbose_name_plural = _('textbooks')
        ordering = ['position', ]

    def __str__(self):
        return self.title


class EntryTextbookCompound(models.Model):
    textbook = models.ForeignKey(
        'voca.Textbook',
        verbose_name=_('textbook'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    entry = models.ForeignKey(
        'voca.Entry',
        verbose_name=_('entry'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    chapter = models.IntegerField(
        verbose_name=_('chapter'),
    )

    page = models.IntegerField(
        verbose_name=_('page'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('textbook word')
        verbose_name_plural = _('textbook words')
        ordering = ['chapter', 'page']
