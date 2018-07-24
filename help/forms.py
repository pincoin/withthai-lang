import json
import urllib

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, Div, Submit, HTML
)
from django import forms
from django.conf import settings
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
            'content',
            HTML('<div class="row">'
                 '<div class="col offset-md-2">'
                 '<div class="g-recaptcha" data-sitekey="{}"></div>'
                 '</div>'
                 '</div>'
                 .format(settings.GOOGLE_RECAPTCHA['site_key'])),
        ]

        self.helper.layout = Layout(
            Fieldset(*fieldset),
            Div(
                Submit('submit', _('Write'), css_class='btn btn-info btn-block'),
                css_class='my-3',
            )
        )

    def clean(self):
        cleaned_data = super(ContactMessageForm, self).clean()

        captcha_response = self.data.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA['secret_key'],
            'response': captcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        captcha_response = urllib.request.urlopen(req)
        result = json.loads(captcha_response.read().decode())

        if not result['success']:
            raise forms.ValidationError(_('Invalid reCAPTCHA. Please try again.'))

        return cleaned_data

    class Media:
        js = ('https://www.google.com/recaptcha/api.js',)

    class Meta:
        model = ContactMessage
        fields = ('title', 'fullname', 'email', 'phone', 'content')
