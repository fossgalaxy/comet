from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^settings/$', views.AccountSettings.as_view(), name="account_settings"),
    url(r'^profile/$', views.ProfileView.as_view(), name="account_profile"),
    url(r'^profile/(?P<username>\w+)/$', views.ProfileView.as_view(), name="account_profile"),
    url(r'^', include('allauth.urls'))
]
