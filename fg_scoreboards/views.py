from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import ScoreBoard, Game

class ScoreBoardView(DetailView):
    model = ScoreBoard

class GameList(ListView):
    model = Game
    paginate_by = 50

    def get_queryset(self):
        self.scoreboard = get_object_or_404(ScoreBoard, pk=int(self.kwargs.get('pk')))
        return Game.objects.filter(board=self.scoreboard).select_related('board').prefetch_related('stats', 'stats__player')

    def get_context_data(self, **kwargs):
        data = super(GameList, self).get_context_data(**kwargs)
        data['scoreboard'] = self.scoreboard
        return data
