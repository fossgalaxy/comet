from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from fg_competitions.signals import handlers

class FgCompetitionsConfig(AppConfig):
    name = 'fg_competitions'
    verbose_name = "Competition Module"

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)
        from .signals import watchers

