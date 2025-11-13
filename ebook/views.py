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

    return render(request, "index.html",context)


@login_required(login_url='login')
def ebooks(request):
    # Get filter parameters
    category_slug = request.GET.get('category', None)
    search_query = request.GET.get('search', None)

    # Start with all available ebooks
    all_ebooks = EBook.objects.filter(is_available=True)

    # Filter by category if specified
    if category_slug:
        all_ebooks = all_ebooks.filter(category__slug=category_slug)

    # Filter by search query if specified
    if search_query:
        all_ebooks = all_ebooks.filter(
            models.Q(title__icontains=search_query) |
            models.Q(descriptions__icontains=search_query)
        )

    # Order by newest first
    all_ebooks = all_ebooks.order_by('-id')

    # Get all categories for filter
    categories = EBookCategory.objects.all().order_by('name')

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


@login_required(login_url='login')
def ebook_detail(request, slug):
    ebook = get_object_or_404(EBook, slug=slug, is_available=True)
    # Get all images related to this ebook
    ebook_images = ebook.covers_images.all().order_by('-is_primary', 'id')

    context = {
        "ebook": ebook,
        "ebook_images": ebook_images,
    }
    return render(request, "ebook/ebook-detail.html", context)


def categories(request):
    all_categories = EBookCategory.objects.all().order_by('name')

    # Count ebooks for each category
    categories_with_count = []
    for category in all_categories:
        ebook_count = category.ebooks.filter(is_available=True).count()
        categories_with_count.append({
            'category': category,
            'ebook_count': ebook_count
        })

    context = {
        "categories": categories_with_count,
    }
    return render(request, "ebook/categories.html", context)


@login_required(login_url='login')
def category_detail(request, slug):
    category = get_object_or_404(EBookCategory, slug=slug)
    ebooks = category.ebooks.filter(is_available=True).order_by('-id')

    context = {
        "category": category,
        "ebooks": ebooks,
        "ebook_count": ebooks.count(),
    }
    return render(request, "ebook/category-detail.html", context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'ยินดีต้อนรับ {user.username}!')

            # Redirect to next page if specified
            next_page = request.GET.get('next', 'index')
            return redirect(next_page)
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')

    return render(request, 'auth/login.html')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if password != confirm_password:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน')
            return render(request, 'auth/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'ชื่อผู้ใช้นี้มีอยู่แล้ว')
            return render(request, 'auth/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'อีเมลนี้มีอยู่แล้ว')
            return render(request, 'auth/register.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
        return redirect('login')

    return render(request, 'auth/register.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'ออกจากระบบเรียบร้อยแล้ว')
    return redirect('index')