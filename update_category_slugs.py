"""
Script to update slugs for existing EBookCategory objects
Run this script: python manage.py shell < update_category_slugs.py
or: python manage.py shell
then: exec(open('update_category_slugs.py').read())
"""

from ebook.models import EBookCategory
from django.utils.text import slugify

def update_category_slugs():
    categories = EBookCategory.objects.all()
    updated_count = 0

    for category in categories:
        if not category.slug:
            base_slug = slugify(category.name)
            slug = base_slug
            counter = 1

            # Check if slug already exists and create unique slug
            while EBookCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            category.slug = slug
            category.save()
            updated_count += 1
            print(f"Updated category: {category.name} -> {category.slug}")

    print(f"\nTotal categories updated: {updated_count}")

if __name__ == "__main__":
    update_category_slugs()
