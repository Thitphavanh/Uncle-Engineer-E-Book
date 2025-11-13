from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ebooks/", views.ebooks, name="ebooks"),
    path("categories/", views.categories, name="categories"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("ebook/<slug:slug>/", views.ebook_detail, name="ebook_detail"),

    # Authentication URLs
    path("login/", views.user_login, name="login"),
]
