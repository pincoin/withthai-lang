import bleach
import markdown
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def mask_ip_address(ip):
    ip_class = ip.split('.')
    ip_class[1] = 'xxx'
    return '.'.join(ip_class)


@register.filter
@stringfilter
def markdownify(text):
    return mark_safe(
        bleach.clean(
            markdown.markdown(text, output_format='html5', extensions=[
                'markdown.extensions.toc',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',
                # 'markdown.extensions.fenced_code',
                # 'markdown.extensions.codehilite',
            ]),
            tags=settings.BLEACH_ALLOWED_TAGS, attributes=settings.BLEACH_ALLOWED_ATTRIBUTES, strip=True,
        )
    )


@register.filter
@stringfilter
def clean_html(text):
    return mark_safe(
        bleach.clean(
            text,
            tags=settings.BLEACH_ALLOWED_TAGS, attributes=settings.BLEACH_ALLOWED_ATTRIBUTES, strip=True,
        )
    )


@register.filter
@stringfilter
def strip_html(text):
    return bleach.clean(
        text,
        tags=[], attributes={}, strip=True,
    )
