import logging

from django.views import generic

from .models import Post


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
