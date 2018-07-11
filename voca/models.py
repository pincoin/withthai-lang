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

    category = TreeForeignKey(
        'voca.EntryCategory',
        verbose_name=_('entry category'),
        related_name=_('entries'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    relationships = models.ManyToManyField(
        'self',
        through='voca.EntryCompound',
        blank=True,
        related_name='components',
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
        related_name=_('from_entry'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    to_entry = models.ForeignKey(
        'voca.Entry',
        related_name=_('to_entry'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('position'),
    )

    class Meta:
        verbose_name = _('compound word')
        verbose_name_plural = _('compound words')
        ordering = ['position']


class EntryMeaning(TimeStampedModel):
    PART_CHOICES = Choices(
        (0, 'noun', _('noun')),
        (1, 'pronoun', _('pronoun')),
        (2, 'verb', _('verb')),
        (3, 'modifier', _('modifier')),
        (4, 'preposition', _('verb')),
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

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    relationships = models.ManyToManyField(
        'self',
        through='voca.EntrySentenceCompound',
        blank=True,
        related_name='components',
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
        related_name=_('from_sentence'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    to_entry = models.ForeignKey(
        'voca.Entry',
        related_name=_('to_entry_sentence'),
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
