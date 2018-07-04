import logging

from django.utils.translation import ugettext_lazy as _
from django.views import generic


class HomeView(generic.TemplateView):
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page_title'] = _('withthai')
        return context

    def get_template_names(self):
        return 'rakmai/home.html'
