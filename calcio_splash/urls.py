"""calcio_splash URL Configuration
"""
from django.urls import include, re_path
from django.contrib import admin
from django.views.generic import TemplateView

from calcio_splash import views
from calcio_splash.admin import admin_site

admin.autodiscover()


urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    re_path(r'^regulation/$', TemplateView.as_view(template_name='regulation.html'), name='regulation'),
    re_path(
        r'^regulation-beach/$', TemplateView.as_view(template_name='regulation_beach.html'), name='regulation-beach'
    ),
    re_path(r'^fuoriposto/$', TemplateView.as_view(template_name='fuoriposto.html'), name='fuoriposto'),
    re_path(r'^iscrizioni/$', TemplateView.as_view(template_name='iscrizioni.html'), name='iscrizioni'),
    re_path(r'^raise_exception/$', views.exception),
    re_path(r'^admin/', admin_site.urls),
    re_path(r'^team/(?P<pk>\d+)$', views.TeamDetailView.as_view(), name='team-detail'),
    re_path(r'^match/(?P<pk>\d+)$', views.MatchDetailView.as_view(), name='match-detail'),
    re_path(r'^beachmatch/(?P<pk>\d+)$', views.BeachMatchDetailView.as_view(), name='beach-match-detail'),
    re_path(r'^group/(?P<pk>\d+)$', views.GroupDetailView.as_view(), name='group-detail'),
    re_path(r'^tournament/(?P<pk>\d+)$', views.TournamentDetailView.as_view(), name='tournament-detail'),
    re_path(
        r'^tournament/(?P<pk>\d+)/group/(?P<pk_group>\d+)/matches/$',
        views.MatchListView.as_view(),
        name='group_matches',
    ),
    re_path(r'^matches/(?P<year>\d+)/$', views.MatchListView.as_view(), name='matches'),
    re_path(r'^classifiche/(?P<year>\d+)/$', views.AlboView.as_view(), name='albo'),
    re_path(r'^classifiche/(?P<gender>\w+)/$', views.AlboMarcatori.as_view(), name='albomarcatori'),
    re_path(r"", include("livematch.urls")),
]

handler404 = "calcio_splash.views.handler404"
handler500 = "calcio_splash.views.handler500"
