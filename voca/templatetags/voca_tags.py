from django import template
from django.utils.safestring import mark_safe
from mptt.utils import get_cached_trees

from ..models import (
    EntryCategory, Textbook
)

register = template.Library()


class CategoryNode(template.Node):
    def __init__(self, nodes):
        self.nodes = nodes
        self.tree_query_set = None

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
        try:
            self.tree_query_set = EntryCategory.objects.all()
        except EntryCategory.DoesNotExist:
            pass

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

    return CategoryNode(nodes)


@register.simple_tag
def get_textbooks(count=5):
    textbooks = Textbook.objects.all().order_by('position')[:count]
    return textbooks
