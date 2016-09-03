from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.conf import settings

STATUS_LIST = [
    ("BP", "Build pending"),
    ("BF", "Build failed"),
    ("BS", "Build succeeded")
]

@python_2_unicode_compatible
class Competition(models.Model):
    """A high-level descripiton of a topic"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('competition_detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class CompetitionLink(models.Model):
    """A link to a document for the competition"""
    name = models.CharField(max_length=100)
    competition = models.ForeignKey(Competition, related_name="links")
    url = models.URLField()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Track(models.Model):
    """A variation in the rules of a competition"""
    name = models.CharField(max_length=100)
    competition = models.ForeignKey(Competition)

    # flags
    allow_submit = models.BooleanField(default=True)
    allow_update = models.BooleanField(default=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('track_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Submission(models.Model):
    """An individual entry into the competition"""
    # meta-data
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    # foreign keys
    track = models.ForeignKey(Track)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Scoring data (setup for geliko-2)
    ranking = models.FloatField(default=1500)
    ranking_rd = models.FloatField(default=350)
    velocity = models.FloatField(default=0.06)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["ranking", "ranking_rd"]
        unique_together = ( ("owner", "track"), )

@python_2_unicode_compatible
class SubmissionUpload(models.Model):
    """A version of a submission"""
    submission = models.ForeignKey(Submission, related_name='uploads')
    status = models.CharField(max_length=5, default="BP", choices=STATUS_LIST)
    created = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.upload)

    class Meta:
        ordering = ["-created"]
