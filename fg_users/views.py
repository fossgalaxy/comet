from django.shortcuts import render
from django.views.generic.base import TemplateView

class ProfileView(TemplateView):
    template_name = "fg_users/profile.html"
