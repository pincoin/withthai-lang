import logging

from . import settings as book_settings
from .models import Book


class BookContextMixin(object):
    logger = logging.getLogger(__name__)

    def dispatch(self, *args, **kwargs):
        self.book = Book.objects.get(slug=self.kwargs.get('book'))

        return super(BookContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookContextMixin, self).get_context_data(**kwargs)
        context['book'] = self.book
        return context


class ArticleContextMixin(object):
    logger = logging.getLogger(__name__)

    def dispatch(self, *args, **kwargs):
        self.block_size = book_settings.ARTICLE_BLOCK_SIZE
        self.chunk_size = book_settings.ARTICLE_CHUNK_SIZE
        return super(ArticleContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleContextMixin, self).get_context_data(**kwargs)
        return context
