from django.shortcuts import render
from django.views.generic.base import TemplateView

from django.contrib.auth import get_user_model

class ProfileView(TemplateView):
    template_name = "fg_users/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        if "username" in kwargs:
            user_model = get_user_model()
            context['profile'] = user_model.objects.get(username=kwargs['username'])
        else:
            context['profile'] = self.request.user

        return context

class AccountSettings(TemplateView):
    template_name = "fg_users/settings.html"

    def get_context_data(self, **kwargs):
        context = super(AccountSettings, self).get_context_data(**kwargs)

        context['profile'] = self.request.user
        return context
