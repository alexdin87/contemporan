import os
import csv
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from gallery.models import Painting

class Command(BaseCommand):
    help = "Load paintings from static input"

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'static', 'paintings.csv')
        image_folder = os.path.join(settings.BASE_DIR, 'static', 'paintings')

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['title']
                filename = row['filename']
                image_name = os.path.basename(filename)

                painting, created = Painting.objects.get_or_create(
                    title=title,
                    defaults={
                        'author': row['author'],
                        'description': row['description'],
                        'year': row['year'] if row['year'].isdigit() else None,
                        'size': row['size'],
                    }
                )

                full_target = os.path.join(settings.MEDIA_ROOT, 'paintings', image_name)
                image_path = os.path.join(image_folder, image_name)
                temp_copy = os.path.join(settings.MEDIA_ROOT, 'paintings', 'placeholder.jpeg')

                if not os.path.exists(image_path):
                    self.stdout.write(self.style.WARNING(f"Image not found: {image_name}"))
                    continue

                # Backup original file before deletion
                shutil.copyfile(image_path, temp_copy)

                # Always overwrite target
                if os.path.exists(full_target):
                    os.remove(full_target)

                with open(temp_copy, 'rb') as img_file:
                    painting.image.save(image_name, File(img_file), save=True)

                msg = f"Created: {title}" if created else f"Updated image for: {title}"
                self.stdout.write(self.style.SUCCESS(f"✅ {msg}"))

        # Optional: remove placeholder after loop
        if os.path.exists(temp_copy):
            os.remove(temp_copy)

        self.stdout.write(self.style.SUCCESS("🎉 Finished loading paintings."))

