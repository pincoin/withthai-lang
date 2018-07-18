from django import template
from django.conf import settings
from django.core.cache import cache

from ..models import NoticeMessage

register = template.Library()


@register.simple_tag
def get_notice(count=5):
    cache_key = 'voca.templatetags.voca_tags.get_notice()'
    cache_time = settings.CHACHE_TIME_SHORT

    notices = cache.get(cache_key)
    if not notices:
        notices = NoticeMessage.objects.all().order_by('-created')[:count]
        cache.set(cache_key, notices, cache_time)

    return notices
