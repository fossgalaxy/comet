from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Count
from .models import Competition, Track, Submission, SubmissionUpload

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "fg_competitions/organiser/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        context['tracks'] = Track.objects.filter(owner=self.request.user).annotate(Count('submission'))

        alerts = []
        for x in range(0, 5):
            alerts.append({
                "title": "Heading",
                "lead": "testing",
                "published": "4 hours ago"
            })

        context['alerts'] = alerts
        return context

class TrackUpdate(UserPassesTestMixin, UpdateView):
    model = Track
    raise_exception = True
    fields = ['name', 'description', 'allow_submit', 'allow_update']

    def test_func(self):
        """check the person attempting to edit the track is the owner"""
        obj = self.get_object()
        if not obj or not obj.owner:
            return False

        return obj.owner.pk == self.request.user.pk
