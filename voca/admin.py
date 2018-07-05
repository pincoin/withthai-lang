from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from .models import (
    Entry, EntryCompound, EntryMeaning
)


class EntryMeaningInlineFormset(BaseInlineFormSet):
    def get_queryset(self):
        return super(EntryMeaningInlineFormset, self).get_queryset().order_by('position')


class EntryMeaningInline(admin.TabularInline):
    model = EntryMeaning
    extra = 1
    formset = EntryMeaningInlineFormset


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pronunciation')
    list_display_links = ('title',)
    inlines = [EntryMeaningInline, ]


class EntryCompoundAdmin(admin.ModelAdmin):
    pass


admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryCompound, EntryCompoundAdmin)
