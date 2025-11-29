from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ebooks/", views.ebooks, name="ebooks"),
    path("categories/", views.categories, name="categories"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    
    # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path("ebook/<slug:slug>/", views.ebook_detail, name="ebook_detail"),

    # Authentication URLs
    path("login/", views.user_login, name="login"),

    # Static Pages URLs
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("careers/", views.careers, name="careers"),
    path("partners/", views.partners, name="partners"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
]
