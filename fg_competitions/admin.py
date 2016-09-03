from django.contrib import admin
from models import Competition, CompetitionLink

# Register your models here.
class CompetitionLinkInline(admin.TabularInline):
    model = CompetitionLink

class CompetitionAdmin(admin.ModelAdmin):
    inlines = [
        CompetitionLinkInline
    ]

admin.site.register(Competition, CompetitionAdmin)
