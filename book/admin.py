from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from ipware.ip import get_ip
from mptt.admin import (
    DraggableMPTTAdmin, MPTTModelAdmin
)

from .models import (
    Category, Attachment, Book, Page, Article, ArticleCategory
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


class ArticleCategoryFilterSpec(SimpleListFilter):
    title = _('category')
    parameter_name = 'category'

    def __init__(self, *args, **kwargs):
        self.categories = ArticleCategory.objects.filter(level__gt=0)
        super(ArticleCategoryFilterSpec, self).__init__(*args, **kwargs)

    def lookups(self, request, model_admin):
        categories = ()

        for category in self.categories:
            categories += ((str(category.id), category.title),)

        return categories

    def queryset(self, request, queryset):
        kwargs = {
            '{}'.format(self.parameter_name): self.value(),
        }
        if self.value() in list(map(lambda x: str(x.id), self.categories)):
            return queryset.filter(**kwargs)
        return queryset


'''
class PageInlineForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Page.objects.filter(book=2))


class PageInline(admin.StackedInline):
    model = Page
    form = PageInlineForm
    readonly_fields = ('ip_address', 'view_count', 'updated')
    extra = 1
'''


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'page', 'file', 'created')
    list_filter = (PageNullFilterSpec,)
    ordering = ['-created', ]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'status', 'license', 'owner', 'position')
    readonly_fields = ('view_count', 'updated')

    # inlines = [PageInline]

    def save_model(self, request, obj, form, change):
        obj.updated = now()
        super(BookAdmin, self).save_model(request, obj, form, change)


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


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'status')
    list_filter = (ArticleCategoryFilterSpec, 'status', 'owner')
    readonly_fields = ('ip_address', 'view_count', 'updated')

    def save_model(self, request, obj, form, change):
        obj.updated = now()

        if obj.id is None:
            obj.ip_address = get_ip(request)

        super(ArticleAdmin, self).save_model(request, obj, form, change)


class ArticleCategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
