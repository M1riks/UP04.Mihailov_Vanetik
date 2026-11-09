from django.contrib import admin
from .models import Brand, Good


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ("name",)


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ("brand", "name","type", "price", "status")
    list_filter = ("brand", "status")
    search_fields = ("name", "brand_name")
    list_editable = ("status",)
