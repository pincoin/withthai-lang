from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from mptt.admin import DraggableMPTTAdmin

from .models import (
    Entry, EntryMeaning, EntryCategory
)


class EntryMeaningInlineFormset(BaseInlineFormSet):
    def get_queryset(self):
        return super(EntryMeaningInlineFormset, self).get_queryset().order_by('position')


class EntryMeaningInline(admin.TabularInline):
    model = EntryMeaning
    extra = 1
    formset = EntryMeaningInlineFormset


class EntryCompoundInline(admin.TabularInline):
    model = Entry.relationships.through
    extra = 1
    fk_name = 'from_entry'


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pronunciation')
    list_display_links = ('title',)
    list_filter = ('level',)
    search_fields = ('title',)
    fields = ('level', 'title', 'pronunciation', 'category', 'description')
    readonly_fields = ('is_removed',)
    inlines = [EntryMeaningInline, EntryCompoundInline]


class EntryCategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20


admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryCategory, EntryCategoryAdmin)
