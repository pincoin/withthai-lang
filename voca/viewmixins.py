import logging

from .forms import VocabularySearchForm

from . import settings as voca_settings


class VocaContextMixin(object):
    logger = logging.getLogger(__name__)

    def dispatch(self, *args, **kwargs):
        self.block_size = voca_settings.VOCA_BLOCK_SIZE
        self.chunk_size = voca_settings.VOCA_CHUNK_SIZE
        return super(VocaContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VocaContextMixin, self).get_context_data(**kwargs)
        return context


class SearchContextMixin(object):
    logger = logging.getLogger(__name__)

    search_form_class = VocabularySearchForm

    def get_context_data(self, **kwargs):
        context = super(SearchContextMixin, self).get_context_data(**kwargs)

        context['search_form'] = self.search_form_class(
            q=self.request.GET.get('q') if self.request.GET.get('q') else '')

        return context
