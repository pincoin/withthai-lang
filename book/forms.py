from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, Div, Submit
)
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

        self.helper = FormHelper()
        self.helper.include_media = False

        # horizontal grid form
        self.helper.form_class = 'form-horizontal'  # Appends `row` class to `div` surrounding label and form field
        self.helper.label_class = 'col-2 col-form-label'
        self.helper.field_class = 'col-10'

        fieldset = [
            '',  # Hide the legend of fieldset (HTML tag)
            'status',
            'title',
            'parent',
            'content',
            'content1',
            'content2',
            'image',
            'youtube',
            'keywords',
            'description',
        ]

        self.helper.layout = Layout(
            Fieldset(*fieldset),
            Div(
                Submit('submit', _('Write'), css_class='btn btn-info btn-block'),
                css_class='my-3',
            )
        )

    class Meta:
        model = Page
        fields = ('title', 'parent', 'image', 'youtube', 'content', 'content1', 'content2',
                  'keywords', 'description', 'status')
