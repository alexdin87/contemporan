import csv
import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from gallery.models import Painting

class Command(BaseCommand):
    help = 'Add or update paintings from CSV without duplicating or suffixing image filenames.'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'paintings.csv')
        image_folder = os.path.join(settings.MEDIA_ROOT, 'paintings')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR("❌ paintings.csv not found"))
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                title = row['title']
                image_name = row['filename']
                image_path = os.path.join(image_folder, image_name)
                temp_copy = os.path.join(image_folder, 'placeholder.jpeg')

                if not os.path.exists(image_path):
                    self.stdout.write(self.style.WARNING(f"⚠️ Image not found: {image_name}"))
                    continue

                painting = Painting.objects.filter(title=title).first()

                if painting:
                    # Step 1: Copy the original to a safe placeholder
                    shutil.copyfile(image_path, temp_copy)

                    # Step 2: Remove existing image file to avoid suffix
                    full_target = os.path.join(settings.MEDIA_ROOT, 'paintings', image_name)
                    if os.path.exists(full_target):
                        os.remove(full_target)

                    # Step 3: Save image from the placeholder file
                    with open(temp_copy, 'rb') as img_file:
                        painting.image.save(image_name, File(img_file), save=True)

                    self.stdout.write(self.style.SUCCESS(f"✅ Overwrote image for existing painting: {title}"))
                else:
                    # New painting
                    painting = Painting(
                        title=title,
                        description=row['description'],
                        year=row['year'] or None,
                        author=row['author'],
                        size=row['size'],
                    )

                    # Ensure clean overwrite if image file already exists
                    full_target = os.path.join(settings.MEDIA_ROOT, 'paintings', image_name)
                    if os.path.exists(full_target):
                        os.remove(full_target)

                    # Step 1: Copy to temp
                    shutil.copyfile(image_path, temp_copy)

                    # Step 2: Save image
                    with open(temp_copy, 'rb') as img_file:
                        painting.image.save(image_name, File(img_file), save=False)

                    painting.save()
                    self.stdout.write(self.style.SUCCESS(f"🆕 Created new painting: {title}"))

                # Step 4: Delete the placeholder
                if os.path.exists(temp_copy):
                    os.remove(temp_copy)

