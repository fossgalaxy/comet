from django.contrib import admin

from .models import ScoreBoard, Game, PlayerStats

# Register your models here.
class PlayerInline(admin.TabularInline):
    model = PlayerStats

class GameAdmin(admin.ModelAdmin):
    model = Game
    inlines = [PlayerInline]
    list_display = ['__str__', 'board']
    list_filter = ('board',)

admin.site.register(Game, GameAdmin)

admin.site.register(ScoreBoard)
