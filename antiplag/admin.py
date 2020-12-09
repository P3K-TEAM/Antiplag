from django.contrib import admin
from .models import Submission, Result, Document

admin.site.register([Submission, Result, Document])
