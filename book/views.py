import logging

from django.utils.translation import ugettext_lazy as _
from django.views import generic

from .models import Book


class BookListView(generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.order_by('position', '-created')

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['page_title'] = _('books')
        return context

    def get_template_names(self):
        return 'book/book_list.html'


class BookDetailView(generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects \
            .select_related('category', 'owner') \
            .filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context

    def get_template_names(self):
        return 'book/book_detail.html'
