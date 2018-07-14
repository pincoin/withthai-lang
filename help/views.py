import logging

from django.utils.translation import ugettext_lazy as _
from django.views import generic

from rakmai.viewmixins import PageableMixin
from .models import (
    Post, NoticeMessage
)
from .viewmixins import HelpContextMixin


class PostDetailView(generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.select_related('owner')

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['page_meta_description'] = self.object.description
        context['page_meta_keywords'] = self.object.keywords
        return context

    def get_template_names(self):
        return 'help/post_detail.html'


class NoticeListView(PageableMixin, HelpContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'messages'

    def get_queryset(self):
        return NoticeMessage.objects.all().order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(NoticeListView, self).get_context_data(**kwargs)
        context['page_title'] = _('Notice')
        return context

    def get_template_names(self):
        return 'help/notice_list.html'


class NoticeDetailView(generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'post'

    def get_queryset(self):
        return NoticeMessage.objects.select_related('owner')

    def get_context_data(self, **kwargs):
        context = super(NoticeDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('{} : Notice').format(self.object.title)
        context['page_meta_description'] = self.object.description
        context['page_meta_keywords'] = self.object.keywords
        return context

    def get_template_names(self):
        return 'help/notice_detail.html'
