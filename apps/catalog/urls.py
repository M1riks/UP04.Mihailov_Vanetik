from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, GoodViewSet

router = DefaultRouter()
router.register("brands", BrandViewSet, basename="brands")
router.register("goods", GoodViewSet, basename="goods")

urlpatterns = [
    path("", include(router.urls)),
]