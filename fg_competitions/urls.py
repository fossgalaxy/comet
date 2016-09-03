from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.CompetitionList.as_view(), name="competitions"),
    url(r'^v/(?P<slug>\w+)$', views.CompetitionDetail.as_view(), name="competition_detail"),
    url(r'^t/(?P<pk>\w+)$', views.TrackDetail.as_view(), name="track_detail"),
    url(r'^t/(?P<track>\w+)/enter$', views.SubmissionCreate.as_view(), name="submission_create"),
    url(r'^s/(?P<pk>\w+)$', views.SubmissionDetail.as_view(), name="submission_detail"),
    url(r'^s/(?P<submission>\w+)/upload$', views.UploadSubmission.as_view(), name="submission_upload"),
    url(r'^s/(?P<pk>\w+)/update$', views.SubmissionUpdate.as_view(), name="submission_update")
]
