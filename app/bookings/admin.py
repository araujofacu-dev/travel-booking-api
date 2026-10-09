from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Booking, Customer, Payment, TourPackage


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email")
    search_fields = ("first_name", "last_name", "email")


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "destination", "start_date", "price", "capacity", "is_active")
    list_filter = ("is_active", "destination")
    search_fields = ("name", "destination")


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "package", "seats", "status", "total_amount", "created_at")
    list_filter = ("status",)
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "status", "created_at")
    list_filter = ("status",)