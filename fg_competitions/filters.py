import django_filters

from .models import Track

class TrackFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    def filter_queryset(self, queryset):
        qs = super(TrackFilter, self).filter_queryset(queryset)
        return qs.prefetch_related('competition')

    class Meta:
        model = Track
        fields = ["name", "allow_submit", "competition"]

