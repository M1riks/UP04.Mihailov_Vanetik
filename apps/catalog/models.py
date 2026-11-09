from django.db import models


class Brand(models.Model):
    """Категория товара."""
    name = models.CharField("Название", max_length=50, unique=True)
    country = models.CharField("Страна", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Good(models.Model):
    """Товар."""

    class Status(models.TextChoices):
        AVAILABLE = "available", "В наличии"
        RESERVED = "reserved", "Забронирован"
        SOLD = "sold", "Продан"

    class Type(models.TextChoices):
        PRODUCTS = "products", "Продукты"
        HOUSEHOLD_CHEMICALS = "household_chemicals", "Бытовая химия"
        GARDEN_SUPPLIES = "garden_supplies", "Товары для сада"
        COSMETICS = "cosmetics", "Косметика"

    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT,
        related_name="goods", verbose_name="Производитель",
    )
    name = models.CharField("Наименование", max_length=100)
    price = models.DecimalField("Цена, ₽", max_digits=12, decimal_places=2)
    weight_kg = models.DecimalField(
        "Вес, кг", max_digits=5, decimal_places=2, null=True, blank=True,
    )
    status = models.CharField(
        "Статус", max_length=20,
        choices=Status.choices, default=Status.AVAILABLE,
    )
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField("Тип", max_length=30, choices=Type.choices, default=Type.PRODUCTS)


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand.name} - ({self.name})"


    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE