from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer, CompetitionSerializer, TrackSerializer, SubmissionSerializer, UploadSerializer, SubmissionTextSerializer
from .models import Competition, Track, Submission, SubmissionUpload, SubmissionText

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CompetitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class SubmissionTextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SubmissionText.objects.all()
    serializer_class = SubmissionTextSerializer

class UploadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SubmissionUpload.objects.all()
    serializer_class = UploadSerializer
