from django import template
from django.conf import settings
from django.core.cache import cache
from django.template import Variable
from django.utils.safestring import mark_safe
from mptt.utils import get_cached_trees

from ..models import Page

register = template.Library()


class PageNode(template.Node):
    def __init__(self, nodes, book):
        self.nodes = nodes
        self.book = Variable(book)
        self.tree_query_set = None
        self.request = Variable('request')

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
        book = self.book.resolve(context)
        request = self.request.resolve(context)

        if request.user.is_superuser:
            tree_query_set = Page.objects \
                .select_related('book') \
                .filter(book__pk=book.id)
        else:
            cache_key = 'book.templatetags.book_tags.book_toc({})'.format(book.id)
            cache_time = settings.CACHE_TIME_VERY_SHORT

            tree_query_set = cache.get(cache_key)

            if not tree_query_set:
                try:
                    tree_query_set = Page.objects \
                        .select_related('book') \
                        .filter(book__pk=book.id, status=Page.STATUS_CHOICES.public)
                    cache.set(cache_key, tree_query_set, cache_time)
                except Page.DoesNotExist:
                    pass

        roots = get_cached_trees(tree_query_set)

        nodes = [self._render_category(context, category) for category in roots]
        return ''.join(nodes)


@register.tag
def book_toc(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, book = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{} tag does not require an additional argument.'.format(token.split_contents()[0])
        )

    nodes = parser.parse(('end_book_toc',))
    parser.delete_first_token()

    return PageNode(nodes, book)


@register.simple_tag
def get_ancestor_path(page_id):
    # breadcrumb
    return get_cached_trees(Page.objects.get(pk=page_id).get_ancestors(include_self=False))
