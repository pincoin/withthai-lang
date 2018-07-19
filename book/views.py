import logging

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from .forms import PageForm
from .models import (
    Book, Page
)


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


class PageDetailView(generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'page'

    def get_queryset(self):
        return Page.objects \
            .select_related('book', 'owner') \
            .filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['page_meta_description'] = self.object.description
        context['page_meta_keywords'] = self.object.keywords
        context['book'] = self.object.book
        return context

    def get_template_names(self):
        return 'book/page_detail.html'


class PageCreateView(generic.CreateView):
    logger = logging.getLogger(__name__)
    model = Page

    def get_context_data(self, **kwargs):
        context = super(PageCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Write New Page')
        context['book'] = Book.objects.get(pk=self.kwargs['book'])
        return context

    def get_form_class(self):
        return PageForm

    def get_form_kwargs(self):
        kwargs = super(PageCreateView, self).get_form_kwargs()
        kwargs['parent_queryset'] = Page.objects.filter(book__pk=self.kwargs['book'])
        return kwargs

    def form_valid(self, form):
        response = super(PageCreateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse('book:page-detail', args=(self.kwargs['book'], self.object.id))

    def get_template_names(self):
        return 'book/page_create.html'
