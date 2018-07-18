import logging

from django.views import generic

from .models import Book


class BookList(generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.all()

        return queryset
