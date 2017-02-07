from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Update(models.Model):
    """Something that users should be informed about"""
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=250)
    body = models.TextField(blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]
