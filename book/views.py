import logging

from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from ipware.ip import get_ip

from rakmai.viewmixins import (
    PageableMixin, SuperuserRequiredMixin
)
from .forms import (
    ArticleForm, PageForm
)
from .models import (
    Book, Page, Article, ArticleCategory
)
from .viewmixins import (
    BookContextMixin, ArticleContextMixin
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
            .filter(slug=self.kwargs['slug'])

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


class PageCreateView(BookContextMixin, SuperuserRequiredMixin, generic.CreateView):
    logger = logging.getLogger(__name__)
    model = Page

    def get_context_data(self, **kwargs):
        context = super(PageCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Write New Page')
        return context

    def get_form_class(self):
        return PageForm

    def get_form_kwargs(self):
        kwargs = super(PageCreateView, self).get_form_kwargs()
        kwargs['parent_queryset'] = Page.objects.filter(book__slug=self.book.slug)
        return kwargs

    def form_valid(self, form):
        form.instance.book = self.book
        form.instance.book.updated = now()
        form.instance.book.save()
        form.instance.owner = self.request.user
        form.instance.view_count = 0
        form.instance.updated = now()
        form.instance.ip_address = get_ip(self.request)
        response = super(PageCreateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse('book:page-detail', args=(self.book.slug, self.object.id))

    def get_template_names(self):
        return 'book/page_create.html'


class PageUpdateView(BookContextMixin, SuperuserRequiredMixin, generic.UpdateView):
    logger = logging.getLogger(__name__)
    model = Page
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super(PageUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Edit')
        return context

    def get_form_class(self):
        return PageForm

    def get_form_kwargs(self):
        kwargs = super(PageUpdateView, self).get_form_kwargs()
        kwargs['parent_queryset'] = Page.objects.filter(book__slug=self.book.slug)
        return kwargs

    def form_valid(self, form):
        form.instance.book.updated = now()
        form.instance.book.save()
        form.instance.updated = now()
        form.instance.ip_address = get_ip(self.request)
        response = super(PageUpdateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse('book:page-detail', args=(self.book.slug, self.object.id))

    def get_template_names(self):
        return 'book/page_update.html'


class ArticleListView(PageableMixin, ArticleContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects \
            .select_related('category', 'owner') \
            .filter(category__in=ArticleCategory.objects
                    .filter(slug=self.kwargs['category'])
                    .get_descendants(include_self=True)) \
            .order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['page_title'] = _('articles')
        context['category_slug'] = self.kwargs['category']
        return context

    def get_template_names(self):
        return 'book/article_list.html'


class ArticleDetailView(generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects \
            .select_related('category', 'owner') \
            .filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['page_meta_description'] = self.object.description
        context['page_meta_keywords'] = self.object.keywords
        context['category_slug'] = self.kwargs['category']
        return context

    def get_template_names(self):
        return 'book/article_detail.html'


class ArticleCategoryListView(PageableMixin, ArticleContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects \
            .select_related('category', 'owner') \
            .filter(category__in=ArticleCategory.objects
                    .filter(slug=self.kwargs['slug'])
                    .get_descendants(include_self=True)) \
            .order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(ArticleCategoryListView, self).get_context_data(**kwargs)
        context['page_title'] = _('articles')
        context['category_slug'] = self.kwargs['category']
        return context

    def get_template_names(self):
        return 'book/article_list.html'


class ArticleCreateView(SuperuserRequiredMixin, generic.CreateView):
    logger = logging.getLogger(__name__)
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Write New Article')
        context['category_slug'] = self.kwargs['category']
        return context

    def get_form_class(self):
        return ArticleForm

    def get_form_kwargs(self):
        kwargs = super(ArticleCreateView, self).get_form_kwargs()
        kwargs['category_queryset'] = ArticleCategory.objects \
            .filter(slug=self.kwargs['category']) \
            .get_descendants(include_self=False)
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.view_count = 0
        form.instance.updated = now()
        form.instance.ip_address = get_ip(self.request)
        response = super(ArticleCreateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse('book:article-detail', args=(self.kwargs['category'], self.object.id))

    def get_template_names(self):
        return 'book/article_create.html'


class ArticleUpdateView(SuperuserRequiredMixin, generic.UpdateView):
    logger = logging.getLogger(__name__)
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Write New Article')
        context['category_slug'] = self.kwargs['category']
        return context

    def get_form_class(self):
        return ArticleForm

    def get_form_kwargs(self):
        kwargs = super(ArticleUpdateView, self).get_form_kwargs()
        kwargs['category_queryset'] = ArticleCategory.objects \
            .filter(slug=self.kwargs['category']) \
            .get_descendants(include_self=False)
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.updated = now()
        form.instance.ip_address = get_ip(self.request)
        response = super(ArticleUpdateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse('book:article-detail', args=(self.kwargs['category'], self.object.id))

    def get_template_names(self):
        return 'book/article_update.html'
