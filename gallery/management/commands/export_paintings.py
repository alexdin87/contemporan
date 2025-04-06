import csv
import os
from django.core.management.base import BaseCommand
from gallery.models import Painting

class Command(BaseCommand):
    help = 'Export all paintings to a CSV file'

    def handle(self, *args, **options):
        output_dir = 'exports'
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, 'paintings_export.csv')
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Author', 'Year', 'Size', 'Description', 'Image'])

            for painting in Painting.objects.all():
                writer.writerow([
                    painting.title,
                    painting.author,
                    painting.year,
                    painting.size,
                    painting.description,
                    painting.image.name if painting.image else '',
                ])

        self.stdout.write(self.style.SUCCESS(f'✅ Exported paintings to {file_path}'))

