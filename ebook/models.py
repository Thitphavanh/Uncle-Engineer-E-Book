from django.db import models
from django.utils.text import slugify


class EBookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # Check if slug already exists and create unique slug
            while EBookCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)


class EBook(models.Model):
    category = models.ForeignKey(
        EBookCategory,
        on_delete=models.CASCADE,
        related_name="ebooks",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    descriptions = models.TextField()
    is_available = models.BooleanField(default=False, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    cover_image = models.ImageField(upload_to="covers/")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            # Check if slug already exists and create unique slug
            while EBook.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)
    
    


class EBookImage(models.Model):
    ebook = models.ForeignKey(
        EBook, related_name="covers_images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="covers/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ebook.title} - Image"
