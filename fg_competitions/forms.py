from django import forms
from django.core.exceptions import ValidationError

from .models import Track, Submission, SubmissionUpload, SubmissionText

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('owner')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        if "track" not in self.cleaned_data:
            raise ValidationError("Invalid track provided")

        track = self.cleaned_data['track']
        if not track.allow_submit:
            raise ValidationError("registrations are not currently open")

    class Meta:
        fields = ["name", "description", "paper", "track", "allow_download", "is_student"]
        widgets = {'track': forms.HiddenInput()}
        model = Submission

class UploadForm(forms.ModelForm):

    class Meta:
        fields = ["upload", "submission"]
        widgets = {'submission': forms.HiddenInput()}
        model = SubmissionUpload

class SubmissionTextForm(forms.ModelForm):

    class Meta:
        fields = ["body", "submission"]
        widgets = {'submission': forms.HiddenInput()}
        model = SubmissionText
