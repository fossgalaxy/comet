from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.http.response import HttpResponse, FileResponse

from .models import Competition, Track, TrackPage, Submission, SubmissionUpload, SubmissionText, submission_path
from .forms import RegisterForm, UploadForm, SubmissionTextForm
from .filters import TrackFilter

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib import messages
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
        try:
            context['get_competition'] = int(filter_comp) if filter_comp else None
        except ValueError:
            context['get_competition'] = None

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
        context['submissions'] = self.request.user.submission_set.filter(track__allow_update=True)

        return context

class CompetitionDetail(DetailView):
    """View details about a competition"""
    model = Competition
    context_object_name = "competition"

##
# Begin track detail code
##

class TrackTab(object):
    """Mixin for track views"""

    def get_context_data(self, **kwargs):
        context = super(TrackTab, self).get_context_data(**kwargs)

        context['tab_active'] = self.track_tab
        context['tabs'] = {
            'track_detail': 'Details',
            'track_scores': 'Leaderboard'
        }

        return context

class TrackDetail(TrackTab, DetailView):
    """View details about a track"""
    model = Track
    context_object_name = "track"
    track_tab = 'track_detail'

    def get_context_data(self, **kwargs):
        context = super(TrackDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['submission'] = Submission.objects.get(track=self.object, owner=self.request.user)
            except ObjectDoesNotExist:
                pass
        return context

class TrackPageView(TrackTab, DetailView):
    model = TrackPage
    context_object_name = "track_page"
    track_tab = 'track_detail'

    def get_context_data(self, **kwargs):
        context = super(TrackPageView, self).get_context_data(**kwargs)
       
        # track
        context['track'] = get_object_or_404(Track, id=self.kwargs.get('track'))

        return context

class TrackScoreView(TrackTab, TemplateView):
    template_name = 'fg_competitions/track_scores.html'
    context_object_name = "track_page"
    track_tab = 'track_scores'

    def get_context_data(self, **kwargs):
        context = super(TrackScoreView, self).get_context_data(**kwargs)
       
        # track
        context['track'] = get_object_or_404(Track.objects.select_related('competition'), id=self.kwargs.get('track'))
        context['submissions'] = context['track'].submission_set.all().select_related('owner')

        return context

##
# end track detail code
##

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
        messages.success(self.request, 'Submission created.')
        return super(SubmissionCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('submission_upload', kwargs={'submission': self.object.id})

@method_decorator(login_required, name='dispatch')
class SubmissionUpdate(UpdateView):
    model = Submission
    fields = ['name', 'description', 'paper', 'allow_download', 'is_student']

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

    def form_valid(self, form):
        messages.success(self.request, 'Submission updated.')
        return super(SubmissionUpdate, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class TextSubmission(CreateView):
    model = SubmissionText
    form_class = SubmissionTextForm

    def get_context_data(self, **kwargs):
        context = super(TextSubmission, self).get_context_data(**kwargs)
        submission = self.kwargs.get('submission')
        context['submission'] = get_object_or_404(Submission, id=submission)
        context['active_tab'] = 'text'

        # if the user is not the owner of that submission, tell them off
        if not context['submission'].owner == self.request.user:
            raise PermissionDenied()

        # check that the track allows updates
        track = context['submission'].track
        if not track.allow_update:
            raise PermissionDenied()

        # check that the track allows text submissions
        if not track.allow_sub_text:
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
        form.instance.submission.save()

        return super(TextSubmission, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class UploadSubmission(CreateView):
    model = SubmissionUpload
    form_class = UploadForm

    def get_context_data(self, **kwargs):
        context = super(UploadSubmission, self).get_context_data(**kwargs)
        submission = self.kwargs.get('submission')
        context['submission'] = get_object_or_404(Submission, id=submission)
        context['active_tab'] = 'upload'

        # if the user is not the owner of that submission, tell them off
        if not context['submission'].owner == self.request.user:
            raise PermissionDenied()

        # check that the track allows updates
        track = context['submission'].track
        if not track.allow_update:
            raise PermissionDenied()

        # check that the track allows file upload submissions
        if not track.allow_sub_uploads:
            raise PermissionDenied()

        return context

    def get_initial(self):
        context = super(UploadSubmission, self).get_initial()
        context['submission'] = self.kwargs.get('submission', None)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.submission.submission_type = "U"
        return super(UploadSubmission, self).form_valid(form)
