from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอตรวจสอบ'),
        ('confirmed', 'ยืนยันแล้ว'),
        ('cancelled', 'ยกเลิก'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('qr', 'QR พร้อมเพย์'),
        ('transfer', 'โอนเงินธนาคาร'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_slip = models.ImageField(upload_to='payment_slips/', blank=True, null=True)
    note = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.get_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ebook = models.ForeignKey(EBook, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ebook.title} x {self.quantity}"

    def get_total(self):
        return self.price * self.quantity
