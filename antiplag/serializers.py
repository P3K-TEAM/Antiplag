from rest_framework import serializers
from .models import Submission, Document


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("id", "status", "created_at", "updated_at")


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "name",
            "file",
            "submission",
            "text",
            "text_raw",
            "type",
            "language",
            "created_at",
            "updated_at"
        )


class DocumentResultSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "name")


class SubmissionDetailSerializer(serializers.ModelSerializer):
    documents = DocumentResultSummarySerializer(many=True)

    class Meta:
        model = Submission
        fields = ('status', 'documents')
