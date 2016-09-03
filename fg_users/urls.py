from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^profile/', views.ProfileView.as_view()),
    url(r'^', include('allauth.urls'))
]
