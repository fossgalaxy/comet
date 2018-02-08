from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings

STATUS_LIST = [
    ("BP", "Build pending"),
    ("BF", "Build failed"),
    ("BS", "Build succeeded"),
    ("DA", "Disqualified by admin")
]

SUBMISSION_TYPES = [
    ("T", "Text Submission"),
    ("U", "Upload")
]

@python_2_unicode_compatible
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

@python_2_unicode_compatible
class CompetitionLink(models.Model):
    """A link to a document for the competition"""
    name = models.CharField(max_length=100)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="links")
    url = models.URLField()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Track(models.Model):
    """A variation in the rules of a competition"""
    name = models.CharField(max_length=100)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # flags
    allow_submit = models.BooleanField(default=True)
    allow_update = models.BooleanField(default=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('track_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class AllowedSubmissionType(models.Model):
    """Types of submissions allowed"""
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    submission_type = models.CharField(max_length=1, choices=SUBMISSION_TYPES)

    def __str__(self):
        return self.get_submission_type_display()

    class Meta:
        unique_together = ( ("track", "submission_type"), )

@python_2_unicode_compatible
class Submission(models.Model):
    """An individual entry into the competition"""
    # meta-data
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    sample = models.BooleanField(default=False)
    submission_type = models.CharField(max_length=1, default="U", choices=SUBMISSION_TYPES)

    # foreign keys
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Scoring data (setup for geliko-2)
    ranking = models.FloatField(default=1500)
    ranking_rd = models.FloatField(default=350)
    velocity = models.FloatField(default=0.06)

    @property
    def pretty_score(self):
        curr_upload = self.current
        if not curr_upload:
            return "No submission"
        elif curr_upload.status != "BS":
            return curr_upload.get_status_display()
        else:
            return self.ranking

    @property
    def current_upload(self):
        return self.uploads.first()

    @property
    def current_text(self):
        return self.text_submissions.first()

    @property
    def current(self):
        if self.submission_type == "U":
            return self.current_upload
        elif self.submission_type == "T":
            ct = self.current_text
            print(ct)
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

    class Meta:
        abstract = True
        ordering = ["-created"]

@python_2_unicode_compatible
class SubmissionText(BaseSubmission):
    """A textual version of a submission"""
    submission = models.ForeignKey(Submission, related_name='text_submissions', on_delete=models.CASCADE)
    body = models.TextField(null=True)

    def __str__(self):
        return "{0}".format(self.body)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submission_detail', kwargs={'pk':self.submission.pk})

@python_2_unicode_compatible
class SubmissionUpload(BaseSubmission):
    """A version of a submission"""
    submission = models.ForeignKey(Submission, related_name='uploads', on_delete=models.CASCADE)
    upload = models.FileField(upload_to=submission_path, validators=[ExtensionValidator(['zip'])])

    def __str__(self):
        return "{0}".format(self.upload)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('submission_detail', kwargs={'pk':self.submission.pk})

