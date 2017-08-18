from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Competition, Track, Submission, SubmissionUpload, SubmissionText

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition

class UploadReadOnlySerializer(serializers.ModelSerializer):
    upload = serializers.FileField(use_url=False)
    class Meta:
        model = SubmissionUpload
        fields = ('pk', 'upload', 'status', 'created', 'feedback')

class SubmissionTextReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionText
        fields = ('pk', 'body', 'status', 'created', 'feedback')

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionUpload
        fields = ('pk', 'status', 'created', 'feedback')

class SubmissionTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionText
        fields = ('pk', 'submission', 'status', 'body', 'created', 'feedback')

class SubmissionSerializer(serializers.ModelSerializer):
    current_upload = UploadReadOnlySerializer(read_only=True)
    current_text = SubmissionTextReadOnlySerializer(read_only=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Submission
        fields = ('pk', 'name', 'owner', 'ranking', 'ranking_rd', 'velocity', 'current_upload', 'current_text')
        read_only_fields = ["pk", "owner"]

class TrackSerializer(serializers.ModelSerializer):
    submission_set = SubmissionSerializer(many=True, read_only=True)
    class Meta:
        model = Track
        fields = ('pk', 'name', 'allow_submit', 'allow_update', 'submission_set')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'groups')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
