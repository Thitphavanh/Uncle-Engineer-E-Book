from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from .models import EBook, EBookCategory


def index(request):
    ebooks = EBook.objects.filter(is_available=True).order_by("?")[:6]

    context = {
        "ebooks": ebooks,
    }

    return render(request, "index.html", context)


@login_required(login_url="login")
def ebooks(request):
    # Get filter parameters
    category_slug = request.GET.get("category", None)
    search_query = request.GET.get("search", None)

    # Start with all available ebooks
    all_ebooks = EBook.objects.filter(is_available=True)

    # Filter by category if specified
    if category_slug:
        all_ebooks = all_ebooks.filter(category__slug=category_slug)

    # Filter by search query if specified
    if search_query:
        all_ebooks = all_ebooks.filter(
            models.Q(title__icontains=search_query)
            | models.Q(descriptions__icontains=search_query)
        )

    # Order by newest first
    all_ebooks = all_ebooks.order_by("-id")

    # Get all categories for filter
    categories = EBookCategory.objects.all().order_by("name")

    # Get selected category for display
    selected_category = None
    if category_slug:
        selected_category = EBookCategory.objects.filter(slug=category_slug).first()

    context = {
        "all_ebooks": all_ebooks,
        "categories": categories,
        "selected_category": selected_category,
        "search_query": search_query,
        "total_count": all_ebooks.count(),
    }
    return render(request, "ebook/ebooks.html", context)


@login_required(login_url="login")
def ebook_detail(request, slug):
    ebook = get_object_or_404(EBook, slug=slug, is_available=True)
    # Get all images related to this ebook
    ebook_images = ebook.covers_images.all().order_by("-is_primary", "id")

    context = {
        "ebook": ebook,
        "ebook_images": ebook_images,
    }
    return render(request, "ebook/ebook-detail.html", context)


def categories(request):
    all_categories = EBookCategory.objects.all().order_by("name")

    # Count ebooks for each category
    categories_with_count = []
    for category in all_categories:
        ebook_count = category.ebooks.filter(is_available=True).count()
        categories_with_count.append({"category": category, "ebook_count": ebook_count})

    context = {
        "categories": categories_with_count,
    }
    return render(request, "ebook/categories.html", context)


@login_required(login_url="login")
def category_detail(request, slug):
    category = get_object_or_404(EBookCategory, slug=slug)
    ebooks = category.ebooks.filter(is_available=True).order_by("-id")

    context = {
        "category": category,
        "ebooks": ebooks,
        "ebook_count": ebooks.count(),
    }
    return render(request, "ebook/category-detail.html", context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"ยินดีต้อนรับ {user.username}!")

            # Redirect to next page if specified
            next_page = request.GET.get("next", "index")
            return redirect(next_page)
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, "auth/login.html")


# Static Pages
def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


def careers(request):
    return render(request, "pages/careers.html")


def partners(request):
    return render(request, "pages/partners.html")


def privacy_policy(request):
    return render(request, "pages/privacy-policy.html")


def terms_of_service(request):
    return render(request, "pages/terms-of-service.html")


# Cart Views
from django.views.decorators.http import require_POST
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(EBook, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)

    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({
            'status': 'success',
            'message': 'เพิ่มสินค้าลงตะกร้าแล้ว',
            'cart_count': len(cart)
        })

    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(EBook, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(EBook, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=True)

    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({'status': 'success'})

    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required(login_url="login")
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        # Get payment information
        payment_method = request.POST.get('payment_method', 'qr')
        payment_slip = request.FILES.get('payment_slip')
        note = request.POST.get('note', '')

        # Calculate total amount
        total_amount = cart.get_total_price()

        # Create Order
        from .models import Order, OrderItem
        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            payment_slip=payment_slip,
            note=note,
            total_amount=total_amount,
            status='pending'
        )

        # Create OrderItems
        for item in cart:
            OrderItem.objects.create(
                order=order,
                ebook=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear the cart
        cart.clear()

        messages.success(
            request,
            f"✅ สั่งซื้อเรียบร้อยแล้ว! หมายเลขคำสั่งซื้อของคุณคือ #{order.id} "
            f"{'เราได้รับสลิปโอนเงินของคุณแล้ว ' if payment_slip else ''}"
            f"ระบบจะตรวจสอบและยืนยันภายใน 24 ชั่วโมง"
        )
        return redirect('index')

    return render(request, 'cart/checkout.html', {'cart': cart})
