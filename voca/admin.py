from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin

from .models import (
    Entry, EntryMeaning, EntryCategory, EntrySentence, Textbook
)


class EntryMeaningInline(admin.TabularInline):
    model = EntryMeaning
    extra = 1


class EntryCompoundInline(admin.TabularInline):
    model = Entry.components.through
    extra = 1
    fk_name = 'from_entry'
    raw_id_fields = ('to_entry',)


class EntryCategoryInline(admin.TabularInline):
    model = Entry.categories.through
    extra = 1
    fk_name = 'entry'
    raw_id_fields = ('category',)


class EntrySentenceCompoundInline(admin.TabularInline):
    model = EntrySentence.words.through
    extra = 1
    fk_name = 'from_sentence'
    raw_id_fields = ('to_entry',)


class EntryTextbookCompoundInline(admin.TabularInline):
    model = Textbook.words.through
    extra = 1
    fk_name = 'textbook'
    raw_id_fields = ('entry',)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'meanings')
    list_display_links = ('title',)
    list_filter = ('level',)
    search_fields = ('title',)
    fields = ('level', 'title', 'pronunciation', 'description')
    readonly_fields = ('is_removed',)
    inlines = [EntryMeaningInline, EntryCompoundInline, EntryCategoryInline]

    def get_queryset(self, request):
        return super(EntryAdmin, self).get_queryset(request) \
            .prefetch_related('meanings')

    def meanings(self, obj):
        return obj.meanings.first().meaning

    meanings.short_description = _('meanings')


class EntryCategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20


class EntrySentenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'pronunciation')
    list_display_links = ('title',)
    search_fields = ('title',)
    fields = ('title', 'pronunciation', 'meaning')
    readonly_fields = ('is_removed',)
    inlines = [EntrySentenceCompoundInline]


class TextbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'slug', 'position')
    inlines = [EntryTextbookCompoundInline]


admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryCategory, EntryCategoryAdmin)
admin.site.register(EntrySentence, EntrySentenceAdmin)
admin.site.register(Textbook, TextbookAdmin)
