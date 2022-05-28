from django.contrib.auth.decorators import login_required
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'livematch', views.MatchViewSet, basename='livematch')

urlpatterns = [
    re_path(r"^api/", include(router.urls)),
    re_path(r"^livematch/", login_required(views.index, login_url='/admin/login/')),
]
