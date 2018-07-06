import logging

from django.utils.translation import ugettext_lazy as _
from django.views import generic

from .models import Entry


class VocaListView(generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entries'

    def get_queryset(self):
        queryset = Entry.objects.all()

        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(VocaListView, self).get_context_data(**kwargs)
        context['page_title'] = _('voca')
        return context

    def get_template_names(self):
        return 'voca/voca_list.html'


class VocaDetailView(generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'entry'
    model = Entry

    def get_context_data(self, **kwargs):
        context = super(VocaDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('voca')
        return context

    def get_template_names(self):
        return 'voca/voca_detail.html'
