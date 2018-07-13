import bleach
import markdown
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def markdownify(text):
    return mark_safe(
        bleach.clean(
            markdown.markdown(text, output_format='html5', extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.fenced_code',
                # 'markdown.extensions.codehilite',
                'markdown.extensions.toc',
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
