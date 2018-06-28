from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.http.response import HttpResponse, FileResponse

from .models import Competition, Track, Submission, SubmissionUpload, SubmissionText, submission_path
from .forms import RegisterForm, UploadForm, SubmissionTextForm
from .filters import TrackFilter

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_filters.views import FilterView

from django.conf import settings
from django.utils.encoding import smart_str
import os

from fileprovider.utils import sendfile

class CompetitionList(ListView):
    """Provide a list of competitions"""
    model = Competition
    context_object_name = "competition_list"

def download_submission(request, pk=None):
    upload_entry = get_object_or_404(SubmissionUpload, pk=pk)

    if not request.user.is_staff:
        raise PermissionDenied()

    full_path = os.path.join(settings.MEDIA_ROOT, upload_entry.upload.name)

    #XXX this will not work in development mode
    #r = sendfile(full_path)

    # Send our own file response, forcing the content type to force download.
    r = FileResponse(open(full_path, 'rb'))
    r['Content-Type']="application/force-download"
    r['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(upload_entry.upload.name))

    return r


def download_submission_sendfile(request, pk=None):
    upload_entry = get_object_or_404(SubmissionUpload, pk=pk)

    if not request.user.is_authenticated():
        raise PermissionDenied()

    full_path = os.path.join(settings.MEDIA_ROOT, upload_entry.upload.name)

    response = HttpResponse(content_type="application/force-download")
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(upload_entry.upload.name))
    response['X-Sendfile'] = full_path

    return response


class TrackList(FilterView):
    """Provide a list of tracks"""
    filterset_class = TrackFilter
    context_object_name = "track_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TrackList, self).get_context_data(**kwargs)

        # Filter paramters - this is hacky
        # if there is a better way without using the form we should do that instead...
        context['competitions'] = Competition.objects.all()
        context['get_name'] = self.request.GET.get('name', '')
        context['get_allow_submit'] = self.request.GET.get('allow_submit', None)

        filter_comp = self.request.GET.get('competition', None)
        context['get_competition'] = int(filter_comp) if filter_comp else None

        if self.request.user.is_authenticated:
            results = Submission.objects.filter(
                owner=self.request.user,
                track__in=kwargs['object_list']
            ).values_list('track_id', 'pk')

            context['uploads'] = {track:pk for (track,pk) in results }
        else:
            context['uploads'] = {}

        return context

class SubmitterDashboard(TemplateView):
    """Mockup of submitter dashboard"""
    template_name = "fg_competitions/submitter_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
   
        # All tracks I have presently entered
        context['submissions'] = self.request.user.submission_set.all()
     
        context['tracks'] = Track.objects.all()
        return context

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

    def get_context_data(self, **kwargs):
        context = super(SubmissionDetail, self).get_context_data(**kwargs)
        context['pipeline'] = [
            {"name": "upload", "icon": "upload", "code": "U"},
            {"name": "build", "icon": "cubes", "code": "B"},
            {"name": "validate", "icon": "vial", "code": "V"}
        ]

        return context


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
    fields = ['name', 'description', 'allow_download']

    def get_context_data(self, **kwargs):
        context = super(SubmissionUpdate, self).get_context_data(**kwargs)
        submission_pk = self.kwargs.get('pk')
        submission = get_object_or_404(Submission, id=submission_pk)

        # if the user is not the owner of that submission, tell them off
        if not submission.owner == self.request.user:
            raise PermissionDenied()

        # check that the track allows updates
        if not submission.track.allow_update:
            raise PermissionDenied()

        return context

@method_decorator(login_required, name='dispatch')
class TextSubmission(CreateView):
    model = SubmissionText
    form_class = SubmissionTextForm

    def get_context_data(self, **kwargs):
        context = super(TextSubmission, self).get_context_data(**kwargs)
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
        context = super(TextSubmission, self).get_initial()
        context['submission'] = self.kwargs.get('submission', None)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "BS"
        form.instance.submission.submission_type = "T"
        return super(TextSubmission, self).form_valid(form)

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
        form.instance.submission.submission_type = "U"
        return super(UploadSubmission, self).form_valid(form)
