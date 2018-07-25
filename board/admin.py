from django.contrib import admin

from .models import (
    Board, Category, Attachment, Message
)


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'theme', 'allow_comments', 'chunk_size', 'block_size')


class CategoryAdmin(admin.ModelAdmin):
    pass


class AttachmentAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Board, BoardAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Message, MessageAdmin)
