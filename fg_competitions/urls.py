from django.conf.urls import url, include

from django.urls import path, re_path
from . import views, views_organiser

urlpatterns = [
    path('', views.TrackList.as_view(), name="competitions"),

    # public URLs 
    path('t/<int:pk>/', views.TrackDetail.as_view(), name="track_detail"),
    path('s/<int:pk>/', views.SubmissionDetail.as_view(), name="submission_detail"),
    path('s/<int:submission>/text/', views.TextSubmission.as_view(), name="submission_text"),
    path('s/<int:submission>/upload/', views.UploadSubmission.as_view(), name="submission_upload"),
    path('d/<int:pk>/', views.download_submission, name="submission_download"),

    path('t/<int:track>/pages/<int:pk>/', views.TrackPageView.as_view(), name="track_page"),
    path('t/<int:track>/scores/', views.TrackScoreView.as_view(), name="track_scores"),

    # Submitter URLs
    path('db', views.SubmitterDashboard.as_view(), name="dashboard"),
    path('t/<int:track>/enter', views.SubmissionCreate.as_view(), name="submission_create"),
    path('s/<int:pk>/update', views.SubmissionUpdate.as_view(), name="submission_update"),

    # management urls
    path('t/<int:pk>/edit', views_organiser.TrackUpdate.as_view(), name="track_update"),
    path('odb', views_organiser.Dashboard.as_view(), name="org_dashboard"),

    # Depricated - urls not used anymore 
    url(r'^v/(?P<slug>\w+)$', views.CompetitionDetail.as_view(), name="competition_detail")
]

