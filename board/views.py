import logging

from django.views import generic
from ipware.ip import get_ip

from .models import Message
from .viewmixins import BoardContextMixin


class MessageListView(BoardContextMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects \
            .select_related('board', 'owner') \
            .filter(board__slug=self.kwargs['slug'],
                    status=Message.STATUS_CHOICES.published) \
            .order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_template_names(self):
        return 'board/{}/message_list.html'.format(self.board.theme)


class MessageDetailView(BoardContextMixin, generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'message'

    def get_object(self, queryset=None):
        o = super(MessageDetailView, self).get_object()
        if o.owner != self.request.user and o.ip_address != get_ip(self.request):
            o.view_count += 1
        o.save()
        return o

    def get_queryset(self):
        return Message.objects \
            .select_related('owner', 'board') \
            .filter(board__slug=self.kwargs['slug'],
                    status=Message.STATUS_CHOICES.published)

    def get_context_data(self, **kwargs):
        context = super(MessageDetailView, self).get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_template_names(self):
        return 'board/{}/message_detail.html'.format(self.board.theme)
