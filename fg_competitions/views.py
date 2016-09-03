from django.shortcuts import render
from django.views.generic import DetailView, ListView

from models import Competition, Track

class CompetitionList(ListView):
    """Provide a list of competitions"""
    model = Competition
    context_object_name = "competition_list"

class CompetitionDetail(DetailView):
    """View details about a competition"""
    model = Competition
    context_object_name = "competition"

class TrackDetail(DetailView):
    """View details about a track"""
    model = Track
    context_object_name = "track"
