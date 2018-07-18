import logging

from django.db.models import Count
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from rakmai.viewmixins import PageableMixin
from .forms import (
    PartFilterForm, TextbookFilterForm
)
from .models import (
    Entry, EntryCategory, EntryCompound, Textbook, EntryTextbookCompound
)
from .viewmixins import (
    SearchContextMixin, VocaContextMixin
)


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
            .prefetch_related('meanings', 'entrysentence_set__entrysentencecompound_set__to_entry')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('{} - Vocabulary').format(self.object.title)

        context['entry_components'] = self.object.components \
            .prefetch_related('meanings') \
            .order_by('voca_entrycompound.position')

        context['entry_complex_words'] = EntryCompound.objects \
            .select_related('from_entry') \
            .prefetch_related('from_entry__meanings') \
            .filter(to_entry=self.object)

        context['entry_sentences'] = self.object.entrysentence_set.all()

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

        return queryset.order_by('entrycategorymembership__position')

    def get_context_data(self, **kwargs):
        context = super(EntryCategoryView, self).get_context_data(**kwargs)
        context['page_title'] = _('{} Vocabulary Category').format(self.kwargs['slug'])
        return context

    def get_template_names(self):
        return 'voca/entry_list.html'


class EntryLevelListView(SearchContextMixin, PageableMixin, VocaContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entries'
    part_filter_form_class = PartFilterForm

    def get_queryset(self):
        queryset = Entry.objects \
            .prefetch_related('meanings')

        if self.kwargs['level'] == 'beginner':
            queryset = queryset.filter(level=Entry.LEVEL_CHOICES.beginner)
        elif self.kwargs['level'] == 'intermediate':
            queryset = queryset.filter(level=Entry.LEVEL_CHOICES.intermediate)
        elif self.kwargs['level'] == 'advanced':
            queryset = queryset.filter(level=Entry.LEVEL_CHOICES.advanced)

        try:
            if 'part' in self.request.GET and int(self.request.GET['part']) > -1:
                queryset = queryset.filter(meanings__part=self.request.GET['part'])
        except ValueError:
            pass

        return queryset.order_by('-created').distinct()

    def get_context_data(self, **kwargs):
        context = super(EntryLevelListView, self).get_context_data(**kwargs)
        context['page_title'] = _('Vocabulary')
        context['part_filter_form'] = self.part_filter_form_class(
            part=self.request.GET.get('part') if self.request.GET.get('part') else '',
        )
        context['level'] = self.kwargs['level']
        return context

    def get_template_names(self):
        return 'voca/level_entry_list.html'


class LevelListView(SearchContextMixin, PageableMixin, VocaContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'levels'

    def get_queryset(self):
        queryset = Entry.objects \
            .values('level') \
            .annotate(total=Count('level'))
        return queryset.order_by('level')

    def get_context_data(self, **kwargs):
        context = super(LevelListView, self).get_context_data(**kwargs)
        context['page_title'] = _('levels')
        context['choices'] = dict(Entry._meta.get_field('level').flatchoices)
        return context

    def get_template_names(self):
        return 'voca/level_list.html'


class TextbookListView(SearchContextMixin, PageableMixin, VocaContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Textbook.objects \
            .prefetch_related('words') \
            .annotate(total=Count('words__pk'))
        return queryset.order_by('position')

    def get_context_data(self, **kwargs):
        context = super(TextbookListView, self).get_context_data(**kwargs)
        context['page_title'] = _('textbooks')
        return context

    def get_template_names(self):
        return 'voca/textbook_list.html'


class TextbookEntryListView(SearchContextMixin, PageableMixin, VocaContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'words'
    textbook_filter_form_class = TextbookFilterForm

    def get_queryset(self):
        queryset = EntryTextbookCompound.objects \
            .filter(textbook__slug=self.kwargs['slug']) \
            .select_related('textbook', 'entry') \
            .prefetch_related('entry__meanings')

        try:
            if 'chapter' in self.request.GET and int(self.request.GET['chapter']) > 0:
                queryset = queryset.filter(chapter=self.request.GET['chapter'])
        except ValueError:
            pass

        return queryset.order_by('chapter')

    def get_context_data(self, **kwargs):
        context = super(TextbookEntryListView, self).get_context_data(**kwargs)
        context['page_title'] = _('textbooks')
        context['textbook_filter_form'] = self.textbook_filter_form_class(
            chapter=self.request.GET.get('chapter') if self.request.GET.get('chapter') else '',
            slug=self.kwargs['slug'],
        )
        context['slug'] = self.kwargs['slug']
        return context

    def get_template_names(self):
        return 'voca/textbook_entry_list.html'
