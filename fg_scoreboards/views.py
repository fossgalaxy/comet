from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import ScoreBoard, Game

class ScoreBoardView(DetailView):
    model = ScoreBoard

class GameList(ListView):
    model = Game

    def get_context_data(self, **kwargs):
        data = super(GameList, self).get_context_data(**kwargs)
        data['scoreboard'] = get_object_or_404(ScoreBoard, pk=int(self.kwargs.get('pk')))
        return data
