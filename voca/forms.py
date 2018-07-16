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


class TextbookFilterForm(forms.Form):
    chapter = forms.ChoiceField(
        choices=(
            ('1', '1'),
            ('2', '2'),
        ),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': 'True',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        chapter = kwargs.pop('chapter', '1')

        super(TextbookFilterForm, self).__init__(*args, **kwargs)

        self.fields['chapter'].initial = chapter
