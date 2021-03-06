from __future__ import unicode_literals
from django.utils.functional import cached_property

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings

# Markdown Library
from martor.models import MartorField


BUILD_PIPELINE = [
    ("U", "upload", "fa-upload"),
    ("B", "build", "fa-build"),
    ("V", "validate", "fa-check")
]

STATUS_LIST = [
    # Complation/Build step
    ("BP", "Build pending"),
    ("BF", "Build failed"),

    # Validation Step
    ("VP", "Validation Pending"),
    ("VF", "Validation Failed"),

    # success states
    ("BS", "Build succeeded"),
    ("VS", "Validation succeeded"),

    # Disqualified
    ("DA", "Disqualified by admin")
]

SUBMISSION_TYPES = [
    ("T", "Text Submission"),
    ("U", "Upload")
]

# non-optional boolean field
YES_OR_NO = (
    ('y', 'Yes'),
    ('n', 'No')
)

class Competition(models.Model):
    """A high-level descripiton of a topic"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('competition_detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.name

class CompetitionLink(models.Model):
    """A link to a document for the competition"""
    name = models.CharField(max_length=100)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="links")
    url = models.URLField()

    def __str__(self):
        return self.name

class TrackManager(models.Manager):
    def get_queryset(self):
        return super(TrackManager, self).get_queryset().prefetch_related('competition')

class Track(models.Model):
    objects = TrackManager()

    """A variation in the rules of a competition"""
    name = models.CharField(max_length=100)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # Details page
    #details = MartorField(blank=True, help_text="")

    # submission permissions
    allow_submit = models.BooleanField(default=True, help_text="Can new submissions be added")
    allow_update = models.BooleanField(default=True, help_text="Can existing submissions be updated")

    # public flags
    allow_download = models.BooleanField(default=False)

    # Submission types
    allow_sub_uploads = models.BooleanField(default=True)
    allow_sub_text = models.BooleanField(default=False)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('track_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-allow_submit', 'name']

class TrackPage(models.Model):
    """A page describing the competition"""
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = MartorField(blank=True)

    def __str__(self):
        return self.title

class AllowedSubmissionType(models.Model):
    """Types of submissions allowed"""
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    submission_type = models.CharField(max_length=1, choices=SUBMISSION_TYPES)

    def __str__(self):
        return self.get_submission_type_display()

    class Meta:
        unique_together = ( ("track", "submission_type"), )

class Submission(models.Model):
    """An individual entry into the competition"""
    # meta-data
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, help_text="Briefly describe your submission")
    created = models.DateTimeField(auto_now_add=True)
    submission_type = models.CharField(max_length=1, default="U", choices=SUBMISSION_TYPES)

    # Extras
    paper = models.URLField(blank=True, null=True, help_text="Provide a link to your research paper")
    allow_download = models.BooleanField(default=True, verbose_name="Make public", help_text="Allow public distribution after results publication")
    is_student = models.CharField(max_length=1, choices=YES_OR_NO, verbose_name="Student Submission", help_text="Is this submission by a student?")
    sample = models.BooleanField(default=False)

    # foreign keys
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Scoring data (setup for geliko-2)
    ranking = models.FloatField(default=1500)
    ranking_rd = models.FloatField(default=350)
    velocity = models.FloatField(default=0.06)

    @property
    def is_public(self):
        """first check if submission has allowed download, if yes then delegate to track"""
        if not self.allow_download:
            return False
        else:
            return self.track.allow_download

    @property
    def pretty_score(self):
        curr_upload = self.current
        if not curr_upload:
            return "No submission"
        return self.ranking

    @property
    def is_valid(self):
        return self.current and self.current.is_valid

    @property
    def versions(self):
        if self.submission_type == "U":
            return self.uploads.all()
        elif self.submission_type == "T":
            return self.text_submissions.all()
        else:
            raise ValueError("unknown submission type")

    @cached_property
    def current_upload(self):
        return self.uploads.first()

    @cached_property
    def current_text(self):
        return self.text_submissions.first()

    @cached_property
    def current(self):
        if self.submission_type == "U":
            return self.current_upload
        elif self.submission_type == "T":
            ct = self.current_text
            return ct
        else:
            raise ValueError("unknown submission type")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submission_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-ranking", "ranking_rd"]
        unique_together = ( ("owner", "track"), )

def submission_path(instance, filename):
    return 'submissions/{0}/{1}'.format(instance.submission.pk, filename)

# This is far from foolproof, it should be combined with something else (like python magic)
from django.core.validators import RegexValidator
class ExtensionValidator(RegexValidator):
    def __init__(self, extensions, message=None):
        if not hasattr(extensions, '__iter__'):
            extensions = [extensions]
        regex = '\.(%s)$' % '|'.join(extensions)
        if message is None:
            message = 'File type not supported. Accepted types are: %s.' % ', '.join(extensions)
        super(ExtensionValidator, self).__init__(regex, message)

    def __call__(self, value):
        super(ExtensionValidator, self).__call__(value.name)

class BaseSubmission(models.Model):
    status = models.CharField(max_length=5, default="BP", choices=STATUS_LIST)
    created = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

    @property
    def is_valid(self):
        return self.status in ('BS', 'VS')

    def check_stage(self, check_stage):
        # check_stage = {upload, build, validate}
        # self.status -> current status of the upload {BP, BF, ...}
        # BUILD_PIPELINE = [ (B, build, icon), (V, validate, icon)... ]

        if self.status[0] == "D":
            return "bad"

        before = True

        for stage in BUILD_PIPELINE:
            if stage[0] == self.status[0]:
                before = False
                if check_stage == stage[1]:
                    if self.status[1] == "F":
                        return "failed"
                    elif self.status[1] == "S":
                        return "succeded"
                    elif self.status[1] == "P":
                        return "in progress"
                elif self.status[1] == "F":
                    return "skipped"
            elif check_stage == stage[1]:
                if before:
                    return "succeded"
                else:
                    return "pending"

        # was probably disqualifed...
        return "bad"

    class Meta:
        abstract = True
        ordering = ["-created"]

class SubmissionText(BaseSubmission):
    """A textual version of a submission"""
    submission = models.ForeignKey(Submission, related_name='text_submissions', on_delete=models.CASCADE)
    body = models.TextField(null=True)

    def __str__(self):
        return "{0}".format(self.body)

    @property
    def get_type(self):
        return "text"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submission_detail', kwargs={'pk':self.submission.pk})

class SubmissionUpload(BaseSubmission):
    """A version of a submission"""
    submission = models.ForeignKey(Submission, related_name='uploads', on_delete=models.CASCADE)
    upload = models.FileField(upload_to=submission_path, validators=[ExtensionValidator(['zip'])])

    @property
    def get_type(self):
        return "upload"

    def __str__(self):
        return "{0}".format(self.upload)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submission_detail', kwargs={'pk':self.submission.pk})
