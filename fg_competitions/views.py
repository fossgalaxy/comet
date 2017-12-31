from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import Competition, Track, Submission, SubmissionUpload
from .forms import RegisterForm, UploadForm
from .filters import TrackFilter

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_filters.views import FilterView

class CompetitionList(ListView):
    """Provide a list of competitions"""
    model = Competition
    context_object_name = "competition_list"

class TrackList(FilterView):
    """Provide a list of tracks"""
    filterset_class = TrackFilter
    context_object_name = "track_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TrackList, self).get_context_data(**kwargs)
        context['competitions'] = Competition.objects.all()
        return context

class SubmitterDashboard(TemplateView):
    """Mockup of submitter dashboard"""
    template_name = "fg_competitions/submitter_dashboard.html"

class CompetitionDetail(DetailView):
    """View details about a competition"""
    model = Competition
    context_object_name = "competition"


class TrackDetail(DetailView):
    """View details about a track"""
    model = Track
    context_object_name = "track"

    def get_context_data(self, **kwargs):
        context = super(TrackDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['submission'] = Submission.objects.get(track=self.object, owner=self.request.user)
            except ObjectDoesNotExist:
                pass
        return context

class SubmissionDetail(DetailView):
    """View details about a submission"""
    model = Submission
    context_object_name = "submission"

@method_decorator(login_required, name='dispatch')
class SubmissionCreate(CreateView):
    model = Submission
    form_class = RegisterForm

    def get_form_kwargs(self):
        kwargs = super(SubmissionCreate, self).get_form_kwargs()
        kwargs.update({'owner': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreate, self).get_context_data(**kwargs)
        context['track'] = get_object_or_404(Track, id=self.kwargs.get('track'))
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.track_id = self.kwargs.get('track')
        return super(SubmissionCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('submission_upload', kwargs={'submission': self.object.id})

@method_decorator(login_required, name='dispatch')
class SubmissionUpdate(UpdateView):
    model = Submission
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        context = super(SubmissionUpdate, self).get_context_data(**kwargs)
        submission_pk = self.kwargs.get('pk')
        submission = get_object_or_404(Submission, id=submission)

        # if the user is not the owner of that submission, tell them off
        if not submission.owner == self.request.user:
            raise PermissionDenied()

        # check that the track allows updates
        if not submission.track.allow_update:
            raise PermissionDenied()

        return context

@method_decorator(login_required, name='dispatch')
class UploadSubmission(CreateView):
    model = SubmissionUpload
    form_class = UploadForm

    def get_context_data(self, **kwargs):
        context = super(UploadSubmission, self).get_context_data(**kwargs)
        submission = self.kwargs.get('submission')
        context['submission'] = get_object_or_404(Submission, id=submission)

        # if the user is not the owner of that submission, tell them off
        if not context['submission'].owner == self.request.user:
            raise PermissionDenied()

        # check that the track allows updates
        track = context['submission'].track
        if not track.allow_update:
            raise PermissionDenied()

        return context

    def get_initial(self):
        context = super(UploadSubmission, self).get_initial()
        context['submission'] = self.kwargs.get('submission', None)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UploadSubmission, self).form_valid(form)
