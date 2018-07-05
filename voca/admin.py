from django.contrib import admin

from .models import (
    Entry, EntryCompound, EntryMeaning
)


class EntryAdmin(admin.ModelAdmin):
    pass


class EntryCompoundAdmin(admin.ModelAdmin):
    pass


class EntryMeaningAdmin(admin.ModelAdmin):
    pass


admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryCompound, EntryCompoundAdmin)
admin.site.register(EntryMeaning, EntryMeaningAdmin)
