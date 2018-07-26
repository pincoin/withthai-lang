import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from ipware.ip import get_ip

from rakmai.viewmixins import (
    PageableMixin, OwnerRequiredMixin
)
from .forms import MessageForm
from .models import (
    Message
)
from .viewmixins import BoardContextMixin


class MessageListView(PageableMixin, BoardContextMixin, generic.ListView):
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


class MessageCreateView(LoginRequiredMixin, BoardContextMixin, generic.CreateView):
    logger = logging.getLogger(__name__)
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super(MessageCreateView, self).get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def form_valid(self, form):
        # These must be set before `form_valid()` which saves Message model instance.
        # Then, `self.object` is available in order to save attachments.
        form.instance.board = self.board
        form.instance.ip_address = get_ip(self.request)
        form.instance.owner = self.request.user
        form.instance.nickname = self.request.user.username

        # The fields such as created, updated, status, view_count are filled by default.
        response = super(MessageCreateView, self).form_valid(form)

        return response

    def get_success_url(self):
        return reverse('board:message-detail', args=(self.object.board.slug, self.object.id,))

    def get_template_names(self):
        return 'board/{}/message_create.html'.format(self.board.theme)


class MessageUpdateView(OwnerRequiredMixin, LoginRequiredMixin, BoardContextMixin, generic.UpdateView):
    logger = logging.getLogger(__name__)
    model = Message
    context_object_name = 'message'

    def get_form_class(self):
        return MessageForm

    def get_form_kwargs(self):
        # Pass 'self.request' object to MessageForm instance
        kwargs = super(MessageUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['categories'] = self.board.categories.all()
        return kwargs

    def form_valid(self, form):
        response = super(MessageUpdateView, self).form_valid(form)

        return response

    def get_success_url(self):
        return reverse('board:message-detail', args=(self.object.board.slug, self.object.id,))

    def get_template_names(self):
        return 'board/{}/message_update.html'.format(self.board.theme)


class MessageDeleteView(OwnerRequiredMixin, LoginRequiredMixin, BoardContextMixin, generic.DeleteView):
    logger = logging.getLogger(__name__)
    model = Message
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super(MessageDeleteView, self).get_context_data(**kwargs)
        context['board'] = self.board  # Fetched by BoardContextMixin.dispatch()
        return context

    def get_success_url(self):
        return reverse('board:message-list', args=(self.object.board.slug,))

    def get_template_names(self):
        return 'board/{}/message_confirm_delete.html'.format(self.board.theme)
