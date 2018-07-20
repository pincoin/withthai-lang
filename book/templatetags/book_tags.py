from django import template
from django.conf import settings
from django.core.cache import cache
from django.template import Variable
from django.utils.safestring import mark_safe
from mptt.utils import get_cached_trees

from ..models import Page, ArticleCategory

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


class PageListItem:
    def __init__(self, tree_query_set, indent):
        self.tree_query_set = tree_query_set
        self.indent = indent

    def _get_children(self, page_item):
        page_item.indent = self.indent * (page_item.level + 1)

        nodes = [page_item]

        for child in page_item.get_children():
            nodes.extend(self._get_children(child))

        return nodes

    def get_list(self):
        items = []

        for page_item in self.tree_query_set:
            items.extend(self._get_children(page_item))

        return items


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
def get_page_ancestor_path(page_id):
    # breadcrumb
    return get_cached_trees(Page.objects.get(pk=page_id).get_ancestors(include_self=False))


@register.simple_tag
def get_adjacent_pages(book_id, page_id):
    tree_set = get_cached_trees(Page.objects
                                .select_related('book')
                                .filter(book__pk=book_id, status=Page.STATUS_CHOICES.public))
    tree_list = PageListItem(tree_set, 0).get_list()

    i = 0
    for i, p in enumerate(tree_list):
        if p.id == page_id:
            break

    return {
        'previous_page': tree_list[i - 1] if i > 0 else None,
        'next_page': tree_list[i + 1] if i + 1 < len(tree_list) else None,
    }


class CategoryNode(template.Node):
    def __init__(self, nodes, category_slug):
        self.nodes = nodes
        self.category_slug = Variable(category_slug)

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
        category_slug = self.category_slug.resolve(context)

        cache_key = 'book.templatetags.book_tags.article_categories({})'.format(category_slug)
        cache_time = settings.CACHE_TIME_LONG

        tree_query_set = cache.get(cache_key)

        if not tree_query_set:
            try:
                tree_query_set = ArticleCategory.objects.filter(slug=category_slug).get_descendants(include_self=False)
                cache.set(cache_key, tree_query_set, cache_time)
            except ArticleCategory.DoesNotExist:
                tree_query_set = None

        roots = get_cached_trees(tree_query_set)

        nodes = [self._render_category(context, category) for category in roots]
        return ''.join(nodes)


@register.tag
def article_categories(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, category_slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{} tag does not require an additional argument.'.format(token.split_contents()[0])
        )

    nodes = parser.parse(('end_article_categories',))
    parser.delete_first_token()

    return CategoryNode(nodes, category_slug)


@register.simple_tag
def get_article_ancestor_path(category_id):
    # breadcrumb
    return ArticleCategory.objects.get(pk=category_id).get_ancestors(include_self=True)
