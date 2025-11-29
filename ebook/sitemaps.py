from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import EBook, EBookCategory


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'index',
            'ebooks',
            'categories',
            'about',
            'contact',
            'careers',
            'partners',
            'privacy_policy',
            'terms_of_service',
        ]

    def location(self, item):
        return reverse(item)


class EBookSitemap(Sitemap):
    """Sitemap for EBooks"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return EBook.objects.filter(is_available=True)

    def location(self, obj):
        return reverse('ebook_detail', args=[obj.slug])


class CategorySitemap(Sitemap):
    """Sitemap for Categories"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return EBookCategory.objects.all()

    def location(self, obj):
        return reverse('category_detail', args=[obj.slug])
