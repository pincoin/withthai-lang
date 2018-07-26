from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, HTML, Div
)
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Message


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['title'].help_text = False

        self.helper = FormHelper()
        self.helper.include_media = False

        fieldset = [
            '',  # Hide the legend of fieldset (HTML tag)
            'title',
            'content',
        ]

        self.helper.layout = Layout(
            Fieldset(*fieldset),
            Div(HTML('''
                <button name="submit" class="btn btn-primary btn btn-info btn-block" type="submit">
                    <i class="fa fa-pencil fa-fw"></i>
                    {}
                </button>'''.format(_('Write')))),
        )

    class Meta:
        model = Message
        fields = ['title', 'content']
