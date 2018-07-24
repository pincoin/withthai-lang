import logging

from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from ipware.ip import get_ip

from rakmai.viewmixins import PageableMixin
from .forms import ContactMessageForm
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


class ContactDoneView(generic.TemplateView):
    pass


class ContactCreateView(generic.CreateView):
    logger = logging.getLogger(__name__)
    form_class = ContactMessageForm

    def get_context_data(self, **kwargs):
        context = super(ContactCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Contact')
        return context

    def form_valid(self, form):
        form.instance.updated = now()
        form.instance.ip_address = get_ip(self.request)
        form.instance.accept_language = self.request.META['HTTP_ACCEPT_LANGUAGE']
        form.instance.user_agent = self.request.META['HTTP_USER_AGENT']
        response = super(ContactCreateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse('help:contact-done')

    def get_template_names(self):
        return 'help/contact_create.html'
