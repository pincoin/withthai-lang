import logging

from django.utils.translation import ugettext_lazy as _
from django.views import generic

from .models import Entry


class EntryListView(generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entries'

    def get_queryset(self):
        queryset = Entry.objects.prefetch_related('meanings')
        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['page_title'] = _('voca')
        return context

    def get_template_names(self):
        return 'voca/entry_list.html'


class EntryDetailView(generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entry'

    def get_queryset(self):
        queryset = Entry.objects.prefetch_related('relationships', 'meanings', 'relationships__meanings')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('voca')
        return context

    def get_template_names(self):
        return 'voca/entry_detail.html'
