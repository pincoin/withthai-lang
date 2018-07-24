from django.contrib import admin

from .models import (
    Post, NoticeMessage, ContactMessage
)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'owner')
    list_select_related = ('owner',)
    list_display_links = ('title',)
    fields = ('title', 'slug', 'description', 'keywords', 'content', 'markup')
    ordering = ['-created']

    def save_model(self, request, obj, form, change):
        if obj.owner is None:
            obj.owner = request.user

        super(PostAdmin, self).save_model(request, obj, form, change)


class NoticeMessageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'created', 'owner')
    list_select_related = ('owner',)
    list_display_links = ('category', 'title')
    list_filter = ('category',)
    fields = ('title', 'description', 'keywords', 'category', 'content', 'markup')
    ordering = ['-created']

    def save_model(self, request, obj, form, change):
        if obj.owner is None:
            obj.owner = request.user

        super(NoticeMessageAdmin, self).save_model(request, obj, form, change)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    fields = ('title', 'fullname', 'email', 'phone', 'content')
    ordering = ['-created']


admin.site.register(Post, PostAdmin)
admin.site.register(NoticeMessage, NoticeMessageAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
