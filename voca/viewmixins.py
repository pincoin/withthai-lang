import logging

from .forms import VocabularySearchForm


class SearchContextMixin(object):
    logger = logging.getLogger(__name__)

    search_form_class = VocabularySearchForm

    def get_context_data(self, **kwargs):
        context = super(SearchContextMixin, self).get_context_data(**kwargs)

        context['search_form'] = self.search_form_class(
            q=self.request.GET.get('q') if self.request.GET.get('q') else '')

        return context
