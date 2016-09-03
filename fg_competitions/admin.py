from django.contrib import admin
from models import Competition, CompetitionLink, Track, Submission, SubmissionUpload

# Register your models here.
class CompetitionLinkInline(admin.TabularInline):
    model = CompetitionLink

class CompetitionAdmin(admin.ModelAdmin):
    inlines = [
        CompetitionLinkInline
    ]

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Track)

class SubmissionUploadInline(admin.TabularInline):
    model = SubmissionUpload

class SubmissionAdmin(admin.ModelAdmin):
    inlines = [
        SubmissionUploadInline
    ]
admin.site.register(Submission, SubmissionAdmin)
