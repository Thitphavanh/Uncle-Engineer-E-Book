from django.contrib import admin
from .models import *

@admin.register(EBookCategory)
class EBookCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class EBookImageAdmin(admin.TabularInline):
    model = EBookImage
    extra = 1


@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "cover_image", "is_available")
    search_fields = ("title",)
    inlines = [EBookImageAdmin]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total',)
    can_delete = False

    def get_total(self, obj):
        if obj and obj.price and obj.quantity:
            return f"฿{obj.get_total():,.2f}"
        return "-"
    get_total.short_description = 'ยอดรวม'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'user__email', 'note')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('ข้อมูลคำสั่งซื้อ', {
            'fields': ('user', 'status', 'total_amount')
        }),
        ('ข้อมูลการชำระเงิน', {
            'fields': ('payment_method', 'payment_slip', 'note')
        }),
        ('เวลา', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user', 'total_amount')
        return self.readonly_fields

    def has_add_permission(self, request):
        # Prevent creating orders through admin - orders should only be created via checkout
        return False
