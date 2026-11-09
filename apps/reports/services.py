from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order
from apps.catalog.models import Good


class ReportService:
    """Сервис отчётов."""

    @staticmethod
    def get_kpi(days: int = 30) -> dict:
        """Главные KPI."""
        since = timezone.now() - timedelta(days=days)
        completed = Order.objects.filter(
            order_type=Order.OrderType.PURCHASE,
            status=Order.Status.COMPLETED,
            created_at__gte=since,
        )
        revenue = completed.aggregate(total=Sum("total_amount"))["total"] or 0
        count = completed.count()
        return {
            "revenue": float(revenue),
            "sales_count": count,
            "avg_check": float(revenue) / count if count else 0,
            "in_stock": Good.objects.filter(status=Good.Status.AVAILABLE).count(),
            "period_days": days,
        }

    @staticmethod
    def get_revenue_by_day(days: int = 30) -> list:
        """Выручка по дням."""
        since = timezone.now() - timedelta(days=days)
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.PURCHASE,
                status=Order.Status.COMPLETED,
                created_at__gte=since,
            )
            .annotate(day=TruncDate("completed_at"))
            .values("day")
            .annotate(total=Sum("total_amount"))
            .order_by("day")
        )
        return [{"date": str(r["day"]), "total": float(r["total"])} for r in rows]

    @staticmethod
    def get_top_models(limit: int = 5) -> list:
        """Топ моделей."""
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.PURCHASE,
                status=Order.Status.COMPLETED,
            )
            .values("good__brand__name", "good__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )
        return [
            {"brand": r["good__brand__name"], "name": r["good__name"], "count": r["count"]}
            for r in rows
        ]

    @staticmethod
    def get_manager_load(days: int = 30) -> list:
        """Загрузка менеджеров."""
        since = timezone.now() - timedelta(days=days)
        rows = (
            Order.objects.filter(
                order_type=Order.OrderType.PURCHASE,
                created_at__gte=since,
            )
            .values("manager__username")
            .annotate(count=Count("id"), total=Sum("total_amount"))
        )
        return [
            {"manager": r["manager__username"], "orders": r["count"], "total": float(r["total"] or 0)}
            for r in rows
        ]

    @staticmethod
    def stock_status() -> list:
        """Состояние склада."""
        return [
            {"status": r["status"], "count": r["count"]}
            for r in Good.objects.values("status").annotate(count=Count("id"))
        ]