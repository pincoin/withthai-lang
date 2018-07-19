from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe
from mptt.utils import get_cached_trees

from ..models import (
    EntryCategory, Textbook
)

register = template.Library()


class CategoryNode(template.Node):
    def __init__(self, nodes, tree_query_set):
        self.nodes = nodes
        self.tree_query_set = tree_query_set

    def _render_category(self, context, category):
        nodes = []
        context.push()

        for child in category.get_children():
            nodes.append(self._render_category(context, child))

        context['category'] = category
        context['children'] = mark_safe(''.join(nodes))

        rendered = self.nodes.render(context)

        context.pop()
        return rendered

    def render(self, context):
        roots = get_cached_trees(self.tree_query_set)

        nodes = [self._render_category(context, category) for category in roots]
        return ''.join(nodes)


@register.tag
def voca_categories(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{} tag does not require an additional argument.'.format(token.split_contents()[0])
        )

    nodes = parser.parse(('end_voca_categories',))
    parser.delete_first_token()

    cache_key = 'voca.templatetags.voca_tags.voca_categories()'
    cache_time = settings.CACHE_TIME_LONG

    tree_query_set = cache.get(cache_key)

    if not tree_query_set:
        try:
            tree_query_set = EntryCategory.objects.all()
            cache.set(cache_key, tree_query_set, cache_time)
        except EntryCategory.DoesNotExist:
            tree_query_set = None

    return CategoryNode(nodes, tree_query_set)


@register.simple_tag
def get_textbooks(count=5):
    cache_key = 'voca.templatetags.voca_tags.get_textbook()'
    cache_time = settings.CACHE_TIME_LONG

    textbooks = cache.get(cache_key)

    if not textbooks:
        textbooks = Textbook.objects.all().order_by('position')[:count]
        cache.set(cache_key, textbooks, cache_time)

    return textbooks
