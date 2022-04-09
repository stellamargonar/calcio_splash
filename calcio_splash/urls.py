"""calcio_splash URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from calcio_splash import views
from calcio_splash.admin import admin_site

admin.autodiscover()


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="home"),
    url(
        r"^regulation/$",
        TemplateView.as_view(template_name="regulation.html"),
        name="regulation",
    ),
    url(
        r"^fuoriposto/$",
        TemplateView.as_view(template_name="fuoriposto.html"),
        name="fuoriposto",
    ),
    url(
        r"^iscrizioni/$",
        TemplateView.as_view(template_name="iscrizioni.html"),
        name="iscrizioni",
    ),
    url(r"^raise_exception/$", views.exception),
    url(r"^admin/", admin_site.urls),
    url(r"^teams/$", views.TeamListView.as_view(), name="teams"),
    url(r"^team/(?P<pk>\d+)$", views.TeamDetailView.as_view(), name="team-detail"),
    url(r"^match/(?P<pk>\d+)$", views.MatchDetailView.as_view(), name="match-detail"),
    url(
        r"^beachmatch/(?P<pk>\d+)$",
        views.BeachMatchDetailView.as_view(),
        name="beach-match-detail",
    ),
    url(r"^group/(?P<pk>\d+)$", views.GroupDetailView.as_view(), name="group-detail"),
    url(
        r"^tournament/(?P<pk>\d+)$",
        views.TournamentDetailView.as_view(),
        name="tournament-detail",
    ),
    url(
        r"^tournament/(?P<pk>\d+)/group/(?P<pk_group>\d+)/matches/$",
        views.MatchListView.as_view(),
        name="group_matches",
    ),
    url(r"^matches/(?P<year>\d+)/$", views.MatchListView.as_view(), name="matches"),
    url(r"^classifiche/(?P<year>\d+)/$", views.AlboView.as_view(), name="albo"),
    url(
        r"^classifiche/(?P<gender>\w+)/$",
        views.AlboMarcatori.as_view(),
        name="albomarcatori",
    ),
    url(r"", include("livematch.urls")),
]

handler404 = "calcio_splash.views.handler404"
handler500 = "calcio_splash.views.handler500"
