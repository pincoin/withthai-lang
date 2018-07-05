from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import (
    TimeStampedModel, SoftDeletableModel
)


class Entry(SoftDeletableModel, TimeStampedModel):
    LEVEL_CHOICES = Choices(
        (0, 'beginner', _('beginner')),
        (1, 'intermediate', _('intermediate')),
        (2, 'advanced', _('advanced')),
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=250,
    )

    pronunciation = models.CharField(
        verbose_name=_('pronunciation'),
        max_length=250,
    )

    status = models.IntegerField(
        verbose_name=_('level'),
        choices=LEVEL_CHOICES,
        default=LEVEL_CHOICES.beginner,
        db_index=True,
    )

    relationships = models.ManyToManyField(
        'self',
        through='voca.EntryCompound',
        blank=True,
        related_name='related_to',
        symmetrical=False,
    )

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')


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
    )

    part = models.IntegerField(
        verbose_name=_('level'),
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

    class Meta:
        verbose_name = _('meaning')
        verbose_name_plural = _('meanings')
