import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from gallery.models import Painting

class Command(BaseCommand):
    help = "Delete all paintings and load from CSV without duplicating image files"

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, "static", "paintings.csv")
        images_dir = os.path.join(settings.MEDIA_ROOT, "paintings")

        # Step 1: Delete all existing records
        Painting.objects.all().delete()
        self.stdout.write(self.style.WARNING("🧹 Deleted all existing paintings."))

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR("❌ CSV file not found."))
            return

        with open(csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                filename = row["filename"]
                image_path = os.path.join(images_dir, filename)

                if not os.path.exists(image_path):
                    self.stdout.write(self.style.WARNING(f"❌ Image not found: {filename}"))
                    continue

                painting = Painting(
                    title=row["title"] or "Untitled",
                    description=row["description"],
                    year=row["year"] or None,
                    author=row["author"],
                    size=row["size"],
                )

                # ✅ Just link to the file — no saving, no suffix
                painting.image.name = f"paintings/{filename}"
                painting.save()

                self.stdout.write(self.style.SUCCESS(f"✅ Linked: {painting.title}"))

        self.stdout.write(self.style.SUCCESS("🎉 Done loading paintings."))

