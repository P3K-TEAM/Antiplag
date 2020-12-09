from rest_framework import serializers
from .models import Submission, Document


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "status", "created_at", "updated_at"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["file", "submission", "text", "text_raw", "type", "language", "created_at", "updated_at"]
