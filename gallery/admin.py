from django.contrib import admin
from .models import Painting

@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year")
    search_fields = ("title", "author")
