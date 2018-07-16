from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import EntryTextbookCompound


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
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': 'True',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        slug = kwargs.pop('slug', '')
        chapter = kwargs.pop('chapter', '1')

        super(TextbookFilterForm, self).__init__(*args, **kwargs)

        chapters = EntryTextbookCompound.objects \
            .filter(textbook__slug=slug) \
            .order_by('chapter') \
            .values_list('chapter', flat=True) \
            .distinct()

        self.fields['chapter'].choices = [('0', '전체')] + list(map(lambda x: (str(x), str(x)+'과'), chapters))
        self.fields['chapter'].initial = chapter
