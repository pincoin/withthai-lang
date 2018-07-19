from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import (
    Page
)


class PageForm(forms.ModelForm):
    parent = TreeNodeChoiceField(None)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Page
        fields = ('title', 'content', 'keywords', 'description', 'parent', 'status')
