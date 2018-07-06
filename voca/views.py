import logging

from django.utils.translation import ugettext_lazy as _
from django.views import generic


class VocaListView(generic.TemplateView):
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        context = super(VocaListView, self).get_context_data(**kwargs)
        context['page_title'] = _('voca')
        return context

    def get_template_names(self):
        return 'voca/voca_list.html'
