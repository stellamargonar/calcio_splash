from rest_framework.routers import DefaultRouter

from django.contrib.auth.decorators import login_required
from django.urls import include, re_path

from . import views

router = DefaultRouter()
router.register(r'livematch', views.MatchViewSet, basename='livematch')
router.register(r'beachmatch', views.BeachMatchViewSet, basename='beachmatch')

urlpatterns = [
    re_path(r"^api/", include(router.urls)),
    re_path(r"^livematch/", login_required(views.index, login_url='/admin/login/'), name='livematch'),
    re_path(r"^beachmatch/", login_required(views.index, login_url='/admin/login/'), name='beachmatch'),
]
