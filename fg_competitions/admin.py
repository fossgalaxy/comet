from django.contrib import admin
from .models import Competition, CompetitionLink, Track, Submission, SubmissionUpload, SubmissionText

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

    fieldsets = (
        (None, {
            'fields': ('name', 'competition', 'owner', 'description'),
        }),
        ("status", {
            'fields': ('allow_submit', 'allow_update', 'allow_download')
        }),
        ("Submission Types",{
            'fields': ('allow_sub_uploads', 'allow_sub_text')
        })
    )


admin.site.register(Track, TrackAdmin)

class SubmissionUploadInline(admin.TabularInline):
    model = SubmissionUpload
    extra = 1

class SubmissionTextInline(admin.TabularInline):
    model = SubmissionText
    extra = 1


class SubmissionAdmin(admin.ModelAdmin):
    fieldsets = (
      (None, {
          'fields': ('name', 'track', ('owner', "sample"), 'description', "submission_type")
      }),
      ("Ranking", {
          'fields': ('ranking', 'ranking_rd', 'velocity')
      })
    )
    list_filter = ("track",)
    list_display = ("__str__", "track")
    inlines = [
        SubmissionUploadInline,
        SubmissionTextInline
    ]
admin.site.register(Submission, SubmissionAdmin)
