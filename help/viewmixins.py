import logging

from . import settings as help_settings


class HelpContextMixin(object):
    logger = logging.getLogger(__name__)

    def dispatch(self, *args, **kwargs):
        self.block_size = help_settings.HELP_BLOCK_SIZE
        self.chunk_size = help_settings.HELP_CHUNK_SIZE
        return super(HelpContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HelpContextMixin, self).get_context_data(**kwargs)
        return context
