"""comet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from rest_framework import routers
from fg_competitions import rest_views

from fg_competitions import views_extra as extra

router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)
router.register(r'groups', rest_views.GroupViewSet)
router.register(r'competition', rest_views.CompetitionViewSet)
router.register(r'track', rest_views.TrackViewSet)
router.register(r'submission', rest_views.SubmissionViewSet)
router.register(r'upload', rest_views.UploadViewSet)
router.register(r'text', rest_views.SubmissionTextViewSet)

urlpatterns = [
    url(r'^$', extra.Homepage.as_view(), name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('fg_users.urls')),
    url(r'^competitions/', include('fg_competitions.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
