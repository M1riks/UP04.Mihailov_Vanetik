"""ViewSet автоматически создаёт все CRUD-эндпоинты:
GET    /api/goods/      – список
POST   /api/goods/      – создать
GET    /api/goods/{id}/ – детали
PUT    /api/goods/{id}/ – обновить
DELETE /api/goods/{id}/ – удалить"""

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Brand, Good
from .serializers import BrandSerializer, GoodSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """CRUD для марок."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "country"]


class GoodViewSet(viewsets.ModelViewSet):
    """CRUD для авто с фильтрами."""
    queryset = Good.objects.select_related("brand").all()
    serializer_class = GoodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["brand", "status", "type"]
    search_fields = ["name", "brand__name"]
    ordering_fields = ["price", "created_at"]
