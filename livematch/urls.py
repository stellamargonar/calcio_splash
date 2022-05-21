from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'livematch', views.MatchViewSet, basename='livematch')

urlpatterns = [
    re_path(r"^api/", include(router.urls)),
    re_path(r"^livematch/", views.index),
]
