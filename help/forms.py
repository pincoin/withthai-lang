from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, Div, Submit
)
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)

        self.fields['title'].help_text = False

        self.helper = FormHelper()
        self.helper.include_media = False

        # horizontal grid form
        self.helper.form_class = 'form-horizontal'  # Appends `row` class to `div` surrounding label and form field
        self.helper.label_class = 'col-2 col-form-label'
        self.helper.field_class = 'col-10'

        fieldset = [
            '',  # Hide the legend of fieldset (HTML tag)
            'title',
            'fullname',
            'email',
            'phone',
            'content'
        ]

        self.helper.layout = Layout(
            Fieldset(*fieldset),
            Div(
                Submit('submit', _('Write'), css_class='btn btn-info btn-block'),
                css_class='my-3',
            )
        )

    class Meta:
        model = ContactMessage
        fields = ('title', 'fullname', 'email', 'phone', 'content')
