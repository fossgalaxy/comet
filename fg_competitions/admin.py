from django.contrib import admin
from .models import Competition, CompetitionLink, Track, Submission, SubmissionUpload

# Register your models here.
class CompetitionLinkInline(admin.TabularInline):
    model = CompetitionLink

class CompetitionAdmin(admin.ModelAdmin):
    inlines = [
        CompetitionLinkInline
    ]
admin.site.register(Competition, CompetitionAdmin)

class TrackAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("competition", "allow_submit", "allow_update")
    list_display = ("__str__", "allow_submit", "allow_update")
admin.site.register(Track, TrackAdmin)

class SubmissionUploadInline(admin.TabularInline):
    model = SubmissionUpload
    extra = 1

class SubmissionAdmin(admin.ModelAdmin):
    fieldsets = (
      (None, {
          'fields': ('name', 'track', ('owner', "sample"), 'description')
      }),
      ("Ranking", {
          'fields': ('ranking', 'ranking_rd', 'velocity')
      })
    )
    list_filter = ("track",)
    list_display = ("__str__", "track")
    inlines = [
        SubmissionUploadInline
    ]
admin.site.register(Submission, SubmissionAdmin)
