from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstituteViewSet

router = DefaultRouter()
router.register(r'institutes', InstituteViewSet, basename='institute')

urlpatterns = [
    path('', include(router.urls)),
]