from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from calcio_splash.models import Match
from livematch.serializers import MatchSerializer


def index(request):
    return render(request, "livematch/index.html")


class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer

    def get_queryset(self):
        return Match.objects.all()
