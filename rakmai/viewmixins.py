import logging

from django.contrib.auth.mixins import AccessMixin


class PageableMixin(object):
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        context = super(PageableMixin, self).get_context_data(**kwargs)

        start_index = int((context['page_obj'].number - 1) / self.block_size) * self.block_size
        end_index = min(start_index + self.block_size, len(context['paginator'].page_range))

        context['page_range'] = context['paginator'].page_range[start_index:end_index]
        return context

    def get_paginate_by(self, queryset):
        return self.chunk_size


class OwnerRequiredMixin(object):
    """
    Authors may edit or delete their own posts only.
    """

    def get_queryset(self):
        return super(OwnerRequiredMixin, self).get_queryset().filter(owner=self.request.user)


class SuperuserRequiredMixin(AccessMixin):
    login_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return super(SuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)

        return self.handle_no_permission()
