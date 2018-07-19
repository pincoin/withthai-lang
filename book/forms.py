from django import forms
from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from .models import (
    Page
)


class PageForm(forms.ModelForm):
    parent = TreeNodeChoiceField(None)

    def __init__(self, *args, **kwargs):
        self.parent_queryset = kwargs.pop('parent_queryset', None)

        super(PageForm, self).__init__(*args, **kwargs)

        self.fields['parent'].queryset = self.parent_queryset
        self.fields['parent'].required = False
        self.fields['parent'].label = _('parent')

    class Meta:
        model = Page
        fields = ('title', 'parent', 'content', 'content1', 'content2', 'keywords', 'description', 'status')
