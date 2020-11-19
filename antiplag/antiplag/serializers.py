from rest_framework import serializers
from .models import Submission, Document
from django.core.files.uploadedfile import InMemoryUploadedFile


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['file', 'submission']

