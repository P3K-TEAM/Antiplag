from django.contrib import admin
from .models import User, Paper, File

# Register your models here.

admin.site.register(User)
#admin.site.register(Paper)

class FilesInline(admin.TabularInline):
    model = File


class FilesAdmin(admin.ModelAdmin):
    inlines = [
        FilesInline,
    ]

admin.site.register(Paper, FilesAdmin)