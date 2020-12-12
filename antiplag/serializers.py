from rest_framework import serializers
from .models import Submission, Document, Result


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


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ("id", "percentage", 'error_msg')


class DocumentResultSummarySerializer(serializers.ModelSerializer):
    percentage = serializers.ReadOnlyField(source='result.get.percentage')
    matches = serializers.ReadOnlyField(source='result.get.matches')

    class Meta:
        model = Document
        fields = ("id", "name", 'matches', 'percentage')


class SubmissionDetailSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ('status', 'documents')

    def get_documents(self, obj):
        if obj.status == Submission.SubmissionStatus.PROCESSED:
            documents = obj.documents.all()
            return DocumentResultSummarySerializer(documents, many=True).data
