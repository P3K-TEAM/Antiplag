from django.contrib import admin
from .models import User, Paper

# Register your models here.

admin.site.register(User)
#admin.site.register(Paper)

class PapersInline(admin.TabularInline):
    model = Paper


class PapersAdmin(admin.ModelAdmin):
    inlines = [
        PapersInline,
    ]

admin.site.register(Paper, PapersAdmin)