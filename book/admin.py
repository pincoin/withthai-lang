from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from ipware.ip import get_ip
from mptt.admin import MPTTModelAdmin

from .models import (
    Category, Attachment, Book, Page
)


class PageNullFilterSpec(SimpleListFilter):
    title = _('page')
    parameter_name = 'page'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Has page'),),
            ('0', _('No page'),),
        )

    def queryset(self, request, queryset):
        kwargs = {
            '{}'.format(self.parameter_name): None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class CategoryAdmin(admin.ModelAdmin):
    pass


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'page', 'file', 'created')
    list_filter = (PageNullFilterSpec,)
    ordering = ['-created', ]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'license', 'owner')
    readonly_fields = ('view_count', 'updated')


class PageAdmin(MPTTModelAdmin):
    list_display = ('title', 'book', 'owner', 'status')
    list_filter = ('book__title', 'status', 'owner')
    mptt_level_indent = 20
    readonly_fields = ('ip_address', 'view_count', 'updated')

    def save_model(self, request, obj, form, change):
        obj.updated = now()

        if obj.id is None:
            obj.ip_address = get_ip(request)

        super(PageAdmin, self).save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Page, PageAdmin)
