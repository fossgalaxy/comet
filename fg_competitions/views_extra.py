from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import Competition, Track, Submission, SubmissionUpload

class Homepage(TemplateView):
    template_name = "fg_competitions/index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['tracks'] = Track.objects.order_by('?').filter(allow_submit=True).select_related('competition')[:3]
        return context

