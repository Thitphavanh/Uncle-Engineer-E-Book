from django.contrib import admin
from .models import *

@admin.register(EBookCategory)
class EBookCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class EBookImageAdmin(admin.TabularInline):
    model = EBookImage
    extra = 1


@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "cover_image", "is_available")
    search_fields = ("title",)
    inlines = [EBookImageAdmin]
