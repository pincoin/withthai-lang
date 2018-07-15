from django.contrib import admin

from .models import (
    Category, Attachment, Book, Page
)


class CategoryAdmin(admin.ModelAdmin):
    pass


class AttachmentAdmin(admin.ModelAdmin):
    pass


class BookAdmin(admin.ModelAdmin):
    pass


class PageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Page, PageAdmin)
