from django import forms
from django.utils.translation import ugettext_lazy as _


class VocabularySearchForm(forms.Form):
    q = forms.CharField(
        label=_('lookup word'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('lookup word'),
                'required': 'True',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        q = kwargs.pop('q', '')

        super(VocabularySearchForm, self).__init__(*args, **kwargs)

        self.fields['q'].initial = q
