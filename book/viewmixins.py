import logging

from .models import Book


class BookContextMixin(object):
    logger = logging.getLogger(__name__)

    def dispatch(self, *args, **kwargs):
        self.book = Book.objects.get(pk=self.kwargs.get('book'))

        return super(BookContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookContextMixin, self).get_context_data(**kwargs)
        context['book'] = self.book
        return context
