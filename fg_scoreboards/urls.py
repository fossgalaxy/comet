from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url(r'^$', views.TrackList.as_view(), name="competitions"),

    url(r'^(?P<pk>\w+)/$', views.ScoreBoardView.as_view(), name="scoreboard"),
    url(r'^(?P<pk>\w+)/games/$', views.GameList.as_view(), name="scoreboard_games"),
]
