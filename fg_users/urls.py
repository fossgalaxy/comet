from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^profile/', views.ProfileView.as_view(), name="account_profile"),
    url(r'^', include('allauth.urls'))
]
