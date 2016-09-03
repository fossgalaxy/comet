from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import Competition, Track, Submission, SubmissionUpload

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionUpload
        fields = ('pk', 'upload', 'status', 'created', 'feedback')

class SubmissionSerializer(serializers.ModelSerializer):
    current_upload = UploadSerializer(read_only=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Submission
        fields = ('pk', 'name', 'owner', 'ranking', 'ranking_rd', 'velocity', 'current_upload')

class TrackSerializer(serializers.ModelSerializer):
    submission_set = SubmissionSerializer(many=True, read_only=True)
    class Meta:
        model = Track
        fields = ('pk', 'name', 'allow_submit', 'allow_update', 'submission_set')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
