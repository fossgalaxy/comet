from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.CompetitionList.as_view(), name="competitions"),
    url(r'^v/(?P<slug>\w+)$', views.CompetitionDetail.as_view(), name="competition_detail"),
    url(r'^t/(?P<pk>\w+)$', views.TrackDetail.as_view(), name="track_detail")
]
