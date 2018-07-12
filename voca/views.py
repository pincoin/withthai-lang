import logging

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from rakmai.viewmixins import PageableMixin
from .models import Entry, EntryCategory
from .viewmixins import SearchContextMixin, VocaContextMixin


class EntryListView(SearchContextMixin, PageableMixin, VocaContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entries'

    def get_queryset(self):
        queryset = Entry.objects.prefetch_related('meanings')

        form = self.search_form_class(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            queryset = queryset.filter(
                Q(title__icontains=q)
            )

        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['page_title'] = _('Vocabulary')
        return context

    def get_template_names(self):
        return 'voca/entry_list.html'


class EntryDetailView(SearchContextMixin, generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entry'

    def get_queryset(self):
        queryset = Entry.objects \
            .prefetch_related('meanings')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('{} - Vocabulary').format(self.object.title)
        context['entry_components'] = self.object.components \
            .prefetch_related('meanings') \
            .order_by('voca_entrycompound.position')
        context['entry_sentences'] = self.object \
            .entrysentencecompound_set \
            .select_related('from_sentence')
        return context

    def get_template_names(self):
        return 'voca/entry_detail.html'


class EntryCategoryView(SearchContextMixin, PageableMixin, VocaContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entries'

    def get_queryset(self):
        queryset = Entry.objects \
            .prefetch_related('meanings', 'categories', ) \
            .filter(categories__in=EntryCategory.objects
                    .filter(slug=self.kwargs['slug']).get_descendants(include_self=True))

        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(EntryCategoryView, self).get_context_data(**kwargs)
        context['page_title'] = _('{} Vocabulary Category').format(self.kwargs['slug'])
        return context

    def get_template_names(self):
        return 'voca/entry_list.html'
