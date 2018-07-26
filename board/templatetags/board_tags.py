from django import template
from django.conf import settings
from django.core.cache import cache

from ..models import Message

register = template.Library()


@register.simple_tag
def get_messages(board_slug, count=5):
    cache_key = 'board.templatetags.board_tags.get_messages()'
    cache_time = settings.CACHE_TIME_SHORT

    messages = cache.get(cache_key)
    if not messages:
        messages = Message.objects \
                       .select_related('board', 'owner') \
                       .filter(board__slug=board_slug,
                               status=Message.STATUS_CHOICES.published) \
                       .order_by('-created')[:count]
        cache.set(cache_key, messages, cache_time)

    return messages
