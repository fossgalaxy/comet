from __future__ import unicode_literals

from django.apps import AppConfig

class FgCompetitionsConfig(AppConfig):
    name = 'fg_competitions'
    verbose_name = "Competition Module"

    def ready(self):
        import fg_competitions.signals

