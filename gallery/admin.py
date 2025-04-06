from django.contrib import admin
from .models import Painting
import csv
from django.http import HttpResponse

@admin.action(description='Export selected paintings to CSV')
def export_titles_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=paintings.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Year', 'Size', 'Description', 'Image'])  # Header

    for painting in queryset:
        writer.writerow([
            painting.title,
            painting.author,
            painting.year,
            painting.size,
            painting.description,
            painting.image.name if painting.image else '',
        ])

    return response

@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year")
    search_fields = ("title", "author")
    actions = [export_titles_to_csv]
