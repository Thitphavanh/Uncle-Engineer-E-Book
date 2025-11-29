#!/usr/bin/env python
"""
Script to update slugs for existing EBook instances
Run this script with: python3 update_slugs.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uncleebook.settings')
django.setup()

from ebook.models import EBook
from django.utils.text import slugify


def update_slugs():
    """Update slugs for all EBook instances that don't have a slug"""
    ebooks = EBook.objects.filter(slug__isnull=True) | EBook.objects.filter(slug='')

    if not ebooks.exists():
        print("All ebooks already have slugs!")
        return

    print(f"Found {ebooks.count()} ebooks without slugs. Updating...")

    for ebook in ebooks:
        base_slug = slugify(ebook.title)
        slug = base_slug
        counter = 1

        # Check if slug already exists and create unique slug
        while EBook.objects.filter(slug=slug).exclude(pk=ebook.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        ebook.slug = slug
        ebook.save()
        print(f"✓ Updated: '{ebook.title}' -> '{slug}'")

    print(f"\n✅ Successfully updated {ebooks.count()} ebooks!")


if __name__ == '__main__':
    update_slugs()
