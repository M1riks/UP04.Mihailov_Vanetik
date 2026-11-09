"""МОДУЛЬ 4 (ЗАКАЗЫ): Админка."""

from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "good", "order_type", "total_amount", "status", "created_at")
    list_filter = ("status", "order_type", "created_at")
    search_fields = ("client__full_name", "good__name")
    readonly_fields = ("created_at", "completed_at")
    list_select_related = ("client", "good", "manager")