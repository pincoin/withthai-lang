from django import template

from ..models import NoticeMessage

register = template.Library()


@register.simple_tag
def get_notice(count=5):
    notices = NoticeMessage.objects.all().order_by('-created')[:count]
    return notices
