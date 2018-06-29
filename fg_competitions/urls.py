from django.conf.urls import url, include
from . import views, views_organiser

urlpatterns = [
    url(r'^$', views.TrackList.as_view(), name="competitions"),
    
    url(r'^tu/(?P<pk>\w+)$', views_organiser.TrackUpdate.as_view(), name="track_update"),
    
    url(r'^v/(?P<slug>\w+)$', views.CompetitionDetail.as_view(), name="competition_detail"),
    url(r'^t/(?P<pk>\w+)$', views.TrackDetail.as_view(), name="track_detail"),
    url(r'^t/(?P<track>\w+)/enter$', views.SubmissionCreate.as_view(), name="submission_create"),
    url(r'^s/(?P<pk>\w+)$', views.SubmissionDetail.as_view(), name="submission_detail"),
    url(r'^s/(?P<submission>\w+)/text$', views.TextSubmission.as_view(), name="submission_text"),
    url(r'^s/(?P<submission>\w+)/upload$', views.UploadSubmission.as_view(), name="submission_upload"),
    url(r'^s/(?P<pk>\w+)/update$', views.SubmissionUpdate.as_view(), name="submission_update"),
    url(r'^d/(?P<pk>\w+)/$', views.download_submission, name="submission_download"),
]

# Alpha urls
urlpatterns += [
    url(r'^odb$', views_organiser.Dashboard.as_view(), name="org_dashboard"),
    url(r'^db$', views.SubmitterDashboard.as_view(), name="dashboard"),
]
