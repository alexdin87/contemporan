import csv
import os
from django.core.management.base import BaseCommand
from gallery.models import Painting
from django.core.files import File

class Command(BaseCommand):
    help = 'Load paintings from CSV file (and replace existing ones)'

    def handle(self, *args, **kwargs):
        # ✅ Delete all existing paintings
        Painting.objects.all().delete()
        self.stdout.write(self.style.WARNING("Deleted all existing paintings."))

        with open('paintings.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                image_path = os.path.join('media/paintings', row['filename'])
                if not os.path.exists(image_path):
                    self.stdout.write(self.style.WARNING(f"Image not found: {row['filename']}"))
                    continue

                # Handle empty or invalid year
                try:
                    year = int(row['year']) if row['year'].strip() else None
                except ValueError:
                    year = None

                with open(image_path, 'rb') as img_file:
                    painting = Painting(
                        title=row['title'],
                        description=row['description'],
                        year=year,
                        author=row['author'],
                        size=row['size']
                    )
                    painting.image.save(row['filename'], File(img_file), save=True)

                self.stdout.write(self.style.SUCCESS(f"Imported: {row['title']}"))

