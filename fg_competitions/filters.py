import django_filters

from .models import Track

class TrackFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Track
        fields = ["name", "allow_submit", "competition"]

