"""calcio_splash URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from calcio_splash import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^regulation/$', TemplateView.as_view(template_name='regulation.html'), name='regulation'),
    url(r'^fuoriposto/$', TemplateView.as_view(template_name='fuoriposto.html'), name='fuoriposto'),

    url(r'^admin/', admin.site.urls),
    url(r'^teams/$', views.TeamListView.as_view(), name='teams'),
    url(r'^team/(?P<pk>\d+)$', views.TeamDetailView.as_view(), name='team-detail'),
    url(r'^matches/$', views.MatchListView.as_view(), name='matches'),
    url(r'^match/(?P<pk>\d+)$', views.MatchDetailView.as_view(), name='match-detail'),

    url(r'^tournament/(?P<pk>\d+)$', views.TournamentDetailView.as_view(), name='tournament-detail'),

]
